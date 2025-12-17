# Global Copilot CLI Instructions

**Usage:** Copy this file to `~/.copilot/agents/default/instructions.md` to use globally across all projects.

## General Guidelines

- Follow project-specific instructions and style guides when available
- Prioritize clarity and maintainability over cleverness
- Add meaningful comments for complex logic
- Keep functions focused and single-purpose
- Use descriptive names for variables and functions

## Code Style

### Indentation & Formatting
- **JavaScript/YAML:** 2 spaces
- **Python:** 4 spaces  
- **Go:** Tabs (standard gofmt)
- **Rust:** 4 spaces (standard rustfmt)

### Naming Conventions
- **Functions:** camelCase (JavaScript), snake_case (Python, Go)
- **Classes:** PascalCase
- **Constants:** UPPER_SNAKE_CASE
- **Files:** kebab-case for JS/YAML, snake_case for Python

### Formatting Standards
- Line length: 100 characters (soft limit, 120 hard limit)
- Trailing commas in multi-line lists/objects
- Use semicolons in JavaScript
- Use `const` over `let` or `var`

## Best Practices

### Testing
- Write tests for all new functions
- Aim for >80% code coverage
- Test edge cases and error conditions
- Use descriptive test names

### Documentation
- Document public APIs with JSDoc/docstrings
- Include examples for complex functions
- Keep README.md up-to-date
- Document breaking changes in CHANGELOG

### Performance
- Use efficient algorithms (prefer O(n) over O(n²))
- Avoid unnecessary loops and calculations
- Cache results when appropriate
- Profile before optimizing

### Version Control
- Write clear, imperative commit messages
- Format: "Type: Brief description\n\nOptional detailed explanation"
- Reference issues: "Fixes #123" or "Closes #456"
- Keep commits atomic and logical

## Security Guidelines

### Secrets & Configuration
- **Never commit secrets** to version control
- Use environment variables for sensitive data
- Use `.env.example` template for configuration
- Rotate secrets regularly

### Input Validation
- Validate all user input
- Use allowlists instead of blocklists
- Sanitize data before using in queries/commands
- Check file paths for directory traversal attacks

### Dependencies
- Keep dependencies up-to-date
- Review dependency licenses (MIT, Apache 2.0 preferred)
- Check for known vulnerabilities (npm audit, cargo audit)
- Minimize dependency count

### Error Handling
- Never expose stack traces in production
- Log security events (failed auth, suspicious activity)
- Use proper HTTP status codes (401, 403, etc.)
- Don't reveal whether usernames/emails exist

## Error Handling

### General Approach
- Be explicit about error types
- Provide actionable error messages
- Include context about what went wrong
- Log errors with appropriate severity levels

### Examples

```javascript
// Good error handling
try {
  const result = await performAction();
} catch (error) {
  logger.error('Action failed', { error: error.message, context: { userId } });
  throw new CustomError('Action could not be completed. Please try again.', 'ACTION_FAILED');
}
```

## API Development

### REST Conventions
- Use proper HTTP verbs (GET, POST, PUT, DELETE)
- Use appropriate status codes (200, 201, 400, 401, 403, 404, 500)
- Return consistent JSON structure
- Include meaningful error responses

### Response Format
```json
{
  "success": true,
  "data": { /* ... */ },
  "error": null
}
```

## Database Guidelines

### Queries
- Use parameterized queries (prevent SQL injection)
- Add indexes to frequently queried columns
- Avoid N+1 queries
- Use transactions for related operations

### Migrations
- Write reversible migrations
- Test migrations on production-like data
- Deploy migrations before application code

## Frontend Development

### HTML/CSS
- Use semantic HTML tags
- Ensure proper heading hierarchy (h1, h2, h3...)
- Use aria labels for interactive elements
- Test with keyboard navigation

### Accessibility (a11y)
- Ensure 4.5:1 contrast ratio for text
- Support keyboard navigation
- Include alt text for images
- Test with screen readers

## DevOps & Deployment

### Configuration
- Use environment variables, not config files
- Use different configs per environment (dev, staging, prod)
- Store sensitive config in secrets manager

### Monitoring & Logging
- Log important events and errors
- Use structured logging (JSON format)
- Set up alerts for critical failures
- Monitor performance metrics

## Project-Specific Overrides

**Important:** Repository instructions in `.github/copilot-instructions.md` will override these global guidelines. Always check for project-specific requirements first.

---

**Last Updated:** 2024-12-17

Feel free to customize this file to match your personal coding standards and preferences!
