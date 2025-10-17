# Contributing to Málaga Reservoirs Weather Data Analysis

We welcome contributions to this project! This document provides guidelines for contributing.

## Types of Contributions

### 🐛 Bug Reports
- Use the GitHub issue tracker
- Include detailed description of the bug
- Provide steps to reproduce
- Include your environment details

### 📈 Feature Requests
- Open a GitHub issue with the "enhancement" label
- Describe the feature and its use case
- Explain why this feature would be useful

### 🔧 Code Contributions
- Fork the repository
- Create a feature branch (`git checkout -b feature/amazing-feature`)
- Make your changes
- Add tests for new functionality
- Ensure all tests pass
- Commit your changes (`git commit -m 'Add amazing feature'`)
- Push to the branch (`git push origin feature/amazing-feature`)
- Open a Pull Request

## Development Setup

1. Fork and clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run tests to ensure everything works:
   ```bash
   python -m pytest tests/
   ```

## Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Include type hints where appropriate
- Keep functions focused and concise

## Testing

- Write unit tests for new functions
- Ensure existing tests continue to pass
- Aim for good test coverage
- Test edge cases and error conditions

## Documentation

- Update README.md if needed
- Add docstrings to new functions
- Update methodology.md for significant changes
- Include examples in documentation

## Data Guidelines

- Do not commit large data files (use .gitignore)
- Include sample data for testing
- Document data sources and formats
- Ensure data privacy and licensing compliance

## Commit Messages

Use clear and descriptive commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for adding tests
- `refactor:` for code refactoring

Example: `feat: add correlation analysis for weather patterns`

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Update documentation as needed
3. Add tests for new functionality
4. Ensure all tests pass
5. Update CHANGELOG.md if applicable
6. Request review from maintainers

## Questions?

Feel free to open an issue for questions or join the discussion in existing issues.

Thank you for contributing! 🙏
