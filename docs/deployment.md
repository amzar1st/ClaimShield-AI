# Deployment and reproducibility

## Existing deployment: do not redeploy unchanged code

Network: Studionet, chain 61999, RPC `https://studio.genlayer.com/api`.
Contract: `0x2B50Ecb7BE683A3e08Ee9d89700D28C80ba24B70`.
Deployment sender: `0xf3C059C1495C80c4C94D4eB9eA43FE2fd5D6ED88` (Studio built-in account).
Constructor: `amzar1st/ClaimShield-AI`.
Execution mode: Normal / Full Consensus, not Leader Only.
Contract source SHA-256: `69706ed22f2b96cd53bbf429e4e900264a3547db516b761c93fa95b1724c2234`.

The RPC deployment transaction's decoded contract bytes were compared with `contracts/claimshield.py` and matched exactly. See `dist/deployment.json` and the verification evidence.

## Recreate only after reset or intentional source changes

1. Open https://studio.genlayer.com and use its built-in account selector. No MetaMask is necessary.
2. Upload `contracts/claimshield.py` through the file import control.
3. Choose Run and Debug and Normal (Full Consensus).
4. Enter constructor `publisher_repository = amzar1st/ClaimShield-AI` and deploy once.
5. Inspect the transaction's execution result and wait for FINALIZED + MAJORITY_AGREE + SUCCESS. Record the actual address and hash.
6. Call `register_policy` with ID `CS-MOTOR-2026` and the policy source/hash from `dist/fixtures.json`, using the deployment administrator.
7. Use `open_claim`, `assess`, `challenge`, `assess` with fictional data. Every accepted record must be read back from finalized state.
8. If deploying a changed version, update `dist/deployment.json` deliberately and re-run browser/integration checks. Do not carry forward old proof as evidence for a new address.

The browser website creates its own disposable SDK account. Studio's built-in account does not expose a cross-site injected provider. Never ask a reviewer to export a Studio key into the website.

## Website

```sh
npm ci
npm run build
```

Serve `dist/` over HTTPS. No runtime secrets required. The checked-in Sites hosting manifest declares the public website. Standard static hosting also works without Sites. Google Fonts has system-font fallbacks.

The app's transaction trail persists public receipts/hashes in session storage. A timeout instructs the user to resume tracking; no transaction is automatically resent. Changing origins creates a separate browser account/session.

## Local verification

```sh
python -m pip install -r requirements.txt
python scripts/prepare-sdk.py
python -m pytest -q tests
npm test
genvm-lint check contracts/claimshield.py
```

Direct-mode tests run the official pinned Python SDK in the official genlayer-test harness with mocked web/model responses. They are not full distributed-consensus or WASM execution proof; live Studio transactions provide that separate evidence. The frontend tests simulate receipt transitions; live browser tests exercise actual signing, RPC submission and final-state reads.

## Clean-environment SDK bootstrap

`genlayer-test==0.29.2` requests the old `genvm-universal.tar.xz` asset, which GenVM 0.3 renamed to `genvm-runners-all.tar.xz`. `scripts/prepare-sdk.py` uses the pinned official linter downloader, verifies the official release SHA-256 `e218a1854214681560351051f76fe2b878545cf3409455ef372d57014a88ca67`, and seeds the harness cache. The test session also invokes this idempotently. This fixes clean GitHub Actions runs without modifying SDK behavior or relying on an unstated local cache. The test fixture explicitly selects `v0.3.0-rc7`; the contract still executes its own immutable runner hash.
