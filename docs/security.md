# Security and trust boundaries

## Authority and evidence

The constructor locks a publisher repository. Only the administrator may register a policy ID, and registration cannot overwrite an existing version. Namespace control is explicit and self-declared: this is not proof of licensure, identity, insurer consent or factual truth. TLS/GitHub retrieval, full commit addresses and SHA-256 commitments authenticate the bytes within that namespace. A compromised publishing account can create new misleading documents; hashes do not make them true. No independent insurer integration is claimed.

Each fetch permits at most 24,000 bytes; no silent truncation, PDF rendering or OCR. UTF-8 decoding, HTTP failure, empty body and hash mismatch exclude the source. A required failed policy or no valid incident evidence yields INSUFFICIENT_EVIDENCE. An optional bad attachment does not suppress a valid attachment. Independent source fingerprints/statuses must agree among validators. Changing source availability can therefore prevent consensus, which is safer than silently recording inconsistent evidence.

## AI and validator safety

All policy, claim and evidence text is explicitly untrusted data in a structured JSON prompt. It cannot change the locked evaluation rules, grant authority or replace the required schema. No external knowledge is allowed. Exact source quotations are programmatically verified for each non-UNCLEAR finding, with policy citations restricted to policy findings and incident citations restricted to incident evidence. Schema failure yields NEEDS_REVIEW. Critical ambiguities dominate negative findings; missing evidence never becomes an automatic denial.

The custom validator independently re-runs retrieval and assessment and compares coverage, exclusion, incident, derived verdict and source status/hash arrays exactly. It additionally retrieves and checks the leader's citation strings, schema and length bounds. Prose may differ. This extra retrieval costs more than a schema-only validator, but prevents the leader from forging quotes while copying valid classification fields. Validator exceptions or leader errors cause disagreement.

Prompt defenses and multi-model consensus reduce risk; they cannot prove that every quotation semantically entails a conclusion or prevent correlated model mistakes. Exact quote matching proves a quote exists, not its logical sufficiency. No deployment should use the demo to decide real insurance eligibility or payment without human review and substantial additional validation.

## State and access

- Only a claim owner or publisher administrator can assess or challenge that claim.
- Claims lock incident details and initial evidence at creation; they cannot be edited.
- One challenge may append one new source after the initial review; at most four incident sources across both rounds.
- No repeat assessment of a reviewed round, no duplicate claim IDs, no duplicate initial evidence URLs and no reusing a source as counter-evidence.
- Each immutable history entry commits to the complete input snapshot and result with canonical JSON and SHA-256.
- Policy count <=100; total claims <=1,000; paginated claim IDs <=20 per call. A fresh contract is required when capacity is exhausted.
- There is no asynchronous application lock set before AI execution. Failed transactions roll back; a party may retry after network failure. There is no unbounded accepted-review retry feature; insufficient evidence can use the one challenge.
- No funds, payouts, tokens, upgrade authority or administrative deletion is implemented by this contract.

## Browser

All on-chain strings are escaped before HTML insertion. Production scripts are bundled locally. A restrictive CSP blocks arbitrary scripts and form submissions; Google Fonts is the only presentation dependency. No analytics or external AI calls from the browser. The only application RPC is stable Studio. Public read calls request finalized state.

Demo account keys use the official SDK cryptographic generator and stay in session storage. Session storage is accessible to same-origin JavaScript and is unsuitable for real assets or a production custody model. There is no Studio private-key export/import and no wallet impersonation. The public site cannot sign for the deployment administrator. Closing the session can make a user's claims unmodifiable from that account, though still publicly readable. This is disclosed in the UI.

## Privacy

Everything submitted is publicly visible and durable on the network while the development state exists. Never upload personal insurance, financial, identity or medical data. The demo uses only synthetic names and identifiers. Production privacy, data deletion requirements and confidential evidence are outside this release.

## Operational limits

Studionet can reset, external sources can disappear, AI calls can time out and models may disagree. Accepted receipts are provisional. The frontend requires FINALIZED plus SUCCESS execution and verifies post-write state. Tracking timeout remains pending and resumable; it does not resubmit the operation. Real network fees and behavior must be revalidated before moving to another network.

## Source-line selection

The v1.1 assessment prompt supplies numbered source lines. Long lines are divided into consecutive 350-character chunks; no non-empty source content is discarded. Models choose integer line IDs and the contract reconstructs their quotations directly from the verified text. Invalid IDs, booleans masquerading as integers, wrong source categories and unsupported fields fail conservatively. A very short selected line cannot support a non-UNCLEAR finding because quotations must contain at least 12 characters. This reduces transcription-related failures without relaxing source grounding.

## Consensus outcome vs execution

A leader can execute successfully while validators reject its answer. The frontend checks the consensus result as well as finality and execution success. A finalized MAJORITY_DISAGREE receipt is a failure even if the leader receipt says SUCCESS. Intermediate UNDETERMINED/timeouts stay pending until a final outcome or bounded tracking timeout. The UI never treats a leader's successful execution as sufficient consensus evidence.
