# CAN J1939 Firmware Sniffer Lab

Laboratorio publico de sniffer CAN/J1939 com ESP32, MCP2515, firmware skeleton e ferramentas Python para parse, filtros, estatisticas e export.

## Por que existe

Um sniffer de bancada precisa ir alem de decompor um CAN ID. Ele deve considerar firmware, SPI, MCP2515, barramento CAN, frames estendidos, timestamp, saida serial, parser no computador, filtros, estatisticas e exportacao de evidencia.

## O que demonstra

- Firmware skeleton publico para ESP32/MCP2515.
- Formato serial de captura.
- Parser J1939 generico para priority, PGN, source e destination.
- Dataset sintetico.
- Filtros por PGN, source e destination.
- Export CSV/JSON.
- Testes automatizados.

## Validado

- Parser.
- Filtros.
- Estatisticas.
- Export CSV/JSON.
- Dataset sintetico.
- CI, CodeQL e dependency review.

## Ainda nao validado

- Barramento CAN fisico.
- Timing eletrico.
- Terminacao fisica.
- MCP2515 real.
- Clock real do modulo.
- Frames vindos de rede real.

## Como demonstrar sem hardware

```bash
python -m pip install -e ".[dev]"
j1939-sniffer-lab simulate --pgn 61444 --json reports/frames.json --csv reports/frames.csv
```

## Validacao fisica futura

Veja:

- [docs/bench-setup.md](docs/bench-setup.md)
- [docs/hardware-validation.md](docs/hardware-validation.md)

