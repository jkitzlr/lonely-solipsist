# Yet Another Quant Library

Fixed income modeling library. Project is currently in pure python, with the first round implemented using jax for algorithmic differentiation.

Future iterations will convert low-level components, products,, market data, financial calculations and AD to hand-rolled Rust implementation.

## Tooling

Project uses the following tools for development:

* ruff for linting and formatting
* pyrefly for static analysis
* pytest for testing
* mkdocs for documenation (TBD)
* uv for project and dependency management as well as the build backend

pre-commit hooks are provided for ruff and pyrefly.
