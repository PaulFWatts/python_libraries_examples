# AI Agent Instructions for Python Libraries Examples

## Project Architecture

This is a **Python libraries demonstration workspace** showcasing comprehensive examples of essential and popular built-in and third-party Python libraries. Each subdirectory contains independent demonstrations with working examples, using **UV for modern Python tooling and package management**.

### Key Structural Patterns

- **UV Project Management**: Each demo uses `pyproject.toml` for dependency management and project configuration
- **Virtual Environment Isolation**: Demos use UV-managed virtual environments for dependency isolation
- **Comprehensive Examples**: Demonstrations are production-ready with full applications, CLIs, or comprehensive test suites (not minimal snippets)
- **Modern Python Standards**: Following current best practices with type hints, dataclasses, and modern Python features

## Development Workflows

### Adding New Library Demonstrations

1. Create directory: `mkdir NewLibrary && cd NewLibrary`
2. Initialize project: `uv init --lib newlibrary-demo` or `uv init --app newlibrary-demo`
3. Add dependencies: `uv add <library-name>`
4. Add dev dependencies: `uv add --dev pytest black isort mypy`
5. Follow established patterns from flagship demos

### Critical Build Commands

```bash
# Project initialization and dependency management
uv sync                    # Install all dependencies from lock file
uv lock                    # Update lock file with current dependencies

# Development tools setup
uv add --dev pytest black isort mypy ruff pre-commit

# Running applications and scripts
uv run python main.py      # Run main application
uv run python -m <module>  # Run as module

# Testing comprehensive suites
uv run python -m pytest -v --cov    # Run tests with coverage (recommended)
uv run python -m pytest --cov-report=html  # Generate HTML coverage report

# Alternative direct pytest (may have issues on some systems)
# uv run pytest -v --cov    # Use python -m pytest instead if this fails

# Code quality and formatting
uv run black .            # Format code
uv run isort .            # Sort imports
uv run mypy .             # Type checking
uv run ruff check         # Fast linting

# Auto-fix formatting and linting issues
uv run ruff check . --fix # Auto-fix linting issues
uv run black .            # Auto-format code
```

### Git Workflow and Documentation Updates

```bash
# Complete workflow for new library demonstrations
# 1. Create and develop the library demo (see Adding New Library Demonstrations)
# 2. Run comprehensive testing and quality checks
uv run python -m pytest -v --cov --cov-report=html
uv run ruff check . --fix
uv run black .

# 3. Export requirements for compatibility
uv export --format requirements-txt > requirements.txt

# 4. Update root README.md to include the new demonstration
# Add entry to "Featured Comprehensive Demonstrations" section

# 5. Commit changes with descriptive message
git add -A
git commit -m "feat: Add comprehensive [LibraryName] demo with [key features]

- [Feature 1 description]
- [Feature 2 description]  
- [Testing/coverage details]
- [Documentation updates]"

# 6. Verify commit includes all necessary files
git log --oneline -1
git show --name-only HEAD
```

### Repository Maintenance

```bash
# After completing a library demonstration:
# 1. Update root README.md with new demo information
# Add entry to "📚 Featured Comprehensive Demonstrations" section
# Include key features, quick start instructions, and file locations

# 2. Ensure consistent documentation structure
# Each demo should have comprehensive README.md
# Include usage examples and installation instructions  
# Document any special requirements or setup steps

# 3. Validate overall repository health
cd <workspace_root>
uv run --directory FastAPI pytest  # Test specific demo
# Repeat for other demos as needed

# 4. Maintain repository-level documentation
# Keep main README.md current with all available demos
# Update PYTHON_UV_COMMANDS_CHEAT_SHEET.md if new patterns emerge
# Review and update copilot-instructions.md based on lessons learned
```

## Library-Specific Implementation Patterns

### Web Frameworks (FastAPI, Flask, Django)
- Always include CORS middleware and request logging
- Use Pydantic models for request/response validation
- Implement health check endpoints at `/health`
- Include both synchronous and asynchronous examples where applicable
- Example: OpenAPI documentation generation with FastAPI

### Data Science Libraries (Pandas, NumPy, Matplotlib, Scikit-learn)
- Comprehensive Jupyter notebooks with step-by-step analysis
- Real dataset examples with data cleaning and visualization
- Multiple algorithm demonstrations with performance comparisons
- Export results in multiple formats (CSV, JSON, PNG, SVG)

### Testing Frameworks (Pytest, Unittest, Mock)
- Comprehensive test categories: unit, integration, fixtures, parametrized
- Mock and patch examples for external dependencies
- Test configuration with `pytest.ini` or `pyproject.toml`
- Coverage analysis with detailed reporting (target 85%+ coverage)

### CLI Applications (Click, Argparse, Rich, Typer)
- Multi-command CLI structures with subcommands
- Progress bars, colored output, and interactive prompts
- Configuration file support and environment variable integration
- Help text generation and command validation

### Async Libraries (AsyncIO, aiohttp, aiofiles)
- Event loop management and async/await patterns
- Concurrent request handling with proper error handling
- Context managers for resource cleanup
- Performance comparisons with synchronous alternatives

## Cross-Component Integration

