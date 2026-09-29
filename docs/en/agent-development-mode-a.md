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

Document version: 0.1 preview · Updated: 2026-09-29

> **Preview notice:** Mode A has deployment configuration, image validation, scheduling, and billing components, but none of its three application topologies is production-verified. The `frontend-package` ZIP control is currently blocked for Mode A, so its upload flow cannot be completed. Use isolated test data and trusted test users. The [Mode B Agent development guide](agent-development-upload.md) covers the Cloudflare Containers workflow; that workflow also has credential-safety limitations and is not a blanket production-safety guarantee.

Mode A runs an Agent on a dedicated node managed by the platform operator. You provide the application artifacts and runtime configuration; the platform assigns an available node when a user launches the Agent. A dedicated node is the unit of scheduling, but it is not by itself proof of network isolation, durable storage, or production readiness.

<a id="section-1"></a>
## 1. Technical-preview scope

Mode A does **not** automatically purchase or provision a cloud server, and it is not a Kubernetes deployment workflow. The platform must first make a compatible node available and independently deliver and validate the runtime that runs on it. The presence of platform UI or APIs does not mean a working node runtime is automatically available. Agent developers do not need node administration access and should not build node-management logic into their applications.

| Area | Current developer-facing boundary |
| --- | --- |
| Compute | One platform-managed dedicated node is assigned to a running session. Availability depends on the operator's node inventory. |
| Architecture | The current image upload and validation pipeline requires `linux/amd64`. Confirm that the selected node supports this image target and meets the application's hardware requirements. |
| Topologies | `single`, `split`, and `frontend-package` appear in configuration. All remain technical preview; `frontend-package` cannot currently complete its ZIP upload. |
| Public entry | `single` and `split` currently use a direct, unauthenticated HTTP entry. Restrict them to trusted testing. |
| Hosted frontend | Current mode authorization blocks Mode A's frontend ZIP upload. Client authentication, query-string forwarding, and refresh recovery also remain incomplete. |
| External Registry | An existing image-reference route supports public images and platform-stored, encrypted read-only credentials for private images. Successful platform validation does not prove that the node can pull the image. |
| Platform Registry | Docker Push to Tencent Cloud Container Registry (TCR) appears only when configured by the platform. Use it only for trusted testing until appropriately scoped write credentials are available. |
| Browser image upload | Browser upload of OCI or `docker save` TAR archives is not available. A source ZIP or `docker export` filesystem TAR is not a runnable OCI image. |
| Persistence | Mode A currently provides no server-side persistence contract. Container files and configuration fields must not be treated as durable storage. |

Select **Mode A** in the platform interface. Do not copy deployment values from old examples or submit undocumented values through an API.

Treat all behavior in this guide as a preview contract that must be rechecked before every release. Platform UI labels and current operator instructions take precedence if they become more restrictive.

Mode A users choose an available whole-node SKU and maximum duration before launch, subject to the Agent's minimum requirements. In Mode B, the runtime specification is fixed by the published Agent version. Choose between these workflows based on the application and the platform's confirmed release conditions; neither a visible deployment form nor a completed upload proves production readiness.

<a id="section-2"></a>
## 2. Choose an application topology

Choose the smallest topology that represents your application. Do not switch topologies merely to bypass an entry, authentication, or persistence limitation.

| Topology | Artifacts | Runtime shape | Entry and current limitation |
| --- | --- | --- | --- |
| `single` | One OCI image | One backend container serves both UI and API | Direct unauthenticated HTTP. Trusted integration tests only; not production-ready. |
| `split` | Frontend and backend OCI images | Separate frontend and backend containers; only the configured entry service should be public | Direct unauthenticated HTTP, with no generally verified service-discovery contract. Restoring the frontend image field and selecting independent private-registry credentials are incomplete. |
| `frontend-package` | Static frontend ZIP plus one backend OCI image | Intended to use a platform-hosted frontend and a backend API proxy | ZIP upload is blocked by current mode authorization, so this route is unavailable end to end. Client authentication, query strings, and refresh recovery also remain limited. |

