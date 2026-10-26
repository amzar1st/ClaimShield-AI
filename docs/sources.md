# Source and evidence provenance

Documentation checked 26 October 2026. Official references are linked in the README.

Stable Studio currently runs GenVM ABI v0.2.16 with the pinned Python runner used by the bundled Studio template. The installed stable SDK 1.1.8 defines Studionet as chain 61999. It differs from the newer v0.123 / Consensus v0.6 preview documented for Studio-dev (61997); no preview network substitution was made.

All demonstration policy/incident material is authored synthetic text, published in this repository. `dist/fixtures.json` points to a content-addressed Git commit and SHA-256 digests of each exact UTF-8 file. Source content is retrieved live by the validators from GitHub, not sent as an unverified frontend claim attachment. It is authoritative only for the project's fictional namespace. No genuine insurer, police, medical, claimant identity or live incident-data feed is integrated.

The project intentionally uses documentary insurance interpretation rather than pretending a weather feed alone proves a non-parametric insurance claim. Production integration requires explicit insurer authority, full policy schedules, privacy and an independent incident-authentication process.

Official Studio backend reference consulted while diagnosing stable RPC behavior: https://github.com/genlayerlabs/genlayer-studio/blob/main/backend/protocol_rpc/endpoints.py . Network simulations and diagnostics are distinct from full-consensus deployment evidence.
