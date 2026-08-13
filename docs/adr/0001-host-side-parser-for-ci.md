# ADR 0001: Host-Side Parser for CI

## Status

Accepted.

## Context

CAN/J1939 labs usually require physical transceivers, a wired bus and an embedded toolchain. Public CI should still validate the most important parsing and analysis behavior.

## Decision

The project validates J1939 parsing, filtering, statistics and export through a Python host-side parser using synthetic frames. Firmware remains in the repository as public bench code and architecture documentation.

## Consequences

- The project is demonstrable without CAN hardware.
- Parser behavior is testable and reproducible.
- Hardware validation remains explicit future work.

