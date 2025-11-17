# Contributing to Open Blog

Thank you for your interest in contributing to Open Blog! We welcome contributions from everyone. This document provides
guidelines and instructions for contributing.

## Getting Started

### Prerequisites

- Node.js 18+
- pnpm (or npm/yarn)
- Git

### Setup Development Environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/open-blog.git
   cd open-blog
   ```

3. Install dependencies:
   ```bash
   pnpm install
   ```

4. Create a `.env.local` file (copy from `.env.example`):
   ```bash
   cp .env.example .env.local
   ```

5. Update `.env.local` with your personal information

6. Start the development server:
   ```bash
   pnpm dev
   ```

   The site will be available at `http://localhost:3000`

## Development Workflow

### Creating a Branch

Create a feature branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:

- `feature/add-dark-mode`
- `fix/header-styling`
- `docs/update-readme`

### Making Changes

1. Make your changes in the appropriate files
2. Follow the existing code style and conventions
3. Keep commits atomic and focused
4. Write meaningful commit messages

### Running Tests

Before submitting a pull request, ensure all tests pass:

```bash
# Run all tests
pnpm test

# Run tests in watch mode
pnpm test --watch

# Run tests with UI
pnpm test:ui
```

### Linting and Formatting

Check and fix code quality:

```bash
# Check for linting issues
pnpm lint

# Format code
pnpm format

# Check formatting without modifying
pnpm format:check
```

### Building

Test the production build:

```bash
pnpm build
pnpm start
```

## Code Style Guidelines

### TypeScript

- Use strict mode (enabled by default)
- Define proper types for all functions and variables
- Avoid using `any` type when possible
- Use interfaces for object types

### Component Guidelines

- Use functional components with hooks
- Place components in `src/components/`
- Use TypeScript for component props
- Add appropriate prop documentation

### Testing

- Write tests for new features
- Aim for meaningful test coverage
- Keep tests focused and readable
- Use descriptive test names

Example:

```typescript
it("returns formatted date with long month", () => {
  const result = formatDate("2024-01-15", { month: "long" });
  expect(result).toContain("January");
});
```

## Commit Message Conventions

Write clear commit messages:

```
feat: add new feature description
fix: fix bug description
docs: update documentation
style: code style changes
refactor: refactor code
test: add or update tests
chore: update dependencies
```

Examples:

- `feat: add RSS feed generation`
- `fix: correct date formatting in blog posts`
- `test: add tests for feed generation`

## Submitting Changes

### Before Creating a Pull Request

1. Ensure your branch is up to date with `master`:
   ```bash
   git fetch origin master
   git rebase origin/master
   ```

2. Run tests and linting:
   ```bash
   pnpm test
   pnpm lint
   pnpm format:check
   ```

3. Build the project:
   ```bash
   pnpm build
   ```

### Creating a Pull Request

1. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a pull request on GitHub with:
    - Clear title describing the change
    - Description of what changed and why
    - Reference any related issues (e.g., `Closes #123`)
    - Screenshots for UI changes

3. Ensure all checks pass (tests, linting, etc.)

## Project Structure

```
open-blog/
├── src/
│   ├── app/              # Next.js app router
│   ├── components/       # React components
│   ├── lib/              # Utility functions and business logic
│   ├── config/           # Configuration files
│   └── styles/           # Global styles
├── public/               # Static assets
├── scripts/              # Utility scripts
├── tests/                # Test files
└── package.json          # Project dependencies
```

## Key Technologies

- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Content**: MDX
- **Testing**: Vitest
- **Code Quality**: ESLint, Prettier

## Reporting Issues

- Use GitHub Issues to report bugs
- Provide clear description and steps to reproduce
- Include screenshots if applicable
- Mention your environment (OS, Node version, etc.)

## Questions?

Feel free to:

- Open an issue with your question
- Ask in pull request discussions
- Refer to the CLAUDE.md for project architecture details

## License

By contributing to Open Blog, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉
