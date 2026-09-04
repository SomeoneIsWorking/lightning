# Project state

## Comparison baseline

The baseline is GNU lightning 2.2.3 consumed through a host distribution's
optional development package. That workflow is unavailable on some current CI
runners and does not provide one pinned, portfolio-owned source or install
contract across hosts.

| ID | Capability | State | Evidence or exact gap | Related goals |
|---|---|---|---|---|
| S001 | Upstream GNU lightning 2.2.3 lineage and license provenance | verified | `main` descends from upstream tag `lightning-2.2.3` at `815f4221e25cad4b81a17169ba8557aed503f18c`; `upstream` names GNU Savannah and existing GPL/LGPL notices remain. | G001, G003 |
| S002 | Deterministic Python build and install orchestration | verified | `tools/build_lightning.py` validates the pinned Gnulib gitlink, bootstraps, builds, and refuses an incomplete `build/install/<host>` prefix. Tooling unit tests prove cleanup leaves another host profile intact. | G001, G003 |
| S003 | Linux x86-64 static installed-library execution | verified | Fedora 44 Clang build passes all 135 upstream JIT tests, installs `lightning.h`, the x86 header, `liblightning.a`, and package metadata, then the installed-prefix consumer emits and executes a function returning 42. | G001, G002, G003 |
| S004 | Consumer interface without a system `liblightning-dev` package | verified | The installed-prefix consumer finds only `build/install/linux-x86_64/include` and `lib`; the documented shape matches Lightrec's `find_path(lightning.h)` and `find_library(lightning)` inputs. | G001, G003 |
| S005 | Linux x86-64 hosted execution | verified | GitHub Actions run `33890647129` at `f305e50483e9794e8fb0b99fb77d82954a4924e5` passed the full-history, pinned-Gnulib Clang build, all 135 upstream tests, install contract, and emitted-function execution. | G002 |
| S006 | macOS arm64 native execution | missing | No maintained MAP_JIT/write-protection implementation and signed native execution job is present. | G002 |
| S007 | Android arm64-v8a native execution | missing | No API-21 AArch64 register-reservation/executable-memory integration and device or emulator execution job is present. | G002 |
| S008 | Windows x86-64 native execution | missing | No maintained native Windows toolchain, executable-memory contract, or execution job is present. | G002 |

## Current focus

Current focus: none. The Linux dependency boundary is ready for downstream
pinning; additional host work begins only with a real executable-memory test.

## Capability details

### S001 — Upstream lineage

Evidence: the maintained branch has the upstream release commit in
its ancestry and carries all original license files.

### S002 — Build and install orchestration

Evidence: a clean host-profile build is fully owned below `build/`
and missing tools, submodule revisions, or install files cause a nonzero result.

### S003 — Linux native execution

Evidence: the complete upstream suite and an installed-prefix
native-code consumer pass on Linux x86-64.

### S004 — Consumer interface

Evidence: a consumer needs only the documented include and library
directories, without `/usr/include`, `/usr/lib`, or a package-manager-specific
GNU lightning installation.

### S005 — Hosted Linux execution

Evidence: GitHub Actions run `33890647129` at exact revision
`f305e50483e9794e8fb0b99fb77d82954a4924e5` passed the complete native gate.

### S006 — macOS arm64 execution

Missing capability: native macOS arm64 code emission must use the supported JIT
memory policy and pass inside a signed executable context.

### S007 — Android arm64-v8a execution

Missing capability: Android arm64-v8a code must compile and execute on the shared
API-21-or-newer device/emulator path with the required reserved-register ABI.

### S008 — Windows x86-64 execution

Missing capability: a maintained Windows x86-64 library build and native emitted
function test must pass before adding a Windows CI job.
