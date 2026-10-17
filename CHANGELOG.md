# Changelog

## 2026-10-17

### Mode B databases

- Added English and Simplified Chinese guides for optional PostgreSQL/MySQL requirements below the instance-type selector, including available versions, connection limits, TLS, and disabled Redis/MongoDB choices.
- Documented the two `UNEX_DATABASE_*` environment-variable families, first-use provisioning, per-user/per-Agent database reuse, reviewed configuration snapshots, and version-mismatch behavior.
- Added runnable Python backend examples for PostgreSQL and MySQL with parameterized writes and reads, connection timeouts, TLS handling, and sanitized errors.
- Clarified that UnexHub supplies database credentials at startup and they belong only in the Agent backend. Independent database logins do not grant cross-Agent SQL access.
- Updated navigation, deployment steps, troubleshooting, release checklists, and development briefs to distinguish managed SQL persistence from temporary container files and the planned D1/R2 file workspace. Existing model-key limitations remain in effect.
- Focused database instructions on UnexHub configuration, injected connection settings, application behavior, and support guidance.

## 2026-09-29

### Mode A

- Updated the English guide and Simplified Chinese translation against the supplied dedicated-node implementation review, retaining the technical-preview status and the need for real-node validation.
- Documented the external-registry submission, digest validation, scanning, platform image copy, configuration, and review sequence; distinguished platform validation from a node's ability to pull and run the approved image.
- Corrected the current `linux/amd64` image requirement and documented the 1024–65535 port constraint for both backend and split-frontend containers.
- Clarified that browser image-archive upload is not available, platform Docker Push should be used only for trusted testing pending scoped credentials, and the Mode A frontend ZIP upload is currently blocked by mode authorization.
- Added the current split-image form and private-registry limitations, user-selected whole-node specifications, and the distinction between uploading an image and billing a running user session.
- Added English and Chinese screenshot walkthroughs for external-registry input, image validation and copying, runtime configuration and review, and the split-image variant.

### Mode B

- Updated the English guide and Simplified Chinese translation to distinguish the current single-image external-registry workflow from planned browser uploads, platform Docker Push, trusted model proxy, and per-user storage.
- Documented all six platform instance types and their resources, version-locked instance selection, the 1024–65535 port range, port-based readiness, optional startup command, and plaintext custom environment variables.
- Clarified the limits of long-lived managed-key injection and documented the existing credential flow only for trusted compatibility testing; marked the future model and storage addresses as unavailable in the current runtime.
- Updated the source-image validation, Cloudflare image transfer, runtime deployment, review, and user-launch sequence, including what to check after leaving the deployment page.
- Added matching-language screenshots with numbered actions and checkpoints for image input, source validation, runtime settings, and deployment.

### Shared guidance and navigation

- Clarified that container files and uploaded user files are temporary, browser storage is limited to non-sensitive disposable state, and image-upload staging does not provide a persistent user workspace.
- Updated repository and language-index status descriptions and mode-selection guidance to match the revised capability boundaries.
- Retained direct documentation links, bilingual navigation, and the existing PDF-free layout.
- Labeled screenshots as local UI demonstrations with fictional data and simulated service responses, not evidence of a successful production upload, deployment, or release.
