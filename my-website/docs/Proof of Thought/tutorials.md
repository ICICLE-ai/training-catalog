---
tags:
  - AI4CI
  - Software
---
# Tutorials

## Installation

### From PyPI (Recommended)

Install the latest stable version:

```bash
pip install proofofthought
```

**Note:** Package name is `proofofthought`, but imports use `z3adapter`:
```python
from z3adapter.reasoning import ProofOfThought
```

### From Source (Development)

For contributing or using the latest development version:

```bash
git clone https://github.com/debarghaG/proofofthought.git
cd proofofthought
pip install -r requirements.txt
```

### Prerequisites

- Python 3.12 or higher
- An OpenAI API key or Azure OpenAI endpoint
- Z3 solver (automatically installed via `z3-solver` package)

## Setup

### Environment Variables

Create a `.env` file in your project directory:

**For OpenAI:**
```bash
OPENAI_API_KEY=your-api-key-here
```

**For Azure OpenAI:**
```bash
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_KEY=your-azure-key-here
AZURE_DEPLOYMENT_NAME=gpt-5  # or gpt-4o
AZURE_API_VERSION=2024-02-15-preview
```

You can also set these as system environment variables instead of using a `.env` file.

## Quick Start

### Using OpenAI

```python
import os
from dotenv import load_dotenv
from openai import OpenAI
from z3adapter.reasoning import ProofOfThought

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize ProofOfThought
pot = ProofOfThought(llm_client=client, model="gpt-4o")

# Ask a question
result = pot.query("Would Nancy Pelosi publicly denounce abortion?")
print(result.answer)  # False
```

### Using Azure OpenAI

```python
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from z3adapter.reasoning import ProofOfThought

# Load environment variables
load_dotenv()

# Create Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_API_VERSION")
)

# Initialize ProofOfThought with your deployment name
pot = ProofOfThought(
    llm_client=client,
    model=os.getenv("AZURE_DEPLOYMENT_NAME")  # e.g., "gpt-4o" or "gpt-5"
)

# Ask a question
result = pot.query("Would Nancy Pelosi publicly denounce abortion?")
print(result.answer)  # False
```

## Examples

The `examples/` directory contains complete working examples for various use cases:

- **simple_usage.py** - Basic usage with OpenAI
- **azure_simple_example.py** - Simple Azure OpenAI integration
- **backend_comparison.py** - Comparing SMT2 vs JSON backends
- **batch_evaluation.py** - Evaluating on datasets
- **postprocessor_example.py** - Using postprocessing techniques

### Running Examples After pip Install

If you installed via `pip install proofofthought`, you can create your own scripts anywhere using the Quick Start examples above. The examples directory is primarily for development and testing.

### Running Examples in Development Mode

If you cloned the repository:

```bash
cd /path/to/proofofthought
python examples/simple_usage.py
```

**Note:** Some examples use helper modules like `utils/azure_config.py` which are only available when running from the repository root.
