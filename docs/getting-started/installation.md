# Installation

## Requirements

- Python 3.10 or higher
- pip

## Install from PyPI

```bash
pip install spec-test-generator
```

## Install from Source

```bash
git clone https://github.com/akz4ol/spec-test-generator-skill.git
cd spec-test-generator-skill
pip install -e .
```

## Install with Development Dependencies

```bash
pip install -e ".[dev]"
```

## Verify Installation

```bash
spec-test-generator --version
```

## Docker

```bash
docker pull ghcr.io/akz4ol/spec-test-generator:latest
docker run --rm -v $(pwd):/prds spec-test-generator /prds/prd.md
```
