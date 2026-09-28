# Changelog

## 2026-09-28

- Added primary English and companion Simplified Chinese Mode A dedicated-node development documentation as a technical preview, with direct navigation alongside Mode B and explicit production-readiness limits.
- Replaced every external API collection link with a direct, language-matched Chat Completions documentation link.
- Removed unsupported “all public endpoints” wording and clarified the scope of the local API guide.
- Regenerated the Chinese Mode B PDF so its API link opens the corresponding GitHub documentation page directly.

## 2026-09-24

- Reorganized the repository into a task-oriented documentation portal with quick-find tables, category navigation, per-page contents, and Previous/Next links.
- Added public API and UNEXHub Agent Developer Center entries to topic-page navigation.
- Marked the original Agent guide as Mode B only; Mode A is now covered by the 2026-09-28 technical-preview documentation with known production gaps.
- Removed obsolete third-party service references and retained direct official or project documentation where available.
- Added the Mode B Agent development and upload guide in English and Simplified Chinese, covering container requirements, Alibaba Cloud Registry push, platform configuration, release checks, and troubleshooting.
- Added a current Chinese PDF edition generated from the guide and linked the download from the repository home and both language indexes.
- Documented managed key/Base URL pairing, session-aware routing, SSE error handling, and the SOL Agent 1.0.4 Base URL override, including the scope of the previously verified connection.
- Clarified that Agents without backend persistence may temporarily use browser `localStorage` only for non-sensitive, disposable frontend state, with reset and security requirements.
- Added English UI reference images for every screenshot used by the primary English documentation while retaining the original Chinese images for the companion translation.

## 2026-09-23

- Set English as the primary documentation language and retained Simplified Chinese as a companion translation.
- Updated UNEXHub branding, moved website and console links to `https://unexhub.ai/`, and updated API Base URLs to `https://api.unexhub.ai/` while retaining protocol-specific paths such as `/v1`.
- Added primary English setup guides with corresponding Simplified Chinese translations for Claude Code, Codex, VS Code, openclaw-cn, Cursor, Windsurf, CC Switch, CC MAX, Aider, Chatbox, and Cherry Studio.
- Retained Chatbox and Cherry Studio, expanded FAQ, and kept the original key, routing, model-call, and billing workflows.
- Added a protocol compatibility reference, current provider configuration examples, and links to source documentation.
- Grouped navigation to match the requested tutorial categories. Messages, Responses, CC MAX, and native editor support are explicitly qualified where unconfirmed.
- Replaced reliance on the unavailable API reference with the compatibility page.

## 2026-09-22

- Created English GitHub guides with corresponding Simplified Chinese translations and UNEXHub interface screenshots.
