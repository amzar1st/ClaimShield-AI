# ClaimShield AI

**Evidence before verdicts.** ClaimShield AI is a GenLayer DApp for independently assessing documentary support for fictional motor-insurance claims. It locks policy versions, verifies incident evidence against SHA-256 commitments, and records source-grounded assessments and a bounded challenge history.

- Website: https://claimshield-ai.tinymule33.chatgpt.site
- Network: stable Studionet, chain ID **61999**
- Intelligent Contract: [`0x2B50Ecb7BE683A3e08Ee9d89700D28C80ba24B70`](https://explorer-studio.genlayer.com/address/0x2B50Ecb7BE683A3e08Ee9d89700D28C80ba24B70)
- Deployment: [`0xd08ed02b204293b10349a9a6f1ffda28523301fac53433690f1e143cd4e82025`](https://explorer-studio.genlayer.com/transactions/0xd08ed02b204293b10349a9a6f1ffda28523301fac53433690f1e143cd4e82025)
- [Verification evidence](docs/evidence.md) · [Security and trust boundaries](docs/security.md) · [Deployment](docs/deployment.md) · [Submission details](docs/submission.md)

## The trust problem

A claim examiner and claimant can disagree about which policy version applies, what the incident documents establish, and why a claim was judged supported or unsupported. An ordinary AI response gives neither party a shared, independently checked record. ClaimShield binds a policy and source bytes to a reproducible input commitment, uses GenLayer validators to independently interpret the same evidence, and preserves the reasoning and quoted sources for review.

This is a **public development demonstration**, not an insurer, payment processor, fraud determination, insurance eligibility engine, legal opinion or coverage guarantee. All example policies, identities and reports are fictional. Never submit personal or confidential claim data. Repository ownership proves control of a publishing namespace, not insurer authority or truth of an incident.

## Try it

1. Open the website and inspect the registered policy and recorded claims without connecting a wallet.
2. Create a temporary **demo account**. No MetaMask is required. Its key remains in browser session storage; do not send real assets to it. Reloading the same tab preserves it; closing the session may lose it.
3. Choose accidental collision, excluded racing or hash mismatch. Inspect the pinned evidence JSON and acknowledge the fictional-data notice.
4. Submit a uniquely identified claim. The transaction trail shows pending consensus, provisional acceptance, finality and execution failures separately.
5. Once finalized, run the validator assessment. Inspect coverage, exclusion and incident findings, quotations, per-source checks and decision hashes.
6. Submit the supplied conflicting evidence as a challenge, then assess again. The original review remains in `get_history`; only one challenge is permitted.
7. If tracking times out or the page reloads, resume the **same transaction hash** instead of resubmitting.

The deployment and publisher transactions use **GenLayer Studio's built-in account**. Studio does not inject that wallet into arbitrary external sites. The website therefore uses a separate disposable local SDK account for visitors, rather than requesting a Studio private key or adding a MetaMask dependency. Publisher administration remains in Studio.

## Contract workflow

`register_policy` (administrator only, immutable version) → `open_claim` → `assess` → optional `challenge` with new evidence → second `assess`.

The constructor locks a single publisher GitHub repository. Sources must use exact `https://raw.githubusercontent.com/<publisher>/<40-character-commit>/<path>` URLs plus a required SHA-256 digest. Policy registration is controlled by the deployment administrator. Claim evidence must come from the same namespace; arbitrary web URLs, branches, query strings and path traversal are rejected.

Each validator independently fetches sources and evaluates three bounded findings: `coverage`, `exclusion`, `incident` (`YES`, `NO`, `UNCLEAR`). A custom equivalence check requires exact agreement on these critical findings, the derived verdict and every source status/hash. Models select numbered source lines; the contract reconstructs exact quotations and validators independently check them against source bytes. Natural-language reasoning can differ. Consensus disagreement is a network transaction failure, never quietly converted into an approved claim.

| Verdict | Meaning |
| --- | --- |
| `SUPPORTED` | All required findings support the fictional claim and no exclusion applies. |
| `NOT_SUPPORTED` | Reliable documents establish a coverage failure, exclusion or incident contradiction, with no unresolved critical finding. |
| `NEEDS_REVIEW` | A critical finding is ambiguous, conflicting, or model output fails citation/schema checks. |
| `INSUFFICIENT_EVIDENCE` | The required policy or all submitted incident sources fail retrieval/integrity checks. |

A failed optional attachment is recorded individually and does not veto reliable evidence. Missing evidence is not an automatic denial. The contract never transfers funds. Assessment completion is not an irreversible claims settlement; a challenge adds a review round.

## Development

Requirements: Python 3.12+, Node 20+ (tested on Node 24).

```sh
python -m pip install -r requirements.txt
npm ci
python -m pytest -q tests
npm test
npm run build
genvm-lint check contracts/claimshield.py
```

Contract runner is pinned to `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`, with ABI `v0.2.16`, matching the deployed stable Studio environment. GenVM validation also reports a newer runner available; upgrading requires compatibility testing, not silently changing the deployed source. GenLayerJS is pinned to stable `1.1.8`; the Consensus v0.6 preview uses a different SDK/network and is not this deployment.

`dist/` is a self-contained static website. Build from `frontend/app.js` with esbuild. `dist/deployment.json` identifies the verified contract; `dist/fixtures.json` pins the published synthetic source files. No backend API key, private wallet key, AI API key or hidden central adjudication server is required.

## Repository layout

- `contracts/claimshield.py`: deployed Intelligent Contract, all assessment logic and persistent history.
- `frontend/`: SDK integration and independently tested transaction lifecycle.
- `dist/`: deployable website, logo and public configuration.
- `fixtures/`: fictional policy, incident reports and conflicting evidence.
- `tests/`: direct SDK behavioral, adversarial validator and frontend receipt tests.
- `docs/`: verification, deployment, limitations, source references and submission details.

## Adoption path

A real pilot needs verified insurer/publisher onboarding, authenticated examiner attestations, privacy-preserving evidence access, complete policy schedules and endorsements, identity authorization, domain-specific benchmarks, formal governance and a human escalation process. Public UTF-8 GitHub fixtures deliberately avoid pretending these problems are solved. Studionet is temporary development infrastructure and may reset; this deployment is not a persistent production service.

## Official references

Documentation checked 26 October 2026:

- [Networks](https://docs.genlayer.com/developers/networks)
- [Equivalence Principle and independent validators](https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle)
- [Web access](https://docs.genlayer.com/developers/intelligent-contracts/features/web-access)
- [Development and testing](https://docs.genlayer.com/developers/intelligent-contracts/tooling-setup)
- [GenLayerJS](https://docs.genlayer.com/api-references/genlayer-js)

MIT licensed. No live insurance service or insurer affiliation is claimed.