Configuration support does not mean that a topology has passed production validation. Before choosing one, confirm that its entry model fits the application:

- Choose `single` when one process can serve the compiled frontend and API on one port.
- Choose `split` only when the frontend and backend require different images or processes and the platform has confirmed the runtime backend route for the current environment. Each image should keep its own default command where possible.
- Prepare `frontend-package` artifacts locally if that topology suits the application, but wait for the platform to enable and validate Mode A ZIP upload before attempting the full workflow. Business API access also requires a validated open and authentication flow. Never put credentials or server-only configuration in the package.

If a production deployment is required now, stop and ask the platform team which supported mode and entry boundary to use. Do not present a successful preview launch as evidence of production security or reliability.

<a id="section-3"></a>
## 3. Prepare the application and runtime

Build every runtime image for `linux/amd64`, as required by the current upload and validation pipeline. Other image architectures are not currently supported. Confirm with the platform that the selected node supports this target and meets the application's hardware requirements. On Apple Silicon or any machine with a different architecture, explicitly set `--platform linux/amd64` instead of relying on the local default.

| Item | Requirement |
| --- | --- |
| Listener | Bind to `0.0.0.0`, not container-only `127.0.0.1`. Each configured frontend or backend container port must be within `1024–65535` and match the application listener. |
| Health check | Provide a lightweight path such as `GET /health` that quickly returns HTTP 200 without calling a model or a slow external dependency. |
| Main process | Run in the foreground, handle `SIGTERM`, and exit within a bounded time. Do not require privileged mode, host networking, or the Docker socket. |
| Command | Prefer the image's tested `ENTRYPOINT` or `CMD`. If the topology requires a command override, enter the exact executable and arguments used in local verification. |
| Permissions | Run the application as a non-root user and grant write access only to explicitly temporary directories. |
| Logs | Write structured logs to stdout/stderr. Include request IDs and stages, but never credentials, complete launch URLs, or sensitive user content. |
| Timeouts | Bound startup and upstream requests. Cancel a model stream when its browser client disconnects. |

Topology-specific configuration:

- For `single`, the image port, application listener, health path, and platform port must all describe the same service. A startup command is currently required.
- For `split`, configure the frontend and backend images and ports independently. Leave a shared command override empty unless the same command is deliberately valid in both images.
- For `frontend-package`, prepare a backend image, backend port, health path, and required startup command for testing after upload support is enabled. The frontend package must be static and contain no runtime secrets.

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

Backend-only placement does not isolate this key from the developer-controlled image, its dependencies, or operators with runtime access. The current injection model is not a safe credential boundary for untrusted third-party code or a production credential-isolation contract. Use this compatibility flow only with trusted preview code and test users; production requires the platform to confirm an appropriate credential or model-call boundary.

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

The frontend image field is not reliably restored when the deployment form is reopened. Keep a record of both image references and digests, and check both fields before saving or submitting again. Independent credential selection for frontend and backend images hosted on different private registries is also incomplete; confirm a supported read-only access route with the platform before using that arrangement.

There is no generally verified backend service-discovery address that an Agent may assume. If the platform has not supplied and validated a route for the current environment, stop the integration rather than inventing one. The direct entry has the same unauthenticated HTTP limitation as `single`. Do not use it for public traffic or sensitive data. Avoid a shared command override unless both images were explicitly built to accept it.

### `frontend-package`

The form displays a frontend ZIP upload control, but current backend mode authorization rejects it for Mode A. Its presence does not indicate a usable upload path: end-to-end ZIP upload, publication, and launch are currently unavailable. Do not bypass the restriction by submitting a different deployment mode.

Use relative paths beneath the platform-provided application base. The intended backend route is `api/...`, but the current open flow does not reliably provide the client with the authentication context required by the API proxy. Do not add a workaround that reads, stores, or forwards a launch token, and do not claim that business API calls work until the platform supplies and validates a documented client flow.

