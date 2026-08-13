# Contributing

Keep examples synthetic, public and hardware-optional.

## Local Validation

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m pytest --cov --cov-report=term-missing -q
```

## Data Rules

Never add proprietary PGNs, corporate logs, private firmware, vehicle/customer identifiers, plates, serial numbers or screenshots from private benches.

