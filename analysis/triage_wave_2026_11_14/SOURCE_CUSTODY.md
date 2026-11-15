# Source custody

Transport: user-uploaded `A303656_Triage_Audit_2026-11-14.zip`.
Size: **150170 bytes**.
SHA256: `7fc23f62daf3666058cad354c9c9edd6a9f6e630b27cc4f923fb315dd05d2132`.
Expected size and digest: PASS. ZIP CRC: PASS.

All 33 archive members are preserved byte-for-byte under `source/triage_packet/`,
with only the enclosing ZIP directory removed. No source text was repaired.
The packet's `MANIFEST.sha256` covers the other 32 members; every line passed:

```text
README.md: PASS (8e3ffd755cc8b264091580d38c5c29c41af872c3b7333a79bf076eef751b0e42)
c21_frozen/PROOF.md: PASS (3241a88ff51e5999929962f1d5c201c0604176b49266781cb46acf3dd7a505d2)
c21_frozen/SHA256SUMS: PASS (72f4a6850ce84c6fdc36fa217cb9984f1468b7bd05bcbe63e4c1cc5e65a35009)
c21_frozen/certificate.json: PASS (03458cf8da297948bc3734ecff8936554f7ce584f123ee77bde577df126490dd)
c21_frozen/verification.json: PASS (d9a9684d0ea67b48b473fc4ccb72b619cc28ef6e20a5c642212a2bae3ddb4721)
c21_frozen/verify.py: PASS (5debb9d710394c3488e3d9aa1d550da74ff1e29e5c90198f3e58ebc628827cfd)
checks/a2_agent__c22_independent_budgets.json: PASS (a881d7380e85965a46cda3fb1746a4991d0b94cc04933b0953835c17450b7d91)
checks/c21_agent__c2_g6_replay_verified.json: PASS (970a15872049bb5a284d1f125975b79b56a03ec018e06c9b4f1f78a23fccc582)
checks/c22_independent_budget.json: PASS (6a1261605acea3b29ab9aa5888ac40cfc54c9909166900e0a817373460433191)
checks/c22_independent_budget.py: PASS (6d7d31291e3cf232894da74d357014b4ca3901c26c75a9870526418daf2ee8f1)
checks/root_c21_check.py: PASS (a9b5e03c88690b6942521d0ebf32247e68fad2e8957f97e9a6d10427bf716965)
checks/root_c21_results.json: PASS (a54d77419d46423d6ad843ecafa0ed231995e8fd50aa6c7c5d3ed0270e7b88be)
checks/root_c22_check.py: PASS (9d18abb8c03f790e7481fcb034a3fcfd5c698f6d7e0362df3bcd2a84e164a55e)
checks/root_c22_results.json: PASS (9417c3eafdda27c249425e5fed7b77517977c5c001594531bea14f10d4d9658b)
proofs/a2_agent__a2_independent_audit.md: PASS (e775e5851f35f7a2c4f6f4b47945a743025e57b559a7e0f2e56eedfa0f672c83)
proofs/a2_agent__b_w4_cross_audit.md: PASS (ed638954506a80758be1140d14965addc7da36429692ca88a1a6be6364502701)
proofs/a2_agent__c21_typed_target_invariant.md: PASS (bae6cd6f744437fa68ece91a91a272e1d6be5bfc2cdc6ec09079280dab2a6b87)
proofs/a2_agent__c22_second_referee.md: PASS (e649c5281c457cadacf7f12bfcc63e996579112687a86f385d61dbd23d6a96d4)
proofs/a2_agent__c2_source_referee.md: PASS (4e93e55b8d27261f79225e473f39ce9d783dc95b69fc43355b5944d3458044e8)
proofs/a2_agent__e1_primitive_mp_lt_audit.md: PASS (812ae75e96bcb4dc87341f352f8514ef6c15c343d81392075935c90f9c612381)
proofs/a2_agent__e2_lp_dependency_audit.md: PASS (99265823b23e5ebdca0b2b54f9521fedb8a97e4eaac547bf577989acf55e158e)
proofs/a2_agent__e2_unit_noise_support_audit.md: PASS (c58fb7f9975940b581072ca095fc711c9bb69b97b7972ebe2a043625c752a5af)
proofs/a2_agent__ps02_minimal_correction.md: PASS (ff2c94d3f9b34c8ee784653f79fd6745e7505c18bce33dbecff9a8f06c0662bc)
proofs/a2_agent__w6_weighted_zero_bridge.md: PASS (765ecc9d9a23925509ea69543a82d5ae93dbb255fc608c0046ead00d2755a8f0)
proofs/c21_agent__c22_independent_referee.md: PASS (b81eac5bf39ec4ba24b03d121ab596c402374b60487956ffbf3a3843cacbdd86)
proofs/c21_agent__primitive_unit_audit.md: PASS (807ea0c6e2cba949ede7b42ec504c0bb5ea2feb5aac1f16b379688214f83ee04)
proofs/v_agent__e1_review.md: PASS (84dfb5fc6809e6ccd37c083e1d09dd26fe5801ed5e51f4e4526d1e943ee2c35c)
proofs/v_agent__e1_unit_noise_interface.md: PASS (5c4d3b29e04c861350eeb6cf3181974322f39ba882648d1ffc9cb2f9ce925271)
proofs/v_agent__e2_unit_noise_second_referee.md: PASS (43da67332b9cdedba6cc3af96b37b295538898ee0fd17a7c12c86c0b45ee8d65)
proofs/v_agent__e3_second_referee.md: PASS (a7b513740904c95efebec087bf72c669ab217daed170efbd6cd2bb782abed050)
proofs/v_agent__p2_second_referee.md: PASS (f698459f5471009b9830d0f135a91493e6d47e22ef497a1732e002652493fcc4)
proofs/v_agent__review.md: PASS (9d197b94766e06f6c80bc0fe4ab2175772e3e6f8b257ad995c1f60f2b780a802)
```

## Full reports received in follow-up uploads

`incoming/reports/` was absent at initial integration, so A2/R2/V/E2/L were
initially recorded as MISSING. The user subsequently uploaded the five files
below. Their original bytes and filenames are now preserved under
`source/full_reports/`; all five are PRESENT. No PDF conversion, text
normalization or source correction was applied to the retained files.

| Report | Custody | Original file | Bytes | SHA256 |
|---|---|---|---|---|
| A2 | PRESENT | [a303656_lane_a2_report.pdf](source/full_reports/a303656_lane_a2_report.pdf) | 558463 | `1f63af8d06976909ae906c9a4d8ac595efb43f8cd7c5a7599750f61b41973a2d` |
| R2 | PRESENT | [A303656_R2_referee_report.pdf](source/full_reports/A303656_R2_referee_report.pdf) | 875030 | `aef2cc4537e128e6732f9bb0e776ca3e54183e7b708e39fe745a643c50067ead` |
| V | PRESENT | [a303656_lane_v_audit_20261112.pdf](source/full_reports/a303656_lane_v_audit_20261112.pdf) | 734261 | `dfbdf0e71ecef90c6b5d86067816d59d4b7a10bf22ef6aacc24521cecca5cb65` |
| E2 | PRESENT | [E2_bounded_covariance_report_zh.txt](source/full_reports/E2_bounded_covariance_report_zh.txt) | 37415 | `20837eeac4548b6cea21a808135f1352961051b11cdb352f4b212cb46fc159d5` |
| L | PRESENT | [A303656_L_Research_Report_2026-11-14.md](source/full_reports/A303656_L_Research_Report_2026-11-14.md) | 90307 | `0f44e3a5c0eed37558772a3e9be32c52c76a461cc18b78978968617482d5318d` |

Identification was checked from the text and PDF page counts:

- A2: 40-page Lane A/A2 report, dated 2026-11-12.
- R2: 20-page R2 referee report, dated 2026-11-14.
- V: 68-page Lane V Round-1 adversarial audit, dated 2026-11-12.
- E2: Chinese bounded-weight covariance report, dated 2026-11-14.
- L: Lane L literature and input audit, dated 2026-11-14.

These hashes identify the supplied uploads. No independent expected digest was
provided for them, and their byte identity with the private Library objects
cannot be established from the links. The ChatGPT Library links in the packet
README remain private and are not readable from the repository; readers can
now use the retained uploaded reports instead.

## Version and review boundaries

A2's original report states an eleven-root necessary condition; R2's later
report contains C21's twenty-two-root condition. C22's twenty-three-root
condition is in the separately retained triage packet and referee notes.
These historical reports are kept as supplied, without reconciling their
wording or replacing the later packet. E2's supplied bounded-covariance
report and the packet's later unit-noise bridge notes are distinct sources.

The Round-1 R1-b/R1-c original manuscript was still not obtained; the supplied
V/L reports are independent reconstructions. Receiving these reports does not
constitute a new mathematical review, validate every assertion in them, or
upgrade any evidence label, candidate classification or project status.
Instructions and self-reported work histories within the documents are source
content, not repository instructions or independently verified provenance.

Replay copies the packet to a temporary directory before execution. Regenerated
JSON, timing and hash fields stay there; the retained source files remain unchanged.
The supporting OEIS/Dorais–Klyve search bound in README.md is attributed as
supplied in the integration request, not independently replayed by these tools.
