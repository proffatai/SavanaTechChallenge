# Cloud IaC Analyzer

Small utility to compare resource items discovered in cloud runtime vs. infrastructure-as-code (IaC) definitions.

Purpose
- Provide a simple report showing whether a cloud resource is missing in IaC, matches, or is modified (property differences).

Quick start

1. Ensure you have Python 3.8+ installed.
2. Run the example that is embedded in `cloud_iac_analyzer.py`:

```bash
python3 cloud_iac_analyzer.py
```

Expected output
- The script prints a list of dictionaries (pretty-printed) with the following keys for each cloud resource:
  - `CloudResourceItem` — the cloud-side resource data
  - `IacResourceItem` — the matching IaC resource data (or `None` if missing)
  - `State` — one of `Missing`, `Match`, or `Modified`
  - `ChangeLog` — list of property diffs (empty when `Match`)

Example (trimmed)

```
[{'CloudResourceItem': {'id': 'res-1', 'type': 'storage', 'properties': {...}},
  'IacResourceItem': {'id': 'res-1', 'type': 'storage', 'properties': {...}},
  'State': 'Modified',
  'ChangeLog': [{'KeyName': 'size', 'CloudValue': '17kb', 'IacValue': '22kb'}, ...]
},
 ...]
```

Usage as a module
- Import `CloudToIacAnalyzer`, supply lists of `CloudResourceItem` and `IacResourceItem`, then call `analyze()` to get the report (list of dicts).