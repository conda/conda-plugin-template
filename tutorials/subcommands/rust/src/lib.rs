use pyo3::prelude::*;

#[pyfunction]
// The original function is below
fn multiply(a: isize, b: isize) -> isize {
    a * b
}

#[pymodule]
fn rustiply(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(multiply, m)?)?;
    Ok(())
}
