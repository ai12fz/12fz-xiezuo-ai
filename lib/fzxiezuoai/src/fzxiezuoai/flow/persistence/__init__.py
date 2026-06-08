"""
12FZ协作AI Flow Persistence.

This module provides interfaces and implementations for persisting flow states.
"""

from fzxiezuoai.flow.persistence.base import FlowPersistence
from fzxiezuoai.flow.persistence.decorators import persist
from fzxiezuoai.flow.persistence.sqlite import SQLiteFlowPersistence


__all__ = ["FlowPersistence", "SQLiteFlowPersistence", "persist"]
