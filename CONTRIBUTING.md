# Contributing to 3D Character Agent

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/3d-character-agent.git`
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Set up development environment (see [Installation](installation.md))

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dev dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy

# Run tests
pytest tests/
```

## Code Style

- Follow PEP 8
- Use type hints
- Format code with Black: `black src/`
- Lint with Flake8: `flake8 src/`

```bash
# Format and lint
black src/ tests/
flake8 src/ tests/
mypy src/
```

## Git Workflow

1. Create feature branch from `main`: `git checkout -b feature/description`
2. Make commits with clear messages: `git commit -m "Add feature description"`
3. Push to your fork: `git push origin feature/description`
4. Open a Pull Request with description of changes

## Pull Request Process

1. Update README.md with any new features
2. Update documentation in `/docs`
3. Add/update tests for new functionality
4. Ensure all tests pass: `pytest`
5. Ensure code is formatted: `black src/`
6. Add CHANGELOG entry
7. Request review from maintainers

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_agent.py::test_character_creation
```

## Areas for Contribution

### High Priority
- [ ] Motion capture integration
- [ ] Real-time preview rendering
- [ ] Advanced cloth simulation
- [ ] Crowd simulation
- [ ] Cloud rendering support

### Medium Priority
- [ ] Additional animation types
- [ ] More character customization options
- [ ] Performance optimizations
- [ ] Docker optimization
- [ ] API authentication/authorization

### Low Priority
- [ ] UI/Dashboard
- [ ] Documentation improvements
- [ ] Example scripts
- [ ] Error message improvements

## Reporting Issues

When reporting issues:
1. Use the issue template
2. Provide clear reproduction steps
3. Include system information (OS, Python version, etc.)
4. Attach error logs and screenshots

## Feature Requests

Before requesting features:
1. Check existing issues and discussions
2. Describe the use case clearly
3. Explain how it would benefit users
4. Provide examples or mockups if applicable

## Documentation

When adding features:
1. Update relevant docs in `/docs`
2. Add docstrings to functions/classes
3. Include usage examples
4. Update API guide if applicable

## Release Process

1. Update version in `src/__init__.py`
2. Update CHANGELOG.md
3. Create release PR
4. Merge to main
5. Create GitHub release with tag

## Questions?

- Check [Discussions](https://github.com/ashish894-commits/3d-character-agent/discussions)
- Open an issue with `question` label
- Contact maintainers

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

Thank you for contributing! 🎉
