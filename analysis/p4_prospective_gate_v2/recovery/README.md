# Gate V2 forensic recovery

This directory contains read-only forensic builders, a fail-closed semantic verifier,
and corruption/metamorphic tests. It must not invoke any evaluator. Generated results
remain `PARTIAL` and `NOT_ESTABLISHED` whenever historical execution exposure cannot
be recovered.

The nine gate names and ordering are frozen in `common_v2.py`. V2.3 and V2.4 are
separate. V2.9 cannot pass before independent audit of the exported bundle.
