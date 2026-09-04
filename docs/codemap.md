# Codemap

Architecture: upstream GNU lightning owns portable runtime code emission and
host backends. The maintained-fork layer owns only source provisioning,
build/install orchestration, and executable consumer verification. Lightrec and
title ports remain downstream consumers.

| Subsystem | Responsibility | Current/target location | Entry point | Deep doc |
|---|---|---|---|---|
| Public JIT API | Portable runtime code-emission interface and architecture dispatch | `include/` | `include/lightning.h.in` | upstream info manual sources in `doc/` |
| Host emitters | Architecture-specific lowering, register allocation, and emitted-memory behavior | `lib/` | `lib/lightning.c` | upstream source comments |
| Upstream conformance | GNU lightning instruction and runtime behavior tests | `check/` | `check/Makefile.am` | `README-hacking` |
| Source provisioning | Enforce the exact Gnulib gitlink and run upstream bootstrap | `tools/lightning_tooling/build.py` | `LightningBuilder._ensure_gnulib` | `README` |
| Build layout | Own per-host work, install, smoke paths, and scoped cleanup | `tools/lightning_tooling/layout.py` | `BuildLayout` | `README` |
| Process boundary | Resolve required tools and propagate command failures | `tools/lightning_tooling/process.py` | `require_program`, `run` | `README` |
| Build/install CLI | Configure a static library and publish the documented prefix | `tools/build_lightning.py`, `tools/lightning_tooling/` | `build_lightning.py` | `README` |
| Tooling falsifiers | Prove scoped cleanup and stable host-profile behavior | `tools/tests/` | `tools/tests/test_layout.py` | `docs/project-state.md` |
| Installed consumer evidence | Link only against the installed prefix, emit code, and execute it | `tests/install_contract.c`, `tools/lightning_tooling/verify.py` | `verify_installed_consumer` | `docs/project-state.md` |
| Landing gate | Run policy, tooling tests, upstream tests, installed consumer, and registries | `tools/verify.py` | `main` | `docs/project-state.md` |

## Where does X go?

| Capability | Owner |
|---|---|
| New portable JIT instruction or architecture backend | upstream-owned `include/` and `lib/`, kept as a focused upstreamable commit |
| macOS or Android executable-memory correction | architecture/runtime owner in `lib/`, with native execution evidence in `tests/` |
| Build directory or dependency provisioning policy | `tools/lightning_tooling/` |
| PSX guest decoding, timing, or fallback | downstream Lightrec/PSXPort, never this repository |
| Title-specific native override | consuming title runtime, never GNU lightning |
