# Exemplos Publicos de Output

Todos os frames sao sinteticos.

## Input

```text
100,0x18F00401,8,11 22 33 44 55 66 77 88
180,0x18EAFF33,3,00 F0 00
```

## Comando

```bash
j1939-sniffer-lab simulate --pgn 61444 --json examples/filtered_pgn_61444.json --csv examples/filtered_pgn_61444.csv
```

## Output resumido

```json
{
  "statistics": {
    "total": 2,
    "by_pgn": {
      "61444": 2
    }
  }
}
```

## Arquivos

- `examples/synthetic_frames.txt`
- `examples/filtered_pgn_61444.json`
- `examples/filtered_pgn_61444.csv`

