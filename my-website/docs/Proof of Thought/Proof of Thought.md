---
tags:
  - AI4CI
  - Software
  - Release 2026-03
---
# ProofOfThought

LLM-based reasoning using Z3 theorem proving with multiple backend support (SMT2 and JSON).

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/proofofthought)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Z3](https://img.shields.io/badge/Z3-4.15+-green.svg)](https://github.com/Z3Prover/z3)
[![OpenAI](https://img.shields.io/badge/OpenAI-Compatible-412991.svg)](https://platform.openai.com/)
[![Azure](https://img.shields.io/badge/Azure-GPT--4o/GPT--5-0078D4.svg)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)



## Features

- **Dual Backend Support**: Choose between SMT2 (default) or JSON execution backends
- **Azure OpenAI Integration**: Native support for Azure GPT-4o and GPT-5 models
- **Comprehensive Benchmarks**: Evaluated on 5 reasoning datasets (ProntoQA, FOLIO, ProofWriter, ConditionalQA, StrategyQA)
- **High-level API**: Simple Python interface for reasoning tasks
- **Batch Evaluation Pipeline**: Built-in tools for dataset evaluation and metrics
- **Postprocessing Techniques**: Self-Refine, Self-Consistency, Decomposed Prompting, and Least-to-Most Prompting for enhanced reasoning quality


## References

- [Z3 Theorem Prover](https://github.com/Z3Prover/z3) — The underlying SMT solver used by ProofOfThought.
- [OpenAI API](https://platform.openai.com/docs) — LLM provider for reasoning generation.
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/) — Azure-hosted LLM endpoint support.
- [SMT-LIB Standard](https://smtlib.cs.uiowa.edu/) — The SMT-LIB 2.0 standard used by the SMT2 backend.
- [Diataxis Documentation Framework](https://diataxis.fr/) — Framework guiding the structure of this documentation.

## Acknowledgements

This work was supported by:

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue Reporting

If you encounter any issues, please report them via [GitHub Issues](https://github.com/debarghaG/proofofthought/issues). When filing an issue, please include:
- A clear description of the problem
- Steps to reproduce the issue
- Your Python version and OS
- Relevant logs or error messages
