"""Jina embedding providers."""

from fzxiezuoai.rag.embeddings.providers.jina.jina_provider import JinaProvider
from fzxiezuoai.rag.embeddings.providers.jina.types import (
    JinaProviderConfig,
    JinaProviderSpec,
)


__all__ = [
    "JinaProvider",
    "JinaProviderConfig",
    "JinaProviderSpec",
]
