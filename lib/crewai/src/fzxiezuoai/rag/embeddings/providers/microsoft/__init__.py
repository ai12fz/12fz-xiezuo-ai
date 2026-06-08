"""Microsoft embedding providers."""

from fzxiezuoai.rag.embeddings.providers.microsoft.azure import (
    AzureProvider,
)
from fzxiezuoai.rag.embeddings.providers.microsoft.types import (
    AzureProviderConfig,
    AzureProviderSpec,
)


__all__ = [
    "AzureProvider",
    "AzureProviderConfig",
    "AzureProviderSpec",
]
