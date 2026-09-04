# Project goals

## G001 — Portable GNU lightning dependency

Provide ports with a maintained, reproducible GNU lightning source and install
contract instead of depending on runner- or distribution-specific development
packages.

Success conditions:

- a clean checkout builds and installs the pinned source through Python tooling;
- consumers receive headers, a static library, and package metadata from one
  predictable prefix under `build/`;
- a program linked only against that prefix emits and executes native code.

Constraints and non-goals:

- preserve upstream history and the GNU lightning 2.2.3 provenance;
- preserve GNU GPL/LGPL notices and downstream source obligations;
- this repository owns the code-emission dependency, not PSX guest semantics or
  Lightrec's block policy.

Related state: S001, S002, S003, S004.

## G002 — Proven maintained host coverage

Make each claimed host a real native-code execution boundary, including its
executable-memory and calling-convention requirements.

Success conditions:

- Linux x86-64, macOS arm64, Android arm64-v8a, and any claimed Windows target
  each compile, link, emit, and execute code in their actual environment;
- hosted jobs exist only after that platform boundary is implemented and
  executable without copyrighted assets;
- unsupported platforms remain explicitly missing rather than represented by a
  policy-only green job.

Constraints and non-goals:

- cross-compilation alone is not execution evidence;
- no writable-and-executable workaround may replace a platform's supported JIT
  memory policy;
- platform enablement must be reusable by Lightrec and future consumers rather
  than copied into a title repository.

Related state: S004, S005, S006, S007.

## G003 — Reviewable upstream maintenance

Keep local platform corrections small, tested, attributable, and suitable for
upstreaming while retaining the full GNU project lineage.

Success conditions:

- `upstream` identifies GNU Savannah and release/tag provenance stays recorded;
- third-party source changes are isolated from portfolio build orchestration;
- verification prints denominators and fails on missing sources, tools, install
  outputs, or executable-code behavior.

Constraints and non-goals:

- do not fork GNU lightning into PSXPort or Lightrec;
- do not add generated guest-code corpora or offline guest translation;
- do not claim a platform from compile-only evidence.

Related state: S001, S002, S003, S007.
