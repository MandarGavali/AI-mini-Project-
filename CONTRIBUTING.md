# Contributing to AI Flight Reminder Tool

Thank you for your interest in contributing to the AI Flight Reminder Tool! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

Before creating an issue, please:

1. **Search existing issues** to avoid duplicates
2. **Check if it's already fixed** in the latest version
3. **Use the issue template** when creating a new issue

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to reproduce**: Detailed steps to reproduce the problem
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: OS, Python version, browser (if applicable)
- **Screenshots**: If applicable, include screenshots

### Suggesting Enhancements

We welcome feature requests! Please:

1. **Check existing issues** for similar suggestions
2. **Describe the feature** clearly and concisely
3. **Explain the use case** and why it would be valuable
4. **Consider implementation** complexity and impact

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- A code editor (VS Code, PyCharm, etc.)

### Getting Started

1. **Fork the repository**

   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**

   ```bash
   git clone https://github.com/yourusername/ai-flight-reminder.git
   cd ai-flight-reminder
   ```

3. **Add upstream remote**

   ```bash
   git remote add upstream https://github.com/originalowner/ai-flight-reminder.git
   ```

4. **Create a virtual environment**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

5. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]  # Install development dependencies
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

### Development Workflow

1. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number
   ```

2. **Make your changes**

   - Write clean, readable code
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

3. **Test your changes**

   ```bash
   # Run tests
   python -m pytest tests/

   # Run with coverage
   python -m pytest tests/ --cov=app

   # Run linting
   flake8 app.py
   black app.py
   ```

4. **Commit your changes**

   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

5. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Fill out the PR template
   - Request review from maintainers

## 📝 Code Style Guidelines

### Python Code

- Follow **PEP 8** style guidelines
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes
- Keep functions **small and focused**
- Use **meaningful variable names**

### Example:

```python
def calculate_delay_probability(
    self,
    weather_data: dict,
    travel_date: str,
    city: str
) -> tuple[float, str, list[str]]:
    """
    Calculate AI-powered delay probability based on multiple factors.

    Args:
        weather_data: Weather forecast data from API
        travel_date: Travel date in YYYY-MM-DD format
        city: Departure city name

    Returns:
        Tuple of (probability, weather_main, risk_factors)
    """
    # Implementation here
    pass
```

### Streamlit Code

- Use **descriptive variable names**
- Add **help text** for user inputs
- Use **columns** for better layout
- Add **error handling** for API calls

## 🧪 Testing Guidelines

### Writing Tests

- Write tests for **new features**
- Test **edge cases** and error conditions
- Aim for **high test coverage**
- Use **descriptive test names**

### Test Structure

```python
def test_calculate_delay_probability_high_risk():
    """Test delay calculation with high-risk weather conditions."""
    # Arrange
    ai_system = FlightReminderAI()
    weather_data = {"list": [{"weather": [{"main": "Thunderstorm"}]}]}

    # Act
    prob, weather, risks = ai_system.calculate_delay_probability(
        weather_data, "2024-01-01", "mumbai"
    )

    # Assert
    assert prob > 0.5
    assert "Thunderstorm" in weather
    assert len(risks) > 0
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_app.py

# Run with coverage
python -m pytest --cov=app --cov-report=html

# Run with verbose output
python -m pytest -v
```

## 📚 Documentation

### Code Documentation

- Add **docstrings** to all functions and classes
- Use **Google-style docstrings**
- Include **examples** for complex functions
- Update **README.md** for new features

### API Documentation

- Document **new API endpoints**
- Include **request/response examples**
- Update **API reference** in docs/

## 🔍 Pull Request Guidelines

### Before Submitting

- [ ] **Tests pass** locally
- [ ] **Code is linted** and formatted
- [ ] **Documentation updated**
- [ ] **No merge conflicts**
- [ ] **Commit messages are clear**

### PR Description

Include:

- **Summary** of changes
- **Motivation** for the change
- **Testing** performed
- **Screenshots** (if UI changes)
- **Breaking changes** (if any)

### PR Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

- [ ] Tests pass locally
- [ ] New tests added
- [ ] Manual testing performed

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No merge conflicts
```

## 🏷️ Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] Update version in `setup.py`
- [ ] Update `CHANGELOG.md`
- [ ] Create release tag
- [ ] Update documentation
- [ ] Test deployment

## 🆘 Getting Help

### Questions and Support

- **GitHub Discussions**: For general questions
- **Issues**: For bug reports and feature requests
- **Discord/Slack**: For real-time chat (if available)

### Resources

- [Python Style Guide](https://pep8.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

## 📋 Contributor Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone, regardless of:

- Age, body size, disability, ethnicity
- Gender identity and expression
- Level of experience, education
- Nationality, personal appearance
- Race, religion, sexual orientation

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, trolling, or inappropriate comments
- Personal attacks or political discussions
- Public or private harassment
- Publishing private information without permission
- Other unprofessional conduct

## 🎉 Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page

Thank you for contributing to the AI Flight Reminder Tool! 🚀
