# Python with UV Tooling Commands Cheat Sheet

## Project Management

| Command | Description |
|---------|-------------|
| `uv init <project-name>` | Initialize a new Python project |
| `uv init --lib <library-name>` | Initialize a new Python library |
| `uv init --app <app-name>` | Initialize a new Python application |
| `uv add <package>` | Add a dependency to the project |
| `uv add --dev <package>` | Add a development dependency |
| `uv remove <package>` | Remove a dependency from the project |
| `uv sync` | Install dependencies from lock file |
| `uv lock` | Update the lock file with current dependencies |
| `uv tree` | Display dependency tree |

## Virtual Environment Management

| Command | Description |
|---------|-------------|
| `uv venv` | Create a virtual environment in .venv |
| `uv venv <name>` | Create a virtual environment with custom name |
| `uv venv --python <version>` | Create venv with specific Python version |
| `uv venv --seed` | Create venv with pip, setuptools, and wheel |
| `uv activate` | Activate the virtual environment |
| `.venv\Scripts\activate` | Activate venv manually (Windows) |
| `source .venv/bin/activate` | Activate venv manually (Unix) |
| `deactivate` | Deactivate the virtual environment |

## Package Installation

| Command | Description |
|---------|-------------|
| `uv pip install <package>` | Install a package |
| `uv pip install <package>==<version>` | Install specific version |
| `uv pip install -r requirements.txt` | Install from requirements file |
| `uv pip install -e .` | Install current project in editable mode |
| `uv pip install --upgrade <package>` | Upgrade a package |
| `uv pip uninstall <package>` | Uninstall a package |
| `uv pip list` | List installed packages |
| `uv pip show <package>` | Show package information |
| `uv pip freeze` | Output installed packages in requirements format |

## Python Version Management

| Command | Description |
|---------|-------------|
| `uv python list` | List available Python versions |
| `uv python install <version>` | Install a specific Python version |
| `uv python install 3.12` | Install Python 3.12 |
| `uv python find` | Find Python installations |
| `uv python pin <version>` | Pin Python version for project |

## Build & Run

| Command | Description |
|---------|-------------|
| `uv run <script.py>` | Run a Python script in project environment |
| `uv run python <script.py>` | Run Python script explicitly |
| `uv run --with <package> <script.py>` | Run script with additional package |
| `uv build` | Build the project (wheel and sdist) |
| `uv build --wheel` | Build only wheel distribution |
| `uv build --sdist` | Build only source distribution |
| `python -m <module>` | Run a module as script |

## Testing

| Command | Description |
|---------|-------------|
| `uv run pytest` | Run tests with pytest |
| `uv run pytest -v` | Run tests with verbose output |
| `uv run pytest --cov` | Run tests with coverage |
| `uv run pytest --cov-report=html` | Generate HTML coverage report |
| `uv run pytest -k <pattern>` | Run tests matching pattern |
| `uv run pytest --lf` | Run only failed tests from last run |
| `uv run pytest --tb=short` | Show short traceback format |
| `uv run python -m unittest` | Run tests with unittest |
| `uv run python -m doctest <file.py>` | Run doctests |

## Code Quality & Formatting

| Command | Description |
|---------|-------------|
| `uv run black .` | Format code with Black |
| `uv run black --check .` | Check if code needs formatting |
| `uv run isort .` | Sort imports with isort |
| `uv run isort --check-only .` | Check import sorting |
| `uv run flake8` | Run flake8 linter |
| `uv run pylint <module>` | Run pylint on module |
| `uv run mypy .` | Run mypy type checker |
| `uv run ruff check` | Run ruff linter (fast) |
| `uv run ruff format` | Format code with ruff |

## Development Tools

