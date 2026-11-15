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

## Missing full reports

`incoming/reports/` was absent during integration. No full-report bytes were
available to copy into `source/full_reports/`:

| Report | Custody |
|---|---|
| A2 | MISSING |
| R2 | MISSING |
| V | MISSING |
| E2 | MISSING |
| L | MISSING |

The ChatGPT Library links in the packet README are private and not readable
from the repository. Included referee notes are not substitutes for missing
full reports. The Round-1 R1-b/R1-c original manuscript was not obtained;
V/L are independent reconstructions. No missing text was reconstructed from memory.

Replay copies the packet to a temporary directory before execution. Regenerated
JSON, timing and hash fields stay there; the retained source files remain unchanged.
The supporting OEIS/Dorais–Klyve search bound in README.md is attributed as
supplied in the integration request, not independently replayed by these tools.
