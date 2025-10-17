# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of our project seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do NOT create a public issue
Please do not report security vulnerabilities through public GitHub issues.

### 2. Send a private report
Instead, please send an email to the maintainers with the following information:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Any suggested fixes (if available)

### 3. Response Timeline
- We will acknowledge receipt of your vulnerability report within 48 hours
- We will provide a more detailed response within 5 business days
- We will work on a fix and keep you updated on our progress

### 4. Responsible Disclosure
We request that you:
- Give us reasonable time to address the issue before public disclosure
- Do not access or modify data that doesn't belong to you
- Do not perform actions that could be harmful to our users or infrastructure

## Security Best Practices for Users

### Data Protection
- Be cautious when sharing datasets containing sensitive information
- Ensure compliance with local data protection regulations
- Use secure channels when transmitting data files

### Code Security
- Always review code before running, especially from untrusted sources
- Keep your Python environment and dependencies up to date
- Use virtual environments to isolate project dependencies

### Environment Security
- Don't commit sensitive information (API keys, passwords) to version control
- Use environment variables for sensitive configuration
- Review the `.gitignore` file to ensure sensitive files are excluded

## Dependencies Security

We regularly monitor our dependencies for known security vulnerabilities. Users should:
- Keep dependencies updated to the latest secure versions
- Review security advisories for the packages used in this project
- Use tools like `pip-audit` to check for known vulnerabilities

## Reporting Security Issues in Dependencies

If you discover a security issue in one of our dependencies:
1. Report it to the dependency's maintainers first
2. If the issue affects this project, report it to us following the vulnerability reporting process above

Thank you for helping keep our project and users safe!
