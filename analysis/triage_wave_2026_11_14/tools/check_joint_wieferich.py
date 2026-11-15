#!/usr/bin/env python3
"""Check only the listed Wieferich examples, using exact modular powers."""


def main():
    for p in (11, 1006003, 20771, 40487, 1645333507):
        base3 = pow(3, p - 1, p * p) == 1
        base5 = pow(5, p - 1, p * p) == 1
        expected = (True, False) if p in (11, 1006003) else (False, True)
        if (base3, base5) != expected or p % 4 != 3:
            raise ValueError(f'Wieferich check failed for {p}')
        print(f'{p}: base3={base3}, base5={base5}, p mod 4=3 PASS')
    print('JOINT_WIEFERICH_CHECK_PASS: none of these five examples is joint')
    print('Scope: listed examples only; no exhaustive prime search. A303656: UNRESOLVED')


if __name__ == '__main__':
    main()
