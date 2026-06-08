"""Type definitions for the embeddings module."""

from typing import Any, Literal, TypeAlias

from fzxiezuoai.rag.core.base_embeddings_provider import BaseEmbeddingsProvider
from fzxiezuoai.rag.embeddings.providers.aws.types import BedrockProviderSpec
from fzxiezuoai.rag.embeddings.providers.cohere.types import CohereProviderSpec
from fzxiezuoai.rag.embeddings.providers.custom.types import CustomProviderSpec
from fzxiezuoai.rag.embeddings.providers.google.types import (
    GenerativeAiProviderSpec,
    VertexAIProviderSpec,
)
from fzxiezuoai.rag.embeddings.providers.huggingface.types import HuggingFaceProviderSpec
from fzxiezuoai.rag.embeddings.providers.ibm.types import (
    WatsonXProviderSpec,
)
from fzxiezuoai.rag.embeddings.providers.instructor.types import InstructorProviderSpec
from fzxiezuoai.rag.embeddings.providers.jina.types import JinaProviderSpec
from fzxiezuoai.rag.embeddings.providers.microsoft.types import AzureProviderSpec
from fzxiezuoai.rag.embeddings.providers.ollama.types import OllamaProviderSpec
from fzxiezuoai.rag.embeddings.providers.onnx.types import ONNXProviderSpec
from fzxiezuoai.rag.embeddings.providers.openai.types import OpenAIProviderSpec
from fzxiezuoai.rag.embeddings.providers.openclip.types import OpenCLIPProviderSpec
from fzxiezuoai.rag.embeddings.providers.roboflow.types import RoboflowProviderSpec
from fzxiezuoai.rag.embeddings.providers.sentence_transformer.types import (
    SentenceTransformerProviderSpec,
)
from fzxiezuoai.rag.embeddings.providers.text2vec.types import Text2VecProviderSpec
from fzxiezuoai.rag.embeddings.providers.voyageai.types import VoyageAIProviderSpec


ProviderSpec: TypeAlias = (
    AzureProviderSpec
    | BedrockProviderSpec
    | CohereProviderSpec
    | CustomProviderSpec
    | GenerativeAiProviderSpec
    | HuggingFaceProviderSpec
    | InstructorProviderSpec
    | JinaProviderSpec
    | OllamaProviderSpec
    | ONNXProviderSpec
    | OpenAIProviderSpec
    | OpenCLIPProviderSpec
    | RoboflowProviderSpec
    | SentenceTransformerProviderSpec
    | Text2VecProviderSpec
    | VertexAIProviderSpec
    | VoyageAIProviderSpec
    | WatsonXProviderSpec
)

AllowedEmbeddingProviders = Literal[
    "azure",
    "amazon-bedrock",
    "cohere",
    "custom",
    "google-generativeai",
    "google-vertex",
    "huggingface",
    "instructor",
    "jina",
    "ollama",
    "onnx",
    "openai",
    "openclip",
    "roboflow",
    "sentence-transformer",
    "text2vec",
    "voyageai",
    "watsonx",
]

EmbedderConfig: TypeAlias = (
    ProviderSpec | BaseEmbeddingsProvider[Any] | type[BaseEmbeddingsProvider[Any]]
)
