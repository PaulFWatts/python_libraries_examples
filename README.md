# Python Libraries Examples

A comprehensive collection of **production-ready demonstrations** showcasing essential and popular Python libraries. Each subdirectory contains independent, working examples designed to serve as learning resources and reference implementations.

## 🚀 Quick Start

This repository uses **UV** for modern Python tooling and package management. Each demonstration is self-contained with its own dependencies and virtual environment.

### Prerequisites

- Python 3.11+ 
- [UV](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh  # Unix
# or
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# Clone the repository
git clone https://github.com/PaulFWatts/python_libraries_examples.git
cd python_libraries_examples
```

### Running a Demo

```bash
# Navigate to any library demo
cd FastAPI  # Example

# Install dependencies and run
uv sync
uv run python main.py
```

## 📚 Library Categories

### Web Development
- **FastAPI** - Modern async web framework with automatic API documentation
- **Flask** - Lightweight WSGI web framework for rapid development
- **Django** - Full-featured web framework (comprehensive example)
- **Requests** - Elegant HTTP library for API interactions

### Data Science & Analysis
- **Pandas** - Data manipulation and analysis with real datasets
- **NumPy** - Numerical computing with performance examples
- **Matplotlib** - Data visualization with multiple chart types
- **Seaborn** - Statistical data visualization
- **Scikit-learn** - Machine learning algorithms and pipelines
- **Jupyter** - Interactive development environment examples

### Database & ORM
- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping
- **Pydantic** - Data validation using Python type hints
- **SQLite3** - Built-in database operations and best practices

### CLI & System
- **Click** - Command-line interface creation toolkit
- **Typer** - Modern CLI framework with type hints
- **Rich** - Rich text and beautiful formatting in terminal
- **Argparse** - Built-in command-line argument parsing

### Async & Networking
- **AsyncIO** - Asynchronous programming patterns
- **aiohttp** - Async HTTP client/server framework
- **Websockets** - WebSocket implementation examples

### Utilities & Configuration
- **python-dotenv** - Environment variable management
- **PyYAML** - YAML parser and configuration
- **ConfigParser** - Built-in configuration file handling
- **Logging** - Structured logging patterns

## 🏗️ Project Structure

Each library demonstration follows this standard structure:

```
LibraryDemo/
├── pyproject.toml          # UV project configuration & dependencies
├── uv.lock                 # Locked dependency versions
├── README.md               # Library-specific documentation
├── main.py                 # Primary demonstration entry point
├── src/                    # Source code (for library projects)
│   └── library_demo/
├── tests/                  # Comprehensive test suite
│   ├── test_main.py
│   └── conftest.py         # Pytest configuration
├── examples/               # Additional usage examples
├── data/                   # Sample data files (if applicable)
├── notebooks/              # Jupyter notebooks (data science demos)
└── requirements.txt        # Generated compatibility file
```

## 🛠️ Development Tools

This repository emphasizes modern Python development practices:

- **UV**: Fast, reliable package management and environment isolation
- **Ruff**: Lightning-fast Python linter and formatter
- **Black**: Code formatter for consistent style
- **Mypy**: Static type checking
- **Pytest**: Testing framework with rich plugin ecosystem
- **Pre-commit**: Git hooks for automated code quality

## 📖 Documentation Standards

Each demonstration includes:

- **Comprehensive README** with installation and usage instructions
- **Type annotations** on all public functions and classes  
- **Docstrings** following Google or NumPy documentation style
- **Jupyter notebooks** for data science libraries with step-by-step analysis
- **API documentation** for web framework examples
- **Code comments** explaining complex algorithms and patterns

## 🧪 Testing Requirements

All demonstrations maintain high testing standards:

- **Minimum 85% test coverage** for all demonstration code
- **Unit tests** for individual functions and classes
- **Integration tests** for end-to-end workflows
- **Performance benchmarks** where relevant
- **Mock examples** for external dependencies
- **Pytest fixtures** for reusable test data and setup

## 🔧 Common Commands

### Project Management
```bash
# Initialize new library demo
uv init --app library-demo
cd library-demo

# Add dependencies
uv add <package-name>
uv add --dev pytest black mypy

# Install all dependencies
uv sync
```

### Development Workflow
```bash
# Run the application
uv run python main.py

# Run tests with coverage
uv run pytest -v --cov --cov-report=html

# Format and lint code
uv run black .
uv run ruff check

# Type checking
uv run mypy .
```

### Package Management
```bash
# Update dependencies
uv lock --upgrade

# Export requirements
uv export --format requirements-txt > requirements.txt

# Install from requirements
uv pip install -r requirements.txt
```

## 🤝 Contributing

When adding new library demonstrations:

1. **Follow the established project structure** using UV project management
2. **Create comprehensive examples** that showcase real-world usage patterns
3. **Include thorough testing** with minimum 85% coverage
4. **Add proper documentation** with type hints and docstrings
5. **Use modern Python features** (dataclasses, type hints, context managers)

See the [AI Agent Instructions](.github/copilot-instructions.md) for detailed development guidelines.

## 📚 Featured Comprehensive Demonstrations

*Library demonstrations will be listed here as they are implemented*

## 📄 License

MIT License - feel free to use these examples in your own projects!

---

**Note**: This repository focuses on production-ready examples rather than minimal code snippets. Each demonstration is designed to be a comprehensive learning resource and reference implementation.
