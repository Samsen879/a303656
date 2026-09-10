# Phase G B31 square-hit source custody

All archives were read from `/mnt/c/Users/Samsen/Downloads` on 2026-09-10.
Names below are the actual Windows filenames; assignment labels are matched by
internal root and content, never inferred from the suffix alone.

| Source ID | Actual ZIP filename | ZIP SHA256 | Members | Internal root | Classification |
|---|---|---|---:|---|---|
| N-v1 | `A303656_B31_N878851_PHASE_G.zip` | `dc8798f4c361f2a87ca2c14f7f686363cbedabebeb10be7e6a00a911132db129` | 5 | `A303656_B31_N878851_PHASE_G` | earlier narrow producer; superseded for accepted content |
| N-v2 | `A303656_B31_N878851_PHASE_G(1).zip` | `c348b1ec241bf6c39ee08bbf6991cb7d33e6de4c558fcdb20602bb7b9c072b81` | 12 | `A303656_B31_N878851_PHASE_G` | canonical task-1 wrapper plus shared v2 core |
| E-v1 | `A303656_B31_EIGHT_INDEX_PHASE_G.zip` | `7ec42c3f04da000d764fc7e171b32c13fee4acf96d8a25c89b1b42f2606e3e9f` | 5 | `A303656_B31_EIGHT_INDEX_PHASE_G` | earlier narrow producer; source for the original criterion audit, superseded by synthesis |
| E-v2 | `A303656_B31_EIGHT_INDEX_PHASE_G(1).zip` | `fe8db9e5c4eda31095d482586f62d38a5f6ea3e90a9257a30d346a7b535763e7` | 12 | `A303656_B31_EIGHT_INDEX_PHASE_G` | canonical task-2 wrapper plus shared v2 core |
| E-v2-duplicate | `A303656_B31_EIGHT_INDEX_PHASE_G(1) (1).zip` | `fe8db9e5c4eda31095d482586f62d38a5f6ea3e90a9257a30d346a7b535763e7` | 12 | `A303656_B31_EIGHT_INDEX_PHASE_G` | byte-identical duplicate of E-v2; receipt only |

Every ZIP passed `unzip -tq`, safe member listing, and its supplied
`SHA256SUMS.txt`. No absolute or traversal path, duplicate member, symlink, or
special file was present. No ZIP is committed.

N-v1 and E-v1 have byte-identical `reference.py`
(`c949e525f50ca10024a4e63d9cd22d43fe6d2e999f49e2b488863f00b7d61839`)
and `certificates/evidence.json`
(`fc4e747cd8a7068fd283341dcc443ea977ed7747084ab5e619d0a6abf680a4df`).
They are task wrappers over one earlier core, not independent implementations.

N-v2 and E-v2 share eight byte-identical core files. Their `results.json`
differ only in task number; their verification logs differ only in elapsed
seconds; their reports are task-specific. The shared core is committed once in
`producer_core/`. The two task-specific reports/results/logs and both original
producer checksum manifests are preserved under `task_wrappers/` and
`source_manifests/`.
