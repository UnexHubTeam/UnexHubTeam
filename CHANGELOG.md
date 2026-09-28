# Changelog

## 2026-09-28

### API documentation

- Replaced every external Postman/API-collection link across the repository with the corresponding local, language-matched Chat Completions guide.
- Removed the unsupported claim that the local guide lists every public endpoint. Clarified that it documents Chat Completions while protocol, model, route, key, and account support must be confirmed separately.
- Updated the repository home, English and Simplified Chinese documentation indexes, compatibility guides, and all topic-page navigation to use direct repository documentation links.

### Agent developer documentation

- Added a primary English Mode A Agent development guide and a companion Simplified Chinese guide for platform-managed dedicated nodes.
- Marked Mode A and its `single`, `split`, and `frontend-package` topologies as a technical preview with explicit entry-security, service-discovery, authentication-context, query-string, refresh, and production-readiness limits.
- Documented Mode A runtime and artifact requirements, including image architecture, non-root execution, ports, health checks, startup commands, public/pullable images, immutable image digests, platform configuration, testing, troubleshooting, release checks, and rollback preparation.
- Documented the managed backend variables `UNEX_API_KEY`, `UNEX_API_BASE_URL`, `UNEX_AGENT_ID`, and `UNEX_USER_ID`, including credential-pairing, browser-exposure, logging, and rotation requirements.
- Clarified that Mode A currently provides no server-side persistence guarantee: `storage_gb` is not a persistent volume, and browser `localStorage` may hold only non-sensitive, disposable interface state.
- Clarified that `gpu_count=1` represents one whole schedulable node rather than one physical GPU, and that the platform-confirmed node specification determines the actual hardware and image architecture.
- Added Mode A beside Mode B in the repository home, both language indexes, A–Z indexes, cross-links, and Previous/Next navigation.
- Renamed the existing container workflow as Mode B, kept the Mode B content separate, and added direct links between the two mode-specific guides.
- Set the final English portal entry label to **Agent Developer Build and Upload Documentation**, with direct English and Simplified Chinese links for both Mode A and Mode B.

### Verification

- Verified all Markdown files, local links and anchors, and the NAV/TOC/PAGER markers on every topic page. No broken local links, stale Mode A coming-soon claims, real credentials, or internal administration details remain.
