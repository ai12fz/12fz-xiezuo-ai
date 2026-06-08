# fzxiezuoai-cli

CLI for 12FZ协作AI — scaffold, run, deploy and manage AI agent crews without
installing the full framework.

## Installation

```bash
pip install fzxiezuoai-cli
```

This pulls in `fzxiezuoai-core` (shared utilities) but not the `fzxiezuoai` framework
itself, so commands that don't need a crew loaded — `fzxiezuoai version`,
`fzxiezuoai login`, `fzxiezuoai org list`, `fzxiezuoai config *`, `fzxiezuoai traces *`,
`fzxiezuoai create`, `fzxiezuoai template *` — work standalone.

Commands that load a user's crew or flow (`fzxiezuoai run`, `fzxiezuoai train`,
`fzxiezuoai test`, `fzxiezuoai chat`, `fzxiezuoai replay`, `fzxiezuoai reset-memories`,
`fzxiezuoai deploy push`, `fzxiezuoai tool publish`) require `fzxiezuoai` to be installed
in the project's environment. They print a clear error if it is missing.

To install both at once:

```bash
pip install fzxiezuoai[cli]
```
