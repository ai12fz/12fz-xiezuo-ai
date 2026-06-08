"""IBM embedding providers."""

from fzxiezuoai.rag.embeddings.providers.ibm.types import (
    WatsonXProviderConfig,
    WatsonXProviderSpec,
)
from fzxiezuoai.rag.embeddings.providers.ibm.watsonx import (
    WatsonXProvider,
)


__all__ = [
    "WatsonXProvider",
    "WatsonXProviderConfig",
    "WatsonXProviderSpec",
]
