use numpy::PyArray1;
use pyo3::prelude::*;

/// The central world state for the engine.
#[pyclass]
pub struct World {
    // ECS and Grids will go here
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
        World {}
    }

    pub fn step(&mut self, _dt: f32) {
        // Step PBD and Grids
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
