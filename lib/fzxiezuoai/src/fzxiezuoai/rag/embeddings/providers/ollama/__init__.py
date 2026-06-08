"""Ollama embedding providers."""

from fzxiezuoai.rag.embeddings.providers.ollama.ollama_provider import (
    OllamaProvider,
)
from fzxiezuoai.rag.embeddings.providers.ollama.types import (
    OllamaProviderConfig,
    OllamaProviderSpec,
)


__all__ = [
    "OllamaProvider",
    "OllamaProviderConfig",
    "OllamaProviderSpec",
]
