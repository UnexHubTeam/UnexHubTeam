# Mode A Agent development guide

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Chat Completions API](chat-completions.md) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/agent-development-mode-a.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1. Technical-preview scope](#section-1)
2. [2. Choose an application topology](#section-2)
3. [3. Prepare the application and runtime](#section-3)
4. [4. Use managed credentials safely](#section-4)
5. [5. Integrate the selected topology](#section-5)
6. [6. Design for a temporary data lifecycle](#section-6)
7. [7. Build and verify locally](#section-7)
8. [8. Publish, configure, and test](#section-8)
9. [9. Troubleshooting](#section-9)
10. [10. Technical-preview release checklist](#section-10)
</details>
<!-- DOCS-TOC:END -->


For Agent developers · Mode A / platform-managed dedicated nodes · **Technical preview**

Document version: 0.1 preview · Updated: 2026-09-28

> **Preview notice:** Mode A configuration is available for integration testing, but none of its three application topologies should be described as production-verified yet. Use isolated test data and trusted test users. For the established Cloudflare Containers workflow, see the [Mode B Agent development guide](agent-development-upload.md).

Mode A runs an Agent on a dedicated node managed by the platform operator. You provide the application artifacts and runtime configuration; the platform assigns an available node when a user launches the Agent. A dedicated node is the unit of scheduling, but it is not by itself proof of network isolation, durable storage, or production readiness.

<a id="section-1"></a>
## 1. Technical-preview scope

Mode A does **not** automatically purchase or provision a cloud server, and it is not a Kubernetes deployment workflow. The platform operator must first make a compatible node available. Agent developers do not need node administration access and should not build node-management logic into their applications.

| Area | Current developer-facing boundary |
| --- | --- |
| Compute | One platform-managed dedicated node is assigned to a running session. Availability depends on the operator's node inventory. |
| Architecture | Match the OS and CPU architecture confirmed for the selected node specification. The examples below use `linux/amd64`; do not assume that value without platform confirmation. |
| Topologies | `single`, `split`, and `frontend-package` can be configured, but each remains a technical-preview path pending end-to-end production validation. |
| Public entry | `single` and `split` currently use a direct, unauthenticated HTTP entry. Restrict them to trusted testing. |
| Hosted frontend | `frontend-package` has launch-token and API-proxy components, but the current open flow does not reliably deliver the required client authentication context. Query-string and browser-storage limitations also remain. |
| Images | Use public or otherwise anonymously pullable images unless the platform explicitly confirms private-registry support for your deployment. |
| Persistence | Mode A currently provides no server-side persistence contract. Container files and configuration fields must not be treated as durable storage. |

Select **Mode A** in the platform interface. Do not copy deployment values from old examples or submit undocumented values through an API.

Treat all behavior in this guide as a preview contract that must be rechecked before every release. Platform UI labels and current operator instructions take precedence if they become more restrictive.

<a id="section-2"></a>
## 2. Choose an application topology

Choose the smallest topology that represents your application. Do not switch topologies merely to bypass an entry, authentication, or persistence limitation.

| Topology | Artifacts | Runtime shape | Entry and current limitation |
| --- | --- | --- | --- |
| `single` | One OCI image | One backend container serves both UI and API | Direct unauthenticated HTTP. Trusted integration tests only; not production-ready. |
| `split` | Frontend and backend OCI images | Separate frontend and backend containers; only the configured entry service should be public | Direct unauthenticated HTTP, with no generally verified service-discovery contract for the backend. Trusted integration tests only. |
| `frontend-package` | Frontend package plus one backend OCI image | Platform hosts the frontend and is intended to proxy API requests to the backend | Token and proxy components exist, but the current open flow does not reliably provide the required client authentication context. Query strings, launch context, and browser storage also remain limited. |

Configuration support does not mean that a topology has passed production validation. Before choosing one, confirm that its entry model fits the application:

- Choose `single` when one process can serve the compiled frontend and API on one port.
- Choose `split` only when the frontend and backend genuinely require different images or processes and the platform has confirmed the runtime backend route for the current environment. Each image should keep its own default command where possible.
- Choose `frontend-package` only for preview testing of a platform-hosted static interface. Do not claim that its business API works until the platform confirms the complete open and authentication flow. Never put credentials or server-only configuration in the package.

If a production deployment is required now, stop and ask the platform team which supported mode and entry boundary to use. Do not present a successful preview launch as evidence of production security or reliability.

<a id="section-3"></a>
## 3. Prepare the application and runtime

Confirm the target OS and CPU architecture for the selected node specification before building. The examples below use `linux/amd64`; if the platform confirms another target, replace it consistently. On Apple Silicon or any machine with a different architecture, always set the confirmed target explicitly instead of relying on the local default.

| Item | Requirement |
| --- | --- |
| Listener | Bind to `0.0.0.0`, not container-only `127.0.0.1`. The listening port must match the port entered in the platform. |
| Health check | Provide a lightweight path such as `GET /health` that quickly returns HTTP 200 without calling a model or a slow external dependency. |
| Main process | Run in the foreground, handle `SIGTERM`, and exit within a bounded time. Do not require privileged mode, host networking, or the Docker socket. |
| Command | Prefer the image's tested `ENTRYPOINT` or `CMD`. If the topology requires a command override, enter the exact executable and arguments used in local verification. |
| Permissions | Run the application as a non-root user and grant write access only to explicitly temporary directories. |
| Logs | Write structured logs to stdout/stderr. Include request IDs and stages, but never credentials, complete launch URLs, or sensitive user content. |
| Timeouts | Bound startup and upstream requests. Cancel a model stream when its browser client disconnects. |

Topology-specific configuration:

- For `single`, the image port, application listener, health path, and platform port must all describe the same service. A startup command is currently required.
- For `split`, configure the frontend and backend images and ports independently. Leave a shared command override empty unless the same command is deliberately valid in both images.
- For `frontend-package`, provide a backend image, backend port, health path, and required startup command. The frontend package must be static and contain no runtime secrets.

For `frontend-package`, place `index.html` at the extracted package root, use relative paths for scripts, styles, fonts, and images, and verify the build under a non-root URL path. Do not include `.env` files, credential-bearing source maps, fixed user or Agent IDs, session values, or launch tokens.

The platform form may show `gpu_count=1`. In Mode A this means **one whole schedulable node**, not one physical GPU. The actual accelerator inventory belongs to the selected node specification. Likewise, `storage_gb` is currently a configuration or eligibility value; it does not create a persistent disk or guarantee that data survives a restart.

<a id="section-4"></a>
## 4. Use managed credentials safely

The platform injects these values into the **backend container** when it starts a user session:

| Variable | Meaning | Safe use |
| --- | --- | --- |
| `UNEX_API_KEY` | Managed model credential for the current user–Agent pair | Read on the backend and use unchanged as the API credential. |
| `UNEX_API_BASE_URL` | Versioned model API base paired with the injected key | It already includes `/v1`; read it on the backend and append only the endpoint such as `/chat/completions`. |
| `UNEX_AGENT_ID` | Current Agent identifier | Use with the platform-provided user ID for logical scoping and diagnostics. |
| `UNEX_USER_ID` | Current user identifier | Trust the injected value, not an identifier submitted by the browser. |

`UNEX_API_KEY` and `UNEX_API_BASE_URL` are a pair. Do not replace one with a hard-coded test or production value while keeping the other. Do not prepend an additional key prefix or append a duplicate API-version segment.

Treat the injected key as a long-lived, high-value managed credential. Do not assume that stopping or relaunching one session revokes it. If exposure is suspected, stop testing, notify the platform team, and follow the platform credential-response and rotation process.

Keep all four values on the backend:

- Never compile them into frontend JavaScript, a frontend package, an image layer, or a sample configuration.
- Never return them from an API response or expose them through client-readable environment endpoints.
- Never log request authorization headers or a dump of the complete process environment.
- Do not ask end users to enter a managed key.
- Do not accept a browser-supplied Base URL and then forward the managed key to it.

Minimal Python configuration:

```python
import os

def model_request_config():
    api_key = os.environ.get("UNEX_API_KEY", "").strip()
    base_url = os.environ.get("UNEX_API_BASE_URL", "").rstrip("/")
    agent_id = os.environ.get("UNEX_AGENT_ID", "")
    user_id = os.environ.get("UNEX_USER_ID", "")
    if not api_key or not base_url:
        raise RuntimeError("Managed model credentials are unavailable")
    endpoint = f"{base_url}/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    return endpoint, headers, agent_id, user_id
```

Check required variables at the business request boundary so that `/health` can remain available for runtime health checks. Application-specific non-secret settings, such as a permitted model ID, may use separate environment variables.

<a id="section-5"></a>
## 5. Integrate the selected topology

### `single`

Serve the compiled interface and backend API from the same application and port. Prefer relative, same-origin API paths. Verify `/`, every static asset, the API route, and the health path from the container before uploading the image.

The current public entry is direct unauthenticated HTTP. A platform launch page may control how a user obtains the URL, but it does not make the resulting port private or add transport encryption. Use only synthetic data on an isolated, trusted test network.

### `split`

Build and test the frontend and backend as separate images. Configure the frontend to reach the backend through the runtime route approved by the platform; do not embed a temporary node address or host port in the frontend image. Confirm that only the intended entry service is exposed and that internal API calls reach the correct backend port.

There is no generally verified backend service-discovery address that an Agent may assume. If the platform has not supplied and validated a route for the current environment, stop the integration rather than inventing one. The direct entry has the same unauthenticated HTTP limitation as `single`. Do not use it for public traffic or sensitive data. Avoid a shared command override unless both images were explicitly built to accept it.

### `frontend-package`

Use relative paths beneath the platform-provided application base. The intended backend route is `api/...`, but the current open flow does not reliably provide the client with the authentication context required by the API proxy. Do not add a workaround that reads, stores, or forwards a launch token, and do not claim that business API calls work until the platform supplies and validates a documented client flow.

After that flow is available, retest the complete path and do not assume that arbitrary query parameters reach the backend: current proxy behavior does not reliably preserve the query string. Where the API contract permits, put ordinary non-sensitive request data in a validated path segment or request body. Never use a query parameter for a credential. Test refresh, direct navigation, asset loading, streaming, cancellation, and error responses. Browser storage may be unavailable or fall back to non-durable in-memory behavior; even if cached values remain, the launch and authentication context may not survive a refresh.

For every topology, validate the actual user entry—not only a container-local URL. A healthy container can still have a broken public path, missing assets, an incorrect backend route, or an unhandled stream disconnect.

<a id="section-6"></a>
## 6. Design for a temporary data lifecycle

Mode A currently offers **no server-side persistence guarantee**. Files written inside a container may disappear when a session stops, a node is reclaimed, an image changes, or the runtime is repaired. The `storage_gb` field is not a volume allocation and must not be described to users as cloud storage.

If no approved external data store is configured, design the Agent as stateless:

- Keep transient request state in memory and expect it to vanish at any time.
- Let users export important output during the active session.
- Make retries idempotent where practical and do not depend on a previous container filesystem.
- Do not promise history, recovery, cross-device synchronization, or retention after stop/restart.

Browser `localStorage` may temporarily hold only non-sensitive, disposable UI state such as a theme, layout choice, or draft that the user can afford to lose. It is not platform persistence and may be cleared, blocked, origin-scoped, unavailable, or replaced by non-durable in-memory behavior. With `frontend-package`, a refresh may lose the launch context even if some cached values remain.

Never put any of the following in browser storage, including `localStorage`, `sessionStorage`, or IndexedDB:

- API keys, `Authorization` values, credentials, or complete launch URLs;
- launch/session values or other routing tokens;
- sensitive chat content or personal data;
- records that must be recoverable, shared, audited, or retained.

If the product requires durable server-side data, pause the release until the platform approves an external persistence integration, access model, retention policy, and deletion process. `UNEX_AGENT_ID` and `UNEX_USER_ID` can help namespace approved backend data, but they do not create storage or replace authorization checks.

<a id="section-7"></a>
## 7. Build and verify locally

Use a unique version tag that you do not overwrite, and record the resulting registry digest. Tags can move unless the registry enforces immutability; the digest is the immutable artifact identity. The example below assumes the platform confirmed `linux/amd64`; replace the target if your selected node specification requires another architecture. Repeat the build for each image in a `split` deployment.

```bash
docker buildx build \
  --platform linux/amd64 \
  -t registry.example.com/team/my-agent:0.1.0-preview.1 \
  --load .

docker image inspect registry.example.com/team/my-agent:0.1.0-preview.1 \
  --format '{{.Os}}/{{.Architecture}} user={{.Config.User}}'
```

Run with placeholder credentials against a mock or explicitly approved test endpoint. Never paste a real key into shell history or commit it to a compose file.

```bash
docker run --rm -d \
  --name mode-a-local \
  -p 127.0.0.1:8080:8080 \
  -e UNEX_API_KEY=sk-local-placeholder \
  -e UNEX_API_BASE_URL=http://host.docker.internal:18080/v1 \
  -e UNEX_AGENT_ID=local-agent \
  -e UNEX_USER_ID=local-user \
  registry.example.com/team/my-agent:0.1.0-preview.1

curl --fail --silent http://127.0.0.1:8080/health
docker stop --time 15 mode-a-local
```

Before pushing, verify:

1. The image reports the platform-confirmed OS and architecture (`linux/amd64` in this example), shows an explicit non-root user, and starts with the exact command intended for the platform.
2. The listener uses `0.0.0.0` and the configured port.
3. The health check succeeds without a model call or persistent data.
4. The UI, assets, API, streaming completion, cancellation, and error states work.
5. Missing or mismatched `UNEX_API_KEY` / `UNEX_API_BASE_URL` fails safely without exposing either value.
6. Restarting with an empty filesystem does not corrupt the application.
7. Image layers and logs contain no source credentials, `.env` files, or user data.
8. Each selected topology is tested as a separate artifact set; success in `single` does not validate `split` or `frontend-package`.

<a id="section-8"></a>
## 8. Publish, configure, and test

Push to a registry that the assigned node can read without credentials, unless the platform team has explicitly confirmed a supported private-registry workflow for Mode A.

```bash
docker login registry.example.com
docker push registry.example.com/team/my-agent:0.1.0-preview.1
docker buildx imagetools inspect \
  registry.example.com/team/my-agent:0.1.0-preview.1
```

Record the published `sha256:...` digest. Prefer configuring the immutable digest rather than a mutable tag:

```text
registry.example.com/team/my-agent@sha256:<published-digest>
```

In the Agent deployment form:

1. Select **Mode A** and the intended application topology.
2. Enter each public/pullable image reference and, where supported, pin its digest.
3. Enter the matching container port, health path, and command. For `split`, check both images separately.
4. Select the node specification required by the application. Interpret `gpu_count=1` as one whole node, not one GPU.
5. Treat `storage_gb` only as a preview configuration constraint, not persistence.
6. Save the draft and launch a developer test instance with synthetic data.

During the platform test, verify startup, health, the real user entry, assets, API routing, an actual permitted model request, streaming completion, cancellation, stop, and relaunch. Check that logs contain no injected credentials or sensitive request data.

Most importantly, verify the artifact twice:

- **Before testing:** resolve the configured reference and record the exact digest currently being tested.
- **Before publishing:** confirm that the release still points to the same reviewed and approved digest.

Do not test `:latest` and later publish whatever that tag happens to contain. If any image digest changes, repeat the relevant build, security, topology, and platform tests. Keep the previously approved digest available as a rollback candidate.

<a id="section-9"></a>
## 9. Troubleshooting

| Symptom | Likely cause | What to check |
| --- | --- | --- |
| No Mode A capacity is available | No compatible dedicated node is currently available | Confirm the selected node specification with the platform operator; do not implement cloud provisioning in the Agent. |
| Image pull fails | The image is private, the reference is wrong, or the node cannot reach the registry | Use a public/pullable image unless private access was explicitly enabled; verify the full reference and digest. |
| `exec format error` | The image architecture does not match the assigned node | Confirm the target with the platform, rebuild with the matching `--platform` value, and inspect the final image. |
| Health check times out | Wrong port/path, loopback-only listener, slow startup, or health handler calls an upstream model | Align the listener, form, and image configuration; keep health local and fast. |
| Container starts but the entry fails | Public route, asset base, frontend/backend route, or exposed role is incorrect | Test through the real platform entry and inspect each browser request, not only container-local `/health`. |
| `split` frontend cannot reach the backend | No validated service-discovery route was provided for the current environment | Do not hard-code a node address; stop and ask the platform team for the supported route before continuing. |
| Model request returns 401 | Injected key and Base URL were not kept together, or a version segment was duplicated | Read both values from the same backend environment and construct the endpoint once. |
| `frontend-package` API returns 401 | The current open flow did not provide the client authentication context required by the proxy | Do not expose or persist a launch token as a workaround; keep this topology in preview until the platform confirms the complete flow. |
| Browser can see a managed credential | A backend value was serialized into frontend configuration or logs | Stop the test, remove the exposure, rebuild the artifact, and follow the platform's credential-response process. |
| `frontend-package` loses request parameters | The current proxy path does not reliably preserve query strings | Move non-sensitive request data to the validated body/path where supported and retest; do not use this topology for production. |
| UI state or launch context vanishes on refresh or relaunch | Browser or container state was treated as durable, or the hosted-frontend context was not restored | Make disposable UI state optional. Do not claim refresh recovery or persistence; use only an approved external store for durable data. |
| Tested behavior differs after publishing | A mutable tag resolved to another image | Compare the active digest with the recorded approved digest, roll back, and retest the changed artifact. |
| “1 GPU” expectations do not match the node | `gpu_count=1` was interpreted as physical GPU quantity | Treat it as one whole-node scheduling unit and use the selected node specification for hardware details. |

For direct-entry failures in `single` or `split`, remember that making a port reachable is not a production fix: the current path remains unauthenticated HTTP. Keep testing isolated and escalate entry-boundary requirements to the platform team.

<a id="section-10"></a>
## 10. Technical-preview release checklist

Do not submit a Mode A preview until every applicable item is true:

- [ ] The release is labeled **technical preview** and does not claim that any topology is production-verified.
- [ ] Every runtime image matches the platform-confirmed node OS and architecture, runs as non-root, binds to `0.0.0.0`, and has a fast, model-independent health check.
- [ ] Image, port, health path, entry role, and command agree with the selected topology.
- [ ] Every image is public/pullable, or the platform has explicitly confirmed the required private-registry access.
- [ ] The exact current registry digest was tested, reviewed, and pinned or recorded for publication.
- [ ] `UNEX_API_KEY` and `UNEX_API_BASE_URL` stay paired and backend-only; `UNEX_AGENT_ID` and `UNEX_USER_ID` are read from the injected environment.
- [ ] No secret, launch/session value, or sensitive content is shipped to the browser, stored in browser storage, written to an image layer, or logged.
- [ ] The application assumes no server persistence; `storage_gb` is not described as a durable volume.
- [ ] Browser state is optional and disposable; no refresh-recovery claim is made for `frontend-package` until the platform validates restoration of launch and authentication context.
- [ ] Any required durable store is explicitly approved and includes user isolation, encryption, retention, and deletion behavior.
- [ ] `single` and `split` tests use trusted users and synthetic data because their direct entry is unauthenticated HTTP.
- [ ] `split` uses an explicitly validated platform-provided backend route; no node address or unverified discovery convention is hard-coded.
- [ ] `frontend-package` is not claimed to have a working business API until the platform validates the complete client authentication flow; it does not depend on query-string forwarding and is not represented as production-ready.
- [ ] Startup, real entry routing, assets, API calls, streaming, cancellation, failure handling, stop, and relaunch were checked on the platform.
- [ ] The tested node specification is described accurately: `gpu_count=1` means one whole node, not one GPU.
- [ ] A known-good digest and rollback procedure are recorded.
- [ ] The platform has explicitly approved the selected topology, entry security, registry access, and data design for the intended release audience.

Re-run the checklist whenever an image, command, port, health path, topology, frontend package, node specification, or platform runtime changes. Continue with the [Mode B Agent development guide](agent-development-upload.md) when the Cloudflare Containers workflow better fits the release.

<!-- DOCS-PAGER:START -->

---

[← Previous: openclaw-cn](openclaw-cn.md) · [Documentation home](README.md) · [Next: Mode B Agent development →](agent-development-upload.md)
<!-- DOCS-PAGER:END -->
