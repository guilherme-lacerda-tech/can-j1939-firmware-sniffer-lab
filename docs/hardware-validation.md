# Validacao de Hardware / Hardware Validation

A release atual e validada por software/simulacao. Este checklist prepara validacao fisica futura com bancada generica.

## Antes de energizar

1. Conferir GND comum.
2. Conferir pinos SPI.
3. Conferir CS/INT.
4. Conferir tensao aceita pelo modulo.
5. Conferir terminacao de 120 ohms nas extremidades.
6. Conferir bitrate esperado.
7. Confirmar que a fonte de frames e publica/sintetica/autorizada.

## Comandos host

Depois de capturar saida serial em arquivo texto:

```bash
j1939-sniffer-lab parse-file capture.txt --json reports/capture.json --csv reports/capture.csv
```

Rodar demonstracao sintetica:

```bash
j1939-sniffer-lab simulate --destination 0xFF
```

## Checklist fisico

- [ ] MCP2515 inicializa
- [ ] barramento detectado
- [ ] frame recebido
- [ ] extended ID detectado
- [ ] PGN parseado
- [ ] source correto
- [ ] destination correto quando aplicavel
- [ ] export CSV/JSON funcionando

## Evidencia aceitavel

- Log serial sintetico ou autorizado.
- CSV/JSON gerado pelo parser.
- Foto privada da bancada sem identificadores sensiveis, se necessario.
- Observacao do bitrate e clock MCP2515 usados.

## Troubleshooting

| Sintoma | Possivel causa | Acao |
| --- | --- | --- |
| Sem frames | bitrate incorreto, sem terminacao, fonte silenciosa | confirmar bitrate, 120 ohms e gerador de frames |
| IDs errados | frame padrao em vez de estendido | configurar fonte para extended CAN ID |
| Erros aleatorios | cabos longos, GND ruim, terminacao errada | encurtar cabos e revisar aterramento |
| PGN inesperado | regra PDU1/PDU2 mal interpretada ou frame nao J1939 | validar CAN ID com exemplos publicos |

## Validated vs Not Yet Validated

Validated:

- parser;
- filters;
- tests;
- simulation;
- CI.

Not yet validated:

- physical CAN bus;
- MCP2515 real timing;
- electrical behavior;
- real public test node.

