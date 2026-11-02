# Archived run directories

These directories hold the working output of earlier reproduction, validation and continuation runs (binaries built from source, logs, chunk outputs and stage-0 replays). They used to sit at the repository root and were moved here unchanged to keep the root readable.

Nothing in the frozen authority, the generated docs, or `scripts/verify_public_repository.py` depends on these paths.

Older records cite them by their original root-level location. In particular, [`REPORT_zh.md`](../../REPORT_zh.md) and some files under [`logs/`](../../logs) refer to paths such as `reproduce_stage0_current/logs/…`. Read any such path as `archive/runs/reproduce_stage0_current/logs/…`. The historical records themselves are left byte-for-byte unchanged.

| Directory | Contents |
|---|---|
| `current_continuation/` | Continuation scan outputs and binaries |
| `final_extension_90m/` | Final 90M-integer extension run |
| `validation_final/` | Final validation run |
| `reproduce_*`, `repro_*`, `current_final_repro_*` | Successive quick, stage-0 and end-to-end replays of `run_reproduce.sh` |

New reproduction runs write to `reproduce_work/` (git-ignored) by default; see [REPRODUCE.md](../../REPRODUCE.md).