| Command | Description |
|---------|-------------|
| `uv run jupyter notebook` | Start Jupyter notebook |
| `uv run jupyter lab` | Start JupyterLab |
| `uv run ipython` | Start IPython REPL |
| `uv run pre-commit install` | Install pre-commit hooks |
| `uv run pre-commit run --all-files` | Run pre-commit on all files |
| `uv run sphinx-build docs/ docs/_build/` | Build Sphinx documentation |

## Package Information & Search

| Command | Description |
|---------|-------------|
| `uv pip show <package>` | Show detailed package information |
| `uv pip list --outdated` | List outdated packages |
| `uv cache clean` | Clean the UV cache |
| `uv cache dir` | Show cache directory location |
| `uv index` | Show package index information |
| `uv tool list` | List installed tools |
| `uv tool install <package>` | Install a tool globally |
| `uv tool uninstall <package>` | Uninstall a global tool |

## Configuration & Environment

| Command | Description |
|---------|-------------|
| `uv --version` | Show UV version |
| `uv python --version` | Show Python version being used |
| `uv pip config list` | Show pip configuration |
| `uv pip config get <key>` | Get specific configuration value |
| `uv pip config set <key> <value>` | Set configuration value |
| `uv self update` | Update UV to latest version |

## Project File Management

| Command | Description |
|---------|-------------|
| `uv export --format requirements-txt` | Export to requirements.txt |
| `uv export --dev --format requirements-txt` | Export with dev dependencies |
| `uv pip compile requirements.in` | Compile requirements.in to requirements.txt |
| `uv pip compile --upgrade requirements.in` | Upgrade and compile requirements |
| `uv pip sync requirements.txt` | Sync environment with requirements |

## Publishing

| Command | Description |
|---------|-------------|
| `uv build` | Build package for distribution |
| `uv publish` | Publish package to PyPI |
| `uv publish --repository <url>` | Publish to custom repository |
| `uv publish --token <token>` | Publish with API token |
| `uv build --wheel` | Build only wheel |
| `uv build --sdist` | Build only source distribution |

## Common Flags

| Flag | Description |
|------|-------------|
| `--verbose` | Verbose output |
| `--quiet` | Suppress output |
| `--dry-run` | Show what would be done without executing |
| `--no-cache` | Disable cache usage |
| `--index-url <url>` | Use custom package index |
| `--extra-index-url <url>` | Add additional package index |
| `--constraint <file>` | Apply constraints from file |
| `--python <version>` | Use specific Python version |

## Examples

### Quick Start
```bash
# Create new project
uv init myproject
cd myproject

# Add dependencies
uv add requests pandas
uv add --dev pytest black

# Run the application
uv run python main.py

# Run tests
uv run pytest
```

### Development Workflow
```bash
# Set up development environment
uv venv
uv sync

# Add development tools
uv add --dev black isort flake8 mypy pytest pytest-cov

# Format and lint code
uv run black .
uv run isort .
uv run flake8
uv run mypy .

# Run tests with coverage
uv run pytest --cov --cov-report=html
```

### Package Management
```bash
# Update all dependencies
uv lock --upgrade

# Install from requirements.txt
uv pip install -r requirements.txt

# Export current environment
uv export --format requirements-txt > requirements.txt

# Create lock file for reproducible builds
uv lock
```

### Building and Publishing
```bash
# Build the package
uv build

# Install locally for testing
uv pip install -e .

# Publish to PyPI
uv publish

# Publish to test PyPI
uv publish --repository https://test.pypi.org/simple/
```

### Working with Multiple Python Versions
```bash
# Install Python versions
uv python install 3.11 3.12 3.13

# Create project with specific Python version
uv init --python 3.12 myproject

# Run with different Python version
uv run --python 3.11 python script.py
```

### Virtual Environment Best Practices
```bash
# Create environment with specific Python version
uv venv --python 3.12

# Create environment in custom location
uv venv --path ./custom-env

# Sync environment with project dependencies
uv sync

# Install additional packages temporarily
uv run --with requests python script.py
```

---
*Generated on: August 31, 2025*
