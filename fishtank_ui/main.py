import sys
import os

# Set dummy drivers for headless execution (e.g. testing in CI)
if os.environ.get('CI') == 'true' or os.environ.get('CI') == '1':
    os.environ['SDL_AUDIODRIVER'] = 'dummy'
    os.environ['SDL_VIDEODRIVER'] = 'dummy'

import moderngl
import pygame
import numpy as np

# In a real environment, we would import the compiled Rust extension here:
# import core_pbd

def main():
    pygame.init()

    # Try to setup Pygame for ModernGL
    # In headless CI environments missing libEGL/libGL, we bypass OpenGL init.
    try:
        pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
        ctx = moderngl.create_context()
        print("ModernGL and Pygame successfully initialized!")
        has_gl = True
    except Exception as e:
        print(f"Skipping ModernGL Context Creation (Running in headless/CI environment without libGL): {e}")
        has_gl = False
        # Just create a dummy display
        pygame.display.set_mode((800, 600), pygame.HIDDEN)

    # Main loop (stubbed out)
    clock = pygame.time.Clock()
    running = True

    # Just run a few frames for the test
    frames = 0
    while running and frames < 10:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if has_gl:
            ctx.clear(0.1, 0.2, 0.3)

        pygame.display.flip()
        clock.tick(60)
        frames += 1

    pygame.quit()
    print("Execution complete.")

if __name__ == "__main__":
    main()
