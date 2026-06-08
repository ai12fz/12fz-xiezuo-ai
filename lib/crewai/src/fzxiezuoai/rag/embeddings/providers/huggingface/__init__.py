"""HuggingFace embedding providers."""

from fzxiezuoai.rag.embeddings.providers.huggingface.huggingface_provider import (
    HuggingFaceProvider,
)
from fzxiezuoai.rag.embeddings.providers.huggingface.types import (
    HuggingFaceProviderConfig,
    HuggingFaceProviderSpec,
)


__all__ = [
    "HuggingFaceProvider",
    "HuggingFaceProviderConfig",
    "HuggingFaceProviderSpec",
]
