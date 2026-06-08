"""Custom embedding providers."""

from fzxiezuoai.rag.embeddings.providers.custom.custom_provider import CustomProvider
from fzxiezuoai.rag.embeddings.providers.custom.types import (
    CustomProviderConfig,
    CustomProviderSpec,
)


__all__ = [
    "CustomProvider",
    "CustomProviderConfig",
    "CustomProviderSpec",
]
