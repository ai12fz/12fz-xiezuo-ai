"""
12FZ协作AI security module.

This module provides security-related functionality for 12FZ协作AI, including:
- Fingerprinting for component identity and tracking
- Security configuration for controlling access and permissions
- Future: authentication, scoping, and delegation mechanisms
"""

from fzxiezuoai.security.fingerprint import Fingerprint
from fzxiezuoai.security.security_config import SecurityConfig


__all__ = ["Fingerprint", "SecurityConfig"]
