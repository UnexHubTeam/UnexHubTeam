# Changelog

## 2026-09-29

### Mode A

- Updated the English guide and Simplified Chinese translation against the supplied dedicated-node implementation review, retaining the technical-preview status and the need for real-node validation.
- Documented the external-registry submission, digest validation, scanning, platform image copy, configuration, and review sequence; distinguished platform validation from a node's ability to pull and run the approved image.
- Corrected the current `linux/amd64` image requirement and documented the 1024–65535 port constraint for both backend and split-frontend containers.
- Clarified that browser image-archive upload is not available, platform Docker Push should be used only for trusted testing pending scoped credentials, and the Mode A frontend ZIP upload is currently blocked by mode authorization.
- Added the current split-image form and private-registry limitations, user-selected whole-node specifications, and the distinction between uploading an image and billing a running user session.

### Mode B

- Updated the English guide and Simplified Chinese translation to distinguish the current single-image external-registry workflow from planned browser uploads, platform Docker Push, trusted model proxy, and per-user storage.
- Documented all six platform instance types and their resources, version-locked instance selection, the 1024–65535 port range, port-based readiness, optional startup command, and plaintext custom environment variables.
- Clarified the limits of long-lived managed-key injection and documented the existing credential flow only for trusted compatibility testing; marked the future model and storage addresses as unavailable in the current runtime.
- Updated the source-image validation, Cloudflare image transfer, runtime deployment, review, and user-launch sequence, including what to check after leaving the deployment page.

### Shared guidance and navigation

- Clarified that container files and uploaded user files are temporary, browser storage is limited to non-sensitive disposable state, and image-upload staging does not provide a persistent user workspace.
- Updated repository and language-index status descriptions and mode-selection guidance to match the revised capability boundaries.
- Retained direct documentation links, bilingual navigation, and the existing PDF-free layout.
