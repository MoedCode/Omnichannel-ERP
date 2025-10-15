# Contributing to OmniMerch ERP

Thank you for considering contributing to OmniMerch ERP! This document outlines the process for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the issue list to avoid duplicates. When you create a bug report, include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps to reproduce the problem
* Provide specific examples
* Describe the behavior you observed and what you expected
* Include screenshots if applicable
* Include your environment details (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

* A clear and descriptive title
* A detailed description of the proposed functionality
* Explain why this enhancement would be useful
* List any alternative solutions you've considered

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the coding standards below
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Write clear commit messages**
6. **Submit a pull request**

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/OmniMerch-ERP.git
   cd OmniMerch-ERP
   ```

2. Run the setup script:
   ```bash
   ./setup.sh
   ```

3. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Coding Standards

### Python Style Guide

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
* Use 4 spaces for indentation (no tabs)
* Maximum line length of 100 characters
* Use meaningful variable and function names
* Add docstrings to all classes and functions

### Django Best Practices

* Follow Django's [coding style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)
* Use Django's built-in features when possible
* Keep views thin, models fat
* Use Django's ORM efficiently
* Write reusable code

### API Design

* Follow RESTful principles
* Use appropriate HTTP methods (GET, POST, PUT, PATCH, DELETE)
* Return appropriate status codes
* Include proper error messages
* Document all endpoints in Swagger

### Testing

* Write tests for new features
* Ensure all tests pass before submitting PR
* Aim for high code coverage
* Test edge cases

```bash
python manage.py test
```

### Database Migrations

* Create migrations for model changes:
  ```bash
  python manage.py makemigrations
  ```

* Always check migration files before committing
* Write reversible migrations when possible
* Add helpful comments for complex migrations

### Git Commit Messages

* Use present tense ("Add feature" not "Added feature")
* Use imperative mood ("Move cursor to..." not "Moves cursor to...")
* First line should be 50 characters or less
* Add detailed description if needed after a blank line

Example:
```
Add customer search functionality

- Implement search by name, email, and phone
- Add filters for customer type
- Update API documentation
```

## Project Structure

```
OmniMerch-ERP/
├── accounting/         # Accounting module
├── crm/               # CRM module
├── dashboard/         # Dashboard & analytics
├── inventory/         # Inventory management
├── maintenance/       # Maintenance management
├── sales/            # Sales module
└── omnimerch_erp/    # Main project settings
```

## Adding a New Module

If you're adding a new module:

1. Create the Django app:
   ```bash
   python manage.py startapp module_name
   ```

2. Add it to `INSTALLED_APPS` in `settings.py`

3. Create models, serializers, views, and URLs

4. Register models in `admin.py`

5. Update main `urls.py` to include module URLs

6. Write tests for the module

7. Update documentation

## Documentation

* Update README.md for major changes
* Update API_EXAMPLES.md for new endpoints
* Add docstrings to new functions and classes
* Update inline code comments as needed

## Testing Checklist

Before submitting a PR, ensure:

- [ ] All tests pass
- [ ] No linting errors
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Migrations are included (if needed)
- [ ] No sensitive data in commits
- [ ] API endpoints are documented
- [ ] Changes are tested manually

## Questions?

Feel free to open an issue for any questions or clarifications needed.

Thank you for contributing to OmniMerch ERP! 🎉
