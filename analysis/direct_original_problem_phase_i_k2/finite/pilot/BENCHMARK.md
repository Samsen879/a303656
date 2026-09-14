# Exact scanner design comparison

Widths are exactly 2^16. Design A classifies each shifted residual segment independently. Design B merges overlapping residual intervals and reuses classifications. Both use a bad-prime segmented sieve; the independent reference instead fully trial-factors every residual, including good primes. Merging is the selected production optimization; no probabilistic classification is used.

| Scale | Design | Seconds | Peak RSS KiB | Shifts | Induced segments | Merged segments | Classified residuals | n/sec |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 100000000 | per_shift | 0.185529 | 77812 | 204 | 204 | 204 | 13369344 | 353239 |
| 100000000 | merged | 0.088927 | 77812 | 204 | 204 | 32 | 2979234 | 736965 |
| 10000000000 | per_shift | 0.306141 | 77812 | 315 | 315 | 315 | 20643840 | 214071 |
| 10000000000 | merged | 0.163542 | 77812 | 315 | 315 | 85 | 6942282 | 400729 |
| 1000000000000 | per_shift | 0.631005 | 77812 | 466 | 466 | 466 | 30539776 | 103860 |
| 1000000000000 | merged | 0.364891 | 77812 | 466 | 466 | 171 | 13146142 | 179604 |

All complete binary arrays (R, active, zero, bulk, A23, minimum residual, success bitsets) agreed between designs, and each scale passed independent full factorization of 100 deterministic controls. RSS is getrusage process peak, a conservative observed value potentially including inherited fork footprint; it is not a tightly isolated allocator estimate. Internal scanner time excludes compilation and controller/factor-reference overhead. Full production-plus-evidence time is separately reported.

Admission used 16× benchmark scanner time +16× reference-control time +120 seconds reserve. A/B/C all fit the original 1800-second deadline. Full kernel and metadata are retained. g++ -O3 -std=c++17; compiler details in environment.txt.
