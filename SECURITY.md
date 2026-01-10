# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by emailing security@example.com or by opening a private security advisory on GitHub.

**Please do NOT open a public issue for security vulnerabilities.**

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution**: Depends on severity (critical: ASAP, high: 30 days, medium: 90 days)

## Security Best Practices

When using Spec & Test Generator:

1. **PRD files**: Be cautious with PRDs containing sensitive business logic
2. **ID map files**: The `.idmap.json` contains fingerprints, not sensitive data
3. **Output artifacts**: Review generated requirements/tests before sharing externally
