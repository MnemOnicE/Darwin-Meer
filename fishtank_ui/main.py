import sys
import os
import ctypes

# Set dummy drivers for headless execution (e.g. testing in CI)
if os.environ.get("CI") or os.environ.get("HEADLESS"):
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    os.environ["SDL_VIDEODRIVER"] = "dummy"

import moderngl
import pygame
import numpy as np

# Import the compiled Rust extension
import core_pbd

# Define the structure to unpack the zero-copy buffer correctly
# #[derive(Clone, Copy, Debug)]
# #[repr(C)]
# pub struct Joint {
#     pub position: Vec3,
#     pub velocity: Vec3,
#     pub mass: f32,
# }
# Vec3 is 3 floats. So position=3 floats, velocity=3 floats, mass=1 float. Total=7 floats (28 bytes).
JOINT_DTYPE = np.dtype(
    [("position", np.float32, 3), ("velocity", np.float32, 3), ("mass", np.float32)]
)


def main():
    pygame.init()

    # Try to setup Pygame for ModernGL
    # In headless CI environments missing libEGL/libGL, we bypass OpenGL init.
    try:
        pygame.display.set_mode(
            (800, 600), pygame.OPENGL | pygame.DOUBLEBUF | pygame.HIDDEN
        )
        ctx = moderngl.create_context()
        print("ModernGL and Pygame successfully initialized!")
        has_gl = True
    except Exception as e:
        print(
            f"Skipping ModernGL Context Creation (Running in headless/CI environment without libGL): {e}"
        )
        has_gl = False
        ctx = None
        # Just create a dummy display
        pygame.display.set_mode((800, 600), pygame.HIDDEN)

    # Initialize the Rust World
    world = core_pbd.World()

    # Access the zero copy memory view
    joints_memview = world.get_joints_buffer()

    # Cast memory view to numpy array via zero-copy
    joints_array = np.frombuffer(joints_memview, dtype=JOINT_DTYPE)

    if has_gl:
        # Create a basic shader to render points
        prog = ctx.program(
            vertex_shader="""
                #version 330
                in vec3 position;
                void main() {
                    // map from world coord to gl coord for testing
                    gl_Position = vec4(position.x - 5.0, position.y, position.z, 1.0);
                }
            """,
            fragment_shader="""
                #version 330
                out vec4 color;
                void main() {
                    color = vec4(1.0, 1.0, 1.0, 1.0);
                }
            """,
        )

        # Reserve a ModernGL VBO for the positions (3 floats per joint)
        vbo = ctx.buffer(reserve=len(joints_array) * 12)
        vao = ctx.vertex_array(prog, [(vbo, "3f", "position")])

    # Main loop
    clock = pygame.time.Clock()
    running = True

    # Just run a few frames for the test
    frames = 0
    while running and frames < 100:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 1. Step the Rust PBD World (this mutates the underlying memory in Rust!)
        dt = 1.0 / 60.0
        world.step(dt)

        if has_gl:
            # 2. Extract position data and write directly to GPU VBO
            # Note: joints_array is still viewing the updated memory!
            positions = np.ascontiguousarray(joints_array["position"])
            vbo.write(positions.tobytes())

            # 3. Render
            ctx.clear(0.1, 0.2, 0.3)
            vao.render(moderngl.POINTS)

        pygame.display.flip()
        clock.tick(60)
        frames += 1

    pygame.quit()
    print("Execution complete.")


if __name__ == "__main__":
    main()
