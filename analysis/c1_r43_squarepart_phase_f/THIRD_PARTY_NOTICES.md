# Third-party provenance

`ecm_reference.cpp` is a reference C++/GMP port of the Montgomery/Suyama and
second-stage organization in SymPy 1.14.0 `sympy.ntheory.ecm`. It is not the
GMP-ECM program. The originating code is BSD-3-Clause licensed; its installed
license is included as `SYMPY_LICENSE.txt`. Local source identity is recorded
in `environment.json`. Source: https://github.com/sympy/sympy/tree/sympy-1.14.0

Only source code is distributed here. GMP-linked binaries are deliberately
not included. The verifier/generator/checking procedures are same-session,
same-author constructions, not an independent human audit or formalization.