After that flow is available, retest the complete path and do not assume that arbitrary query parameters reach the backend: current proxy behavior does not reliably preserve the query string. Where the API contract permits, put ordinary non-sensitive request data in a validated path segment or request body. Never use a query parameter for a credential. Test refresh, direct navigation, asset loading, streaming, cancellation, and error responses. Browser storage may be unavailable or fall back to non-durable in-memory behavior; even if cached values remain, the launch and authentication context may not survive a refresh.

For every topology, validate the actual user entry—not only a container-local URL. A healthy container can still have a broken public path, missing assets, an incorrect backend route, or an unhandled stream disconnect.

<a id="section-6"></a>
## 6. Design for a temporary data lifecycle

Mode A currently offers **no server-side persistence guarantee**. Files written inside a container may disappear when a session stops, a node is reclaimed, an image changes, or the runtime is repaired. The `storage_gb` field is not a volume allocation and must not be described to users as cloud storage.

Files that end users upload through an Agent are session-temporary unless an approved external store is explicitly configured. Tell users that stopping the session may lose these files and offer export during the session. Storage used to stage publishing artifacts, including frontend ZIPs or planned image archives, is not a persistent workspace for end users; using R2 in an artifact pipeline does not create one.

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

Use a unique version tag that you do not overwrite, and record the resulting registry digest. Tags can move unless the registry enforces immutability; the digest is the immutable artifact identity. Build for the currently required `linux/amd64` target and confirm a compatible node with the platform. Repeat the build for each image in a `split` deployment.

```bash
docker buildx build \
  --platform linux/amd64 \
  --provenance=false \
  -t registry.example.com/team/my-agent:0.1.0-preview.1 \
  --load .

docker image inspect registry.example.com/team/my-agent:0.1.0-preview.1 \
  --format '{{.Os}}/{{.Architecture}} user={{.Config.User}}'
```

Run with placeholder credentials against a mock or explicitly approved test endpoint. Never paste a real key into shell history or commit it to a compose file.

```bash
docker run --rm -d \
  --name mode-a-local \
  --platform linux/amd64 \
  -p 127.0.0.1:8080:8080 \
  -e UNEX_API_KEY=sk-local-placeholder \
  -e UNEX_API_BASE_URL=http://host.docker.internal:18080/v1 \
  -e UNEX_AGENT_ID=local-agent \
  -e UNEX_USER_ID=local-user \
  registry.example.com/team/my-agent:0.1.0-preview.1

curl --fail --silent http://127.0.0.1:8080/health
curl --fail --silent -o /dev/null http://127.0.0.1:8080/
docker logs --tail 80 mode-a-local
docker stop --time 15 mode-a-local
```

Before pushing, verify:

1. Every image reports `linux/amd64`, shows an explicit non-root user, and starts with the exact command intended for the platform. The platform has confirmed a compatible node and the required hardware.
2. Each frontend or backend listener uses `0.0.0.0` and its configured port within `1024–65535`.
3. The health check succeeds without a model call or persistent data.
4. The UI, assets, API, streaming completion, cancellation, and error states work.
5. Missing or mismatched `UNEX_API_KEY` / `UNEX_API_BASE_URL` fails safely without exposing either value.
6. Restarting with an empty filesystem does not corrupt the application.
7. Image layers and logs contain no source credentials, `.env` files, or user data.
8. Each selected topology is tested as a separate artifact set; success in `single` does not validate `split` or `frontend-package`.

For a frontend ZIP prepared for future platform testing, inspect its contents and serve the extracted build locally beneath a non-root URL path:

```bash
unzip -l dist/frontend-0.1.0-preview.1.zip
```

Check that `index.html` is at the package root, assets use relative paths, and the package contains no `.env`, credentials, or fixed session values. Local package tests do not remove the current Mode A upload restriction.

<a id="section-8"></a>
## 8. Publish, configure, and test

### Choose the current artifact route

