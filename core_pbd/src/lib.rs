use glam::Vec3;
use numpy::PyArray1;
use pyo3::prelude::*;

pub type NodeID = usize;

#[derive(Clone, Copy, Debug)]
#[repr(C)]
pub struct Joint {
    pub position: Vec3,
    pub velocity: Vec3,
    pub mass: f32,
}

#[derive(Clone, Copy, Debug)]
#[repr(C)]
pub struct Link {
    pub joint_a: NodeID,
    pub joint_b: NodeID,
    pub compliance_alpha: f32,
    pub structural_integrity: f32,
}

#[derive(Clone, Copy, Debug)]
#[repr(C)]
pub struct Skin {
    pub joints: [NodeID; 3],
}

#[derive(Default, Clone, Debug)]
pub struct ArenaAllocator {
    pub joints: Vec<Joint>,
    pub links: Vec<Link>,
    pub skins: Vec<Skin>,
}

impl ArenaAllocator {
    pub fn new() -> Self {
        Self::default()
    }
}

/// The central world state for the engine.
#[pyclass]
pub struct World {
    allocator: ArenaAllocator,
}

impl Default for World {
    fn default() -> Self {
        Self::new()
    }
}

#[pymethods]
impl World {
    #[new]
    pub fn new() -> Self {
        let mut allocator = ArenaAllocator::new();
        // Add a few dummy joints so we have something to render
        for i in 0..100 {
            allocator.joints.push(Joint {
                position: Vec3::new((i as f32) * 0.1, 0.0, 0.0),
                velocity: Vec3::new(0.0, 0.1, 0.0),
                mass: 1.0,
            });
        }

        World {
            allocator,
        }
    }

    pub fn step(&mut self, dt: f32) {
        // Step PBD and Grids
        for joint in self.allocator.joints.iter_mut() {
            joint.position += joint.velocity * dt;
        }
    }

    /// Exposes the joints array as a zero-copy Python memoryview.
    /// This avoids making a copy and can be directly loaded into numpy or OpenGL.
    pub unsafe fn get_joints_buffer<'py>(
        &mut self, // note: mutable so we can pass WRITE flag if needed, but for now we do READ
        py: Python<'py>,
    ) -> PyResult<&'py PyAny> {
        let bytes_len = self.allocator.joints.len() * std::mem::size_of::<Joint>();
        let bytes_ptr = self.allocator.joints.as_ptr() as *const u8;

        // Return a zero-copy memoryview that points directly to the underlying rust Vec
        let mem = pyo3::ffi::PyMemoryView_FromMemory(
            bytes_ptr as *mut std::os::raw::c_char,
            bytes_len as isize,
            pyo3::ffi::PyBUF_READ
        );
        let mem_obj = py.from_owned_ptr_or_err(mem)?;
        Ok(mem_obj)
    }
}

/// A Python module implemented in Rust.
#[pyfunction]
fn dummy_array<'py>(py: Python<'py>) -> &'py PyArray1<f32> {
    let array = numpy::ndarray::Array1::from_vec(vec![1.0, 2.0, 3.0]);
    PyArray1::from_array(py, &array)
}

/// A Python module implemented in Rust.
#[pymodule]
fn core_pbd(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<World>()?;
    m.add_function(wrap_pyfunction!(dummy_array, m)?)?;
    Ok(())
}