### Dependency Management Strategy
Each library demo maintains its own `pyproject.toml`:
```toml
[project]
name = "library-demo"
version = "0.1.0"
dependencies = ["requests>=2.31.0"]

[project.optional-dependencies]
dev = ["pytest>=7.0", "black>=23.0", "mypy>=1.0"]
```

### Data Flow Patterns
- Use Pydantic models for data validation across components
- SQLite for persistence demos (lightweight, no external dependencies)
- JSON/CSV for data interchange between examples
- Environment variable configuration with python-dotenv

### Code Quality Standards
- Type hints on all function signatures and class attributes
- Docstrings following Google or NumPy style
- Error handling with custom exceptions where appropriate
- Logging with structured output using Python's logging module

## Key Files for Understanding Patterns

- `pyproject.toml` - Project configuration and dependencies
- `uv.lock` - Locked dependency versions for reproducible builds
- `PYTHON_UV_COMMANDS_CHEAT_SHEET.md` - Project-specific tooling guide
- `main.py` or `app.py` - Primary application entry points
- `tests/` directories - Comprehensive testing strategies
- `requirements.txt` - Fallback compatibility (generated from UV)

## Critical Dependencies and Tools

### Essential Development Tools
- **UV**: Modern Python package installer and resolver
- **Ruff**: Fast Python linter and formatter (alternative to Black + isort)
- **Mypy**: Static type checker
- **Pytest**: Testing framework with rich plugin ecosystem
- **Pre-commit**: Git hooks for code quality

### Popular Library Categories to Demonstrate

#### Web Development
- **FastAPI**: Modern async web framework with automatic API docs
- **Flask**: Lightweight WSGI web framework
- **Django**: Full-featured web framework (minimal example)
- **Requests**: HTTP library for API interactions

#### Data Science & Analysis
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib/Seaborn**: Data visualization
- **Scikit-learn**: Machine learning library
- **Jupyter**: Interactive development environment

#### Database & ORM
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type hints
- **SQLite3**: Built-in database (for simple examples)

#### CLI & System
- **Click/Typer**: Command-line interface frameworks
- **Rich**: Rich text and beautiful formatting in terminal
- **Pathlib**: Modern path handling (built-in)
- **argparse**: Command-line parsing (built-in)

#### Async & Networking
- **AsyncIO**: Asynchronous programming (built-in)
- **aiohttp**: Async HTTP client/server
- **Websockets**: WebSocket implementation

#### Utilities & Configuration
- **python-dotenv**: Environment variable management
- **PyYAML**: YAML parser and emitter
- **configparser**: Configuration file parser (built-in)
- **logging**: Logging facility (built-in)

## Development Environment Setup

### Project Structure Template
```
LibraryDemo/
├── pyproject.toml          # UV project configuration
├── uv.lock                 # Locked dependencies
├── README.md               # Comprehensive documentation
├── main.py                 # Primary demonstration
├── src/                    # Source code (if library structure)
│   └── library_demo/
├── tests/                  # Test suite
│   ├── test_main.py
│   └── conftest.pytest    # Pytest configuration
├── examples/               # Additional usage examples
├── data/                   # Sample data files (if needed)
└── requirements.txt        # Generated compatibility file
```

### Standard pyproject.toml Template
```toml
[project]
name = "library-demo"
version = "0.1.0"
description = "Demonstration of [Library Name] usage patterns"
authors = [{name = "Your Name", email = "email@example.com"}]
dependencies = [
    "requests>=2.31.0",
    # Library-specific dependencies
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.5.0",
    "ruff>=0.0.290",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --cov=src --cov-report=html --cov-report=term"

[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

## Documentation Standards

Each demonstration includes:
- **README.md** with feature breakdown, installation, and usage examples
- **Inline code documentation** with comprehensive docstrings
- **Type annotations** on all public functions and classes
- **Example notebooks** for data science libraries (using Jupyter)
- **API documentation** for web framework examples

## Testing Requirements

- **Minimum 85% test coverage** for all demonstration code
- **Unit tests** for individual functions and classes
- **Integration tests** for end-to-end workflows
- **Performance benchmarks** where relevant (especially for data processing)
- **Mock examples** for external dependencies
- **Pytest fixtures** for common test data and setup

## Code Quality Standards

- **Type hints** required on all function signatures
- **Error handling** with custom exceptions and proper logging
- **Code formatting** with Black (88 character line length)
- **Import sorting** with isort (Black-compatible profile)
- **Linting** with Ruff for fast feedback
- **Pre-commit hooks** for automated quality checks

## Performance Considerations

- **Async examples** where libraries support asynchronous operations
- **Memory-efficient patterns** for data processing demonstrations
- **Benchmarking comparisons** between similar libraries
- **Profiling examples** using cProfile and memory_profiler where relevant

## Security & Best Practices

- **Environment variable management** with python-dotenv
- **Input validation** using Pydantic or similar
- **SQL injection prevention** in database examples
- **HTTPS/TLS examples** for network libraries
- **Rate limiting** and error handling in API examples

When adding new library demonstrations, prioritize comprehensive, production-ready examples that showcase real-world usage patterns rather than simple Hello World implementations. Each demo should stand alone as a learning resource and reference implementation.

---
*Instructions for AI agents working with the Python Libraries Examples repository*
