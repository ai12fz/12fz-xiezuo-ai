"""Re-exports of OAuth2 primitives from ``fzxiezuoai_core.auth.oauth2``."""

from __future__ import annotations

from fzxiezuoai_core.auth.oauth2 import (
    AuthenticationCommand as AuthenticationCommand,
    Oauth2Settings as Oauth2Settings,
    ProviderFactory as ProviderFactory,
)


__all__ = ["AuthenticationCommand", "Oauth2Settings", "ProviderFactory"]