Open [Agent deployment configuration](https://unexhub.ai/console/my_agents?tab=deploy). The following describes the existing platform UI and APIs, not proof of a successful deployment on a real node.

| Route | Current availability | Developer action |
| --- | --- | --- |
| External Registry | Available for image references | Push your OCI image to a registry, enter its full reference, and select platform-stored read-only credentials if it is private. |
| Push to platform Registry | Shown only when the platform configures TCR; trusted testing only | Use the page's Docker Push instructions only in the approved test environment. Broader use requires per-Agent, short-lived, revocable write credentials. |
| Browser OCI / `docker save` TAR upload | Planned; no current developer upload route | Do not use a source ZIP or `docker export` TAR as an image, or assume an old “local archive” label enables upload. |
| Frontend ZIP for `frontend-package` | Control is visible, but Mode A authorization blocks completion | Prepare and test the package locally; wait for upload authorization and the complete frontend/API flow to be validated. |

For the existing external Registry route:

```bash
docker login registry.example.com
docker push registry.example.com/team/my-agent:0.1.0-preview.1
docker buildx imagetools inspect \
  registry.example.com/team/my-agent:0.1.0-preview.1
```

Record the published `sha256:...` digest. An immutable reference identifies the exact artifact:

```text
registry.example.com/team/my-agent@sha256:<published-digest>
```

Private Registry credentials are encrypted and stored by the platform for read-only image access. Keep them out of image layers, frontend code, application environment variables, and build logs. Node pullability must be checked separately: platform validation or a completed push does not prove that the assigned node can read the reviewed image or its platform copy.

### Validate, save, test, and submit for review

This sequence includes release checks that developers and the platform must verify; the current UI does not enforce every requirement below.

1. Create or select the Agent, open its deployment configuration, and select **Mode A**. Choose `single` or `split` for the current image workflow. The `frontend-package` workflow remains blocked as described above.
2. Select the image source. Enter one `linux/amd64` image reference for `single`, or both frontend and backend references for `split`; select read-only private Registry credentials where needed. Fill in the matching container ports within `1024–65535` and health paths. For `split`, recheck both images whenever reopening the form, and do not assume one credential covers different private registries.
3. Choose **Pull and validate image** (“拉取并校验镜像”). Check the resolved source digest and image-scan state for every component. A tag alone is not the reviewed artifact identity; a production release must also have the required scans enabled and completed.
4. Check the **platform TCR copy state**. Mode A queues external images for copying to TCR. If copying fails, use the copy retry action and verify the result before proceeding. For private external images, do not submit for release until the platform copy is ready and the node's read-only pull has been verified. For production, require a trusted immutable platform copy for every component, even if the current review UI permits an earlier submission for a public image.
5. Save runtime configuration on the same page: frontend/backend container ports within `1024–65535`, health paths, startup command, minimum node specification, and idle timeout. `single` currently requires a command; for `split`, prefer each image's own default command. Keep `gpu_count=1` as one whole-node unit and treat `storage_gb` only as a configuration constraint.
6. After the platform confirms that the selected real-node runtime is available for testing, run a developer test with synthetic data. Confirm the actual digest, image pull, startup, health, real user entry, assets, API routing, model requests, streaming, cancellation, errors, stop, and relaunch. Verify that logs and errors contain no credentials or sensitive data. Do not count platform validation or local container tests as this real-node test.
7. When each digest, scan, required platform copy, saved configuration, and applicable test is ready, choose **Submit for listing review** (“提交上架审核”). The submitted digest must match the artifact tested. Await approval and platform confirmation that the entry and data design suit the intended audience before users launch it.

Compare the **candidate, actually tested, submitted, and approved/published digests** for every image. If one changes, repeat the relevant build, scan, topology, and platform tests and submit the new version for review. Keep the previously approved digest and a rollback procedure available.

### User launch and billing

After review and release approval, users choose an available whole-node SKU and maximum duration before launch. The choice must satisfy the Agent's minimum requirements and available capacity. This differs from Mode B, where the published version fixes the runtime specification.

The platform estimates and precharges runtime cost from the user's recharge balance before starting. Runtime duration starts only when the instance reaches `running`; uploading or validating an image does not start end-user container billing. Current Mode A runtime pricing uses the whole-node hourly rate, rounds runtime up to whole hours, and caps settlement at the precharge. A failed start or failed startup health check receives a full runtime refund. Model calls are billed separately from node runtime. The `storage_gb` field does not currently add a persistent-disk charge or provide a persistent disk.

### Planned upload improvements

Planned work includes browser OCI / `docker save` TAR uploads with progress, cancel/resume and archive validation; scoped temporary Docker Push credentials; complete per-component private Registry handling; and working Mode A frontend ZIP authorization and publication. These are future capabilities, not additional upload endpoints available today. Each route still needs digest validation, scanning, an immutable platform copy, and review before release. Artifact staging does not provide end-user persistence.

<a id="section-9"></a>
## 9. Troubleshooting

| Symptom | Likely cause | What to check |
| --- | --- | --- |
| No Mode A capacity is available | No compatible dedicated node is currently available | Confirm the selected node specification with the platform operator; do not implement cloud provisioning in the Agent. |
| Platform validates an image, but node pull fails | Platform read-only access and node pull access are separate | Check the reference, digest, TCR copy state, and platform-confirmed node read-only access; do not put Registry credentials in the app. |
| Platform copy is pending or failed | The external image has not been copied successfully to TCR | Inspect the copy state, use retry after resolving the error, and verify every component before release. |
| No browser image TAR upload is available | This route is planned, not implemented | Use the existing external Registry route, or configured TCR Docker Push in trusted testing. |
| Platform Registry Push does not appear | The platform has not configured TCR | Use the external Registry route. If TCR Push is visible, use it only for trusted tests until the platform confirms scoped write credentials. |
| Image architecture is rejected, or startup reports `exec format error` | An image is not `linux/amd64`, or the assigned node is incompatible | Rebuild with `--platform linux/amd64`, inspect every image, and have the platform confirm a compatible node. |
| Health check times out | Wrong port/path, loopback-only listener, slow startup, or health handler calls an upstream model | Align the listener, form, and image configuration; keep health local and fast. |
| Container starts but the entry fails | Public route, asset base, frontend/backend route, or exposed role is incorrect | Test through the real platform entry and inspect each browser request, not only container-local `/health`. |
| `split` frontend cannot reach the backend | No validated service-discovery route was provided for the current environment | Do not hard-code a node address; stop and ask the platform team for the supported route before continuing. |
| `split` frontend image is missing after reopening, or two private registries cannot be configured | Image-field restoration and independent credential selection are incomplete | Recheck both saved artifact references and digests before resubmitting; confirm a supported private pull route with the platform. |
| Model request returns 401 | Injected key and Base URL were not kept together, or a version segment was duplicated | Read both values from the same backend environment and construct the endpoint once. |
| `frontend-package` ZIP upload is rejected | Current frontend upload authorization does not allow Mode A | The full workflow is unavailable until the platform fixes and validates authorization; do not change modes to bypass it. |
| `frontend-package` API returns 401 | The current open flow did not provide the client authentication context required by the proxy | Do not expose or persist a launch token as a workaround; keep this topology in preview until the platform confirms the complete flow. |
| Browser can see a managed credential | A backend value was serialized into frontend configuration or logs | Stop the test, remove the exposure, rebuild the artifact, and follow the platform's credential-response process. |
| `frontend-package` loses request parameters | The current proxy path does not reliably preserve query strings | Move non-sensitive request data to the validated body/path where supported and retest; do not use this topology for production. |
| UI state or launch context vanishes on refresh or relaunch | Browser or container state was treated as durable, or the hosted-frontend context was not restored | Make disposable UI state optional. Do not claim refresh recovery or persistence; use only an approved external store for durable data. |
| Tested behavior differs after publishing | A mutable tag resolved to another image | Compare the active digest with the recorded approved digest, roll back, and retest the changed artifact. |
| “1 GPU” expectations do not match the node | `gpu_count=1` was interpreted as physical GPU quantity | Treat it as one whole-node scheduling unit and use the selected node specification for hardware details. |

For direct-entry failures in `single` or `split`, remember that making a port reachable is not a production fix: the current path remains unauthenticated HTTP. Keep testing isolated and escalate entry-boundary requirements to the platform team.

When reporting a problem, include the Agent ID, topology, version, redacted image reference and digest, node SKU, time and timezone, request ID, stage, HTTP status, and reproduction steps. Exclude credentials, complete launch URLs, and user content.

<a id="section-10"></a>
## 10. Technical-preview release checklist

Before releasing a Mode A preview, verify every applicable item. These are release requirements, not a claim that every check is currently enforced automatically:

- [ ] The release is labeled **technical preview** and does not claim that any topology is production-verified.
- [ ] Every runtime image is `linux/amd64`, runs as non-root, binds to `0.0.0.0`, and has a fast, model-independent health check; the platform has confirmed a compatible node and the required hardware.
- [ ] Every configured frontend/backend container port is within `1024–65535`; image, port, health path, entry role, and command agree with the selected topology.
- [ ] Platform image validation and the actual node's read-only image pull were separately verified, including any private Registry or TCR copy.
- [ ] Each image's digest, scan result, and required TCR copy are ready; failed copies were resolved and retried.
- [ ] Platform TCR Push is used only in trusted tests until scoped write credentials are available; browser image TAR upload is not presented as available.
- [ ] Both `split` image fields and digests were rechecked after reopening; separate private-registry access is confirmed where required.
- [ ] The exact current registry digest was tested, reviewed, and pinned or recorded for publication.
- [ ] `UNEX_API_KEY` and `UNEX_API_BASE_URL` stay paired and backend-only; `UNEX_AGENT_ID` and `UNEX_USER_ID` are read from the injected environment.
- [ ] No secret, launch/session value, or sensitive content is shipped to the browser, stored in browser storage, written to an image layer, or logged.
- [ ] The application assumes no server persistence; `storage_gb` is not described as a durable volume.
- [ ] End-user uploads are described as session-temporary unless an approved external store is configured; publishing-artifact staging is not presented as a user workspace.
- [ ] Browser state is optional and disposable; no refresh-recovery claim is made for `frontend-package` until the platform validates restoration of launch and authentication context.
- [ ] Any required durable store is explicitly approved and includes user isolation, encryption, retention, and deletion behavior.
- [ ] `single` and `split` tests use trusted users and synthetic data because their direct entry is unauthenticated HTTP.
- [ ] `split` uses an explicitly validated platform-provided backend route; no node address or unverified discovery convention is hard-coded.
- [ ] The Mode A `frontend-package` ZIP authorization block has been resolved before attempting its full workflow; complete client authentication, query forwarding, and refresh behavior have then been validated for the intended use.
- [ ] The platform independently delivered and validated the selected node runtime, and startup, real entry routing, assets, API calls, streaming, cancellation, failure handling, stop, and relaunch were checked on a real node.
- [ ] The tested node specification is described accurately: `gpu_count=1` means one whole node, not one GPU.
- [ ] A known-good digest and rollback procedure are recorded.
- [ ] Runtime configuration was saved and the tested artifact was submitted for review before user launch; users choose their whole-node SKU and duration at launch.
- [ ] User-facing pricing separates model calls from node runtime and explains that runtime billing starts at `running`, not image upload.
- [ ] The platform has explicitly approved the selected topology, entry security, registry access, and data design for the intended release audience.

Re-run the checklist whenever an image, command, port, health path, topology, frontend package, node specification, or platform runtime changes. Continue with the [Mode B Agent development guide](agent-development-upload.md) when the Cloudflare Containers workflow better fits the release, while checking its current credential-safety and release limitations as well.

<!-- DOCS-PAGER:START -->

---

[← Previous: openclaw-cn](openclaw-cn.md) · [Documentation home](README.md) · [Next: Mode B Agent development →](agent-development-upload.md)
<!-- DOCS-PAGER:END -->
