# fzxiezuoai-core

Shared utilities used by both `fzxiezuoai` and `fzxiezuoai-cli`: version lookup, storage
paths, user-data helpers, telemetry, and the printer.

This package is a leaf — it has no dependency on the `fzxiezuoai` framework — and is
pulled in transitively by `fzxiezuoai` and `fzxiezuoai-cli`. End users do not normally
install it directly.
