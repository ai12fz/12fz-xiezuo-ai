"""AWS embedding providers."""

from fzxiezuoai.rag.embeddings.providers.aws.bedrock import BedrockProvider
from fzxiezuoai.rag.embeddings.providers.aws.types import (
    BedrockProviderConfig,
    BedrockProviderSpec,
)


__all__ = [
    "BedrockProvider",
    "BedrockProviderConfig",
    "BedrockProviderSpec",
]
