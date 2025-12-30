# python_graphql_comparison
A side-by-side comparison of major Python GraphQL libraries (Graphene, Strawberry, Ariadne, Tartiflette) implemented within a single Django project.

## Development Setup

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. The hooks include:
- mypy for type checking
- ruff for linting and formatting
- Other basic checks (trailing whitespace, end-of-file fixing, etc.)

To set up the pre-commit hooks:

1. Install development dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```

2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. (Optional) Run the hooks against all files:
   ```bash
   pre-commit run --all-files
   ```

The hooks will run automatically on each commit. If any issues are found, the commit will be aborted until the issues are fixed.
