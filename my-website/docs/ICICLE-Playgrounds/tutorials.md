---
tags:
  - Foundation-AI
---

# Tutorial

## Development

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd icicle-playgrounds

# Install dependencies
uv sync

# Install development dependencies
uv sync --group dev
```

### Running Tests

```bash
# Run tests using pytest
uv run pytest

# Or using just (if available)
just test
```

### Documentation Generation

This project includes a script to generate MDX documentation:

```bash
uv run python generate-mdx.py
```

## Dependencies

- **httpx** - HTTP client for API interactions
- **pillow** - Image processing capabilities
- **pydantic** - Data validation and serialization
- **torchvision** - Computer vision utilities