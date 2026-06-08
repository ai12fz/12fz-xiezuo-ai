"""ONNX embedding providers."""

from fzxiezuoai.rag.embeddings.providers.onnx.onnx_provider import ONNXProvider
from fzxiezuoai.rag.embeddings.providers.onnx.types import (
    ONNXProviderConfig,
    ONNXProviderSpec,
)


__all__ = [
    "ONNXProvider",
    "ONNXProviderConfig",
    "ONNXProviderSpec",
]
