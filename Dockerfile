# syntax=docker/dockerfile:1

FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN pip install --no-cache-dir build

# Copy source files
COPY pyproject.toml README.md ./
COPY src/ src/
COPY skills/ skills/
COPY schemas/ schemas/

# Build wheel
RUN python -m build --wheel

# Runtime stage
FROM python:3.11-slim

LABEL org.opencontainers.image.title="Spec & Test Generator"
LABEL org.opencontainers.image.description="Generate requirements and test artifacts from PRDs"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.source="https://github.com/yourorg/spec-test-generator-skill"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Copy wheel and install
COPY --from=builder /app/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl

# Copy skill files (policies, examples)
COPY --chown=appuser:appuser skills/ /app/skills/
COPY --chown=appuser:appuser schemas/ /app/schemas/

# Create output directory
RUN mkdir -p /app/spec && chown appuser:appuser /app/spec

USER appuser

# Set default policy path
ENV SPEC_GENERATOR_POLICY_PATH=/app/skills/spec-test-generator/policy/default.internal.yaml

ENTRYPOINT ["spec-test-generator"]
CMD ["--help"]
