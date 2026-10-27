# Project Explorer submission

## Identity

- **Contribution type:** Builder → Projects.
- **Project name:** ClaimShield AI.
- **Primary tag:** AI (choose the closest available official tag).
- **Additional tags:** Insurance; Infrastructure, if available.
- **Logo:** [512 × 512 PNG](../dist/logo.png), approximately 20 KB.
- **One-liner:** Evidence-grounded insurance claim assessments with independent GenLayer validators and auditable challenges.

## Overview (946 characters)

ClaimShield AI is a GenLayer DApp for evidence-grounded insurance claim assessments. A publisher registers immutable policy versions; claimants submit incident details and commit-pinned public evidence with required SHA-256 hashes. Validators independently retrieve and interpret documents, compare coverage, exclusions and incident-support findings, and record verdicts with exact source quotations and decision hashes. Invalid attachments are tracked individually without vetoing reliable evidence. Claim parties can append counter-evidence for one further review without overwriting history. The public frontend handles signed writes, pending consensus, finality, failures and resumable tracking without MetaMask. Verified Studionet scenarios demonstrate support, exclusions, conflicting reports, missing evidence and recovery. This is a fictional-data development demo, not an insurer, payment authorization or insurance eligibility decision.

## Links

- **Public frontend:** https://claimshield-ai.tinymule33.chatgpt.site
- **GitHub:** https://github.com/amzar1st/ClaimShield-AI
- **Contract:** https://explorer-studio.genlayer.com/address/0x2B50Ecb7BE683A3e08Ee9d89700D28C80ba24B70
- **Deployment transaction:** https://explorer-studio.genlayer.com/transactions/0xd08ed02b204293b10349a9a6f1ffda28523301fac53433690f1e143cd4e82025
- **Evidence report:** https://github.com/amzar1st/ClaimShield-AI/blob/main/docs/evidence.md
- **Live verification:** https://github.com/amzar1st/ClaimShield-AI/blob/main/docs/LIVE_VERIFICATION.md
- **Security/trust model:** https://github.com/amzar1st/ClaimShield-AI/blob/main/docs/security.md
- **Recovery demonstration:** https://explorer-studio.genlayer.com/transactions/0xad6fe6d4342533933059a85061b78b6f53cbace710dd0abb80930c4ada27eeb9
- **Challenge demonstration:** https://explorer-studio.genlayer.com/transactions/0x0968fff8cafcad1e25b01337286dd2661cf12f49828cf09e39d28b86fc4f90ee

## GenLayer integration / reviewer notes

GenLayer is central to assessment: validators independently retrieve hash-committed policy/incident documents, perform natural-language interpretation, and use a custom Equivalence Principle validator to compare decision-critical fields and source fingerprints. The contract derives a bounded verdict and stores immutable review history and decision commitments. The frontend calls the deployed Intelligent Contract through GenLayerJS and requires finalized accepted consensus plus successful execution before confirming a write.

Verified: 48 contract tests, 17 transaction tests, GenVM lint/semantic validation, 15 finalized full-consensus release transactions (including an intentional rejected duplicate), all four verdict categories, a conflicting-evidence challenge, and bad-hash recovery. Six decision commitments were recomputed successfully. Public browser screenshots and machine-readable receipts are in the repository.

Use the submission as a **Studionet development demo**. Evidence is authenticated to a project-controlled publishing namespace, not to a licensed insurer. No payouts, real-person eligibility decisions, private claim data or production readiness are claimed. Studio's built-in account handles deployment/publisher writes; external visitors use separate temporary browser-session accounts without MetaMask.

The contribution is prepared for review; no Project Explorer form has been submitted automatically.
