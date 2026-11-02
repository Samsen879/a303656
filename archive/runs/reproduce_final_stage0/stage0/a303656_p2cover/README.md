# A303656 finite p²-cover search bundle

主报告：`REPORT_zh.md`

核心文件：

- `src/verify_pruning.cpp`：独立精确 verifier；
- `cert/gcd_factor_B5000.txt`：完整因子分解证书；
- `output/primes_B5000_verified_by_order.csv`：527 个素数的完整 order/capacity 表；
- `src/method_a_bitset.py`：Method A；
- `src/method_b_lazy.py`：Method B；
- `logs/`：实际运行日志；
- `run_reproduce.sh`：复现入口。
