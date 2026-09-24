# Agent development and upload guide

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Public API reference ↗](https://documenter.getpostman.com/view/57297668/2sBYArUsxK) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/agent-development-upload.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>On this page</strong></summary>

1. [1. Before you start](#section-1)
2. [2. Application runtime requirements](#section-2)
3. [3. Connect to models using managed credentials](#section-3)
4. [4. Web routing and streaming responses](#section-4)
5. [5. Build and verify locally](#section-5)
6. [6. Push to an Alibaba Cloud public repository](#section-6)
7. [7. Configure and publish on the platform](#section-7)
8. [8. Updates, rollback, and example-specific settings](#section-8)
9. [9. Troubleshooting](#section-9)
10. [10. Release checklist and reusable development brief](#section-10)
</details>
<!-- DOCS-TOC:END -->


[Download the Chinese PDF](../../assets/documents/agent-development-upload.zh-CN.pdf) · [Repository home](../../README.md)

For Agent developers · Mode B / Cloudflare Containers

Document version: 1.0 · Updated: 2026-09-24

> **Scope:** This guide covers Mode B only. A Mode A tutorial has not yet been published in this repository. Check the [Agent Developer Center](https://unexhub.ai/agent-doc) for current platform requirements.

This guide is for developers who have a web application, or plan to build an Agent with Python and Vue, and want to publish it through the platform. You deliver a working Docker image. The platform handles image processing, runtime deployment, and user instance startup. You do not need to deploy the platform's Cloudflare Worker yourself.

The verified delivery path is: **develop locally → build an amd64 image → push to Alibaba Cloud Container Registry → enter the external image reference on the platform → validate, scan, and deploy → test → submit for review and publish.**

This page covers platform-managed Agent deployments. For creating a personal key for an ordinary API client, see [Quick start](getting-started.md). These two scenarios use different credential configuration.

Examples use `my-agent:1.0.0` as the image name and `claude-opus-5` as the model. Replace the image name, registry address, and model as appropriate. The model name is a gateway identifier; availability depends on the platform's model list, account group, and channels.

<a id="section-1"></a>
## 1. Before you start

| Requirement | What to check |
| --- | --- |
| Platform developer account | You can create an Agent, edit its deployment configuration, and start a developer test instance. |
| Local Docker installation | Docker Desktop or Docker Engine is running, and `docker version` works. |
| Application source | The project includes a Dockerfile, dependency files, web entry point, backend API, and health check. |
| Alibaba Cloud image repository | You have created a repository and obtained its address, login username, and login instructions from the console. |
| Available model | The default model is supported by the platform and included in the Agent's model allowlist. |

Do not embed a developer's personal model key in the application. At startup, the platform injects credentials for each user–Agent pair. Registry login passwords, managed model keys, and Cloudflare administration credentials serve different purposes and are not interchangeable.

### Choose the delivery method

| Method or artifact | Role in this guide |
| --- | --- |
| Platform “External image registry” | The verified main workflow: enter a complete Registry image reference. |
| Docker push to Alibaba Cloud | Upload the image to your repository, then let the platform pull it. |
| TAR produced by `docker save` | Image backup, migration, or delivery to a system that supports importing it. This does not imply that the platform has a browser upload feature. |
| Source ZIP | Source-code delivery, not a container image reference. |
| Direct Docker push to the platform / browser TAR upload | Planned capabilities in the supplied specification baseline. Use them only after the platform explicitly provides a supported entry point. |

The steps below use an Alibaba Cloud **public repository**. Use a private repository only when the platform supports configuring its Registry read-only credentials.

<a id="section-2"></a>
## 2. Application runtime requirements

| Item | Requirement or recommendation |
| --- | --- |
| Deployment mode | Select “Mode B · Cloudflare Containers.” The backend value is `c`, not `b`. |
| OS and architecture | Build `linux/amd64`, including when developing on an Apple Silicon Mac. |
| Listener | Listen on `0.0.0.0:8080`, not only on the container's `127.0.0.1`. |
| Web entry point | `GET /` serves the user interface. Prefer same-origin web and business API requests. |
| Health check | `GET /health` promptly returns HTTP 200 JSON, such as `{"ok":true}`, without calling a model. |
| Process and permissions | Run as a non-root user, keep the main process in the foreground, and do not require privileged mode or the Docker Socket. |
| Shutdown | Handle SIGTERM, exit within a bounded period, and cancel unfinished model requests. |
| Storage | Treat container memory and disk as temporary. Use explicit external storage for data that must survive restarts. |
| Network requests | Set connection and response timeouts. Close upstream streams when the browser disconnects or cancels. |
| Logs and errors | Record request IDs, stages, durations, and status. Do not log keys, complete session URLs, or raw sensitive inputs. |

Port 8080 is used throughout this guide and the example project. If you use another non-privileged port permitted by the platform, the application listener, image declaration, and platform form must agree. Keep 8080 for an initial integration.

Recommended project layout:

```text
my-agent/
├── backend/
│   ├── app/                  # Python backend and Agent logic
│   └── requirements.txt      # Pinned production dependencies
├── frontend/
│   ├── src/                  # Vue interface
│   ├── package.json
│   └── package-lock.json
├── test/                     # Local tests and mock gateway
├── Dockerfile
├── .dockerignore
├── .env.example              # Names and placeholder values only
├── agent-manifest.json
└── README.md
```

Other stacks are supported if they meet the same HTTP, credential, and lifecycle requirements. For Python and Vue, use a multi-stage build: build the Vue assets first, then copy the backend, production dependencies, and static assets into one runtime image.

At minimum, exclude the following from the Docker build context. Also exclude real `.env` files from version control:

```text
.git
.idea
.env
.env.*
!.env.example
**/node_modules
**/__pycache__
**/.pytest_cache
**/.venv
**/*.log
**/*.pyc
```

Scan the final image before publishing, not just the source tree. Deleting a file in a later image layer does not remove it from earlier layers; credentials should never enter the build context.

<a id="section-3"></a>
## 3. Connect to models using managed credentials

### Read these four variables in the backend

| Variable | Meaning | How to use it |
| --- | --- | --- |
| `UNEX_API_KEY` | Managed key for the current user and Agent | Already includes `sk-`; use it unchanged as the Bearer credential. |
| `UNEX_API_BASE_URL` | Model API root paired with that key | Already includes `/v1`; let the SDK or request code append the endpoint. |
| `UNEX_AGENT_ID` | Current Agent identifier | Use for isolation; do not ask the user to enter it. |
| `UNEX_USER_ID` | Current user identifier | Use for isolation; do not trust a user ID supplied by the frontend. |

Do not enter `UNEX_*` variables in the platform's custom environment-variable form. The platform injects them when starting an instance. Developers simulate this injection only for local testing.

This Python snippet illustrates backend configuration and request parameters; it is not a complete application:

```python
import os

api_key = os.environ.get("UNEX_API_KEY", "")
base_url = os.environ.get("UNEX_API_BASE_URL", "").rstrip("/")
model = os.environ.get("LLM_MODEL", "claude-opus-5")

configured = bool(api_key.strip() and base_url)
# Check configured at the chat entry point; /health must remain available.
endpoint = f"{base_url}/chat/completions" if base_url else ""
headers = {"Authorization": f"Bearer {api_key}"}
payload = {"model": model, "messages": [], "stream": True}
```

Do not append another `/v1` or another `sk-` prefix. With an SDK, do not add `Bearer ` to its `api_key` argument. Populate `messages` after backend validation, and implement timeouts and cancellation for production requests.

### Keep the key and Base URL paired

**Default to the injected `UNEX_API_BASE_URL`. Do not hard-code a test or production hostname as a universal address for all environments.**

The recorded integration test confirmed that a managed key worked when paired with the Base URL injected into the same instance; manually substituting another hostname returned HTTP 401. This establishes that the injected key and URL must stay together. It does not publish or recommend a fixed hostname for every environment.

If your application has a Base URL setting, allow only trusted addresses explicitly configured on the server. Confirm that the selected endpoint accepts the current managed key before switching. Never forward a managed key to an arbitrary browser-supplied URL. End users do not need to enter API keys.

### Keep model configuration consistent

Check the model ID actually sent by the application, the `LLM_MODEL` variable, the Agent's model allowlist, and the channels available to the current account. Return the active model from the backend so that the interface does not display a different model from the one being called.

Example:

```text
LLM_MODEL=claude-opus-5
```

Gateway support for output-length parameters and tool calls varies. For HTTP 400 errors, inspect the specific error and supported parameters. Do not silently switch models or repeatedly retry requests that may incur charges.

<a id="section-4"></a>
## 4. Web routing and streaming responses

### Route every request to the same instance

The current platform routes user traffic using the `session` parameter in the entry URL. Browsers do not automatically copy the page's query parameters to JavaScript, CSS, image, or API requests. A successful HTML request does not prove that its assets can load.

The Python and Vue example uses this approach:

1. Inline JavaScript, CSS, and small icons into the production HTML. Vue and Vite projects can use `vite-plugin-singlefile`.
2. Use same-origin relative API URLs and explicitly forward the current `session`.
3. Preserve the entry URL's path prefix. Set `Referrer-Policy: no-referrer`, and keep session values out of external requests and logs.

Example API URL construction:

```typescript
function apiUrl(path: "config" | "chat"): URL {
  const url = new URL(`api/${path}`, document.baseURI);
  const session = new URL(window.location.href)
    .searchParams.get("session");
  if (session && url.origin === window.location.origin) {
    url.searchParams.set("session", session);
  }
  return url;
}
```

If you keep separate assets, verify that every asset request meets the routing requirements, including fonts, images, and dynamically imported modules. Vite's `base: "./"` alone does not preserve query parameters.

The container's health check can access `/health` directly. Requests through the public Worker hostname still follow the platform's session routing. Users should open instances through the platform rather than remove `session` and navigate to a bare hostname.

### HTTP 200 does not mean generation succeeded

Streaming APIs often send HTTP 200 before the upstream model finishes. Determine completion from the terminal event agreed between the frontend and backend. The example application's protocol includes:

```text
event: token
data: {"content":"OK"}

event: done
data: {"model":"claude-opus-5"}
```

An error can arrive inside an HTTP 200 response:

```text
event: error
data: {"code":"provider_401","retryable":false}
```

`token`, `done`, and `error` are this application's SSE event names, not a universal protocol for every OpenAI-compatible endpoint. Your frontend and backend must agree on success, failure, cancellation, and unexpected stream termination.

<a id="section-5"></a>
## 5. Build and verify locally

Run commands from the project root. Examples use Bash or zsh on macOS or Linux.

### Build an amd64 image

```bash
docker buildx build \
  --platform linux/amd64 \
  --provenance=false \
  --load \
  -t my-agent:1.0.0 .

docker image inspect my-agent:1.0.0 \
  --format '{{.Os}}/{{.Architecture}} user={{.Config.User}}'
```

The result should identify `linux/amd64` and a non-root runtime user. `EXPOSE 8080` declares a port; the application must still listen on it.

### Check startup and the page first

```bash
docker run --rm -d \
  --name my-agent-local \
  --platform linux/amd64 \
  -p 127.0.0.1:8080:8080 \
  my-agent:1.0.0

curl --fail http://127.0.0.1:8080/health
curl --fail -o /dev/null http://127.0.0.1:8080/
docker logs --tail 80 my-agent-local
docker stats --no-stream my-agent-local
```

Open `http://127.0.0.1:8080/` in a browser. Without model credentials, the page and health check should still work, and chat should explain that credentials are missing. Logs must not contain keys or complete user inputs.

### Then verify a complete conversation

Prefer a local mock gateway to test the endpoint path, credential forwarding, model ID, streaming, and cancellation without paid model calls. If using the supplied SOL example source, start its mock in another terminal:

```bash
python3 test/mock_gateway.py
```

Stop the previous test container, then simulate platform injection:

```bash
docker stop --time 15 my-agent-local

docker run --rm -d \
  --name my-agent-local \
  --platform linux/amd64 \
  -p 127.0.0.1:8080:8080 \
  -e API_BASE_URL= \
  -e UNEX_API_KEY=sk-test \
  -e UNEX_API_BASE_URL=http://host.docker.internal:3000/v1 \
  -e UNEX_AGENT_ID=local-agent \
  -e UNEX_USER_ID=local-user \
  my-agent:1.0.0
```

These mock commands require the example project's `test/mock_gateway.py` and Docker Desktop. `sk-test` is only a mock credential, not a real model key. On Linux Docker Engine, configure a suitable route from the container to the host; the container's `127.0.0.1` does not refer to the host.

Cancel a generation and verify that the upstream call stops. Run `docker stop --time 15 my-agent-local` and verify a clean exit. Test the page, health endpoint, and conversation separately; success in one does not replace the others.

<a id="section-6"></a>
## 6. Push to an Alibaba Cloud public repository

### Create the repository and confirm its address

Create a namespace and repository in the Alibaba Cloud Container Registry console and select public access. Registry domains vary by region and instance type. **Use the repository address and login instructions provided by your console.** This guide does not require a fixed namespace prefix.

The example below uses a Hangzhou endpoint. Replace the three `YOUR_...` values with your own information. Increment the version for each release rather than continually overwriting `latest`.

```bash
REGISTRY='registry.cn-hangzhou.aliyuncs.com'
NAMESPACE='YOUR_NAMESPACE'
REPOSITORY='YOUR_REPOSITORY'
VERSION='1.0.0'
IMAGE="$REGISTRY/$NAMESPACE/$REPOSITORY:$VERSION"

docker login "$REGISTRY" --username 'YOUR_LOGIN_NAME'
docker tag my-agent:1.0.0 "$IMAGE"
docker push "$IMAGE"
```

Enter the password only at Docker's interactive prompt. Do not put it in a script, Dockerfile, source tree, or chat. These commands upload a container image, not a frontend source ZIP.

### Record the digest and check anonymous access

Record the `sha256:...` digest printed after the push. A tag is a convenient input name; the digest identifies that image's content. Verify the digest during platform binding, deployment, and rollback.

A successful pull on an authenticated machine does not prove that anonymous access works. Use a temporary empty Docker configuration to inspect the remote manifest without your saved Registry credentials:

```bash
CHECK_CONFIG=$(mktemp -d)
docker --config "$CHECK_CONFIG" manifest inspect "$IMAGE"
rm -r "$CHECK_CONFIG"
```

If this fails, check public visibility, the address, and the tag. For a private image, use platform-supported Registry read-only credentials. Do not put the Registry username and password in Agent environment variables.

### Export a TAR when needed

```bash
docker image save -o my-agent-1.0.0-amd64.tar my-agent:1.0.0
docker load -i my-agent-1.0.0-amd64.tar
```

This produces a standard Docker image archive. Do not substitute `docker export`, which exports a container filesystem rather than the same image artifact with its configuration. A TAR file's SHA-256 and a Registry image digest hash different objects and are not interchangeable.

<a id="section-7"></a>
## 7. Configure and publish on the platform

Open your Agent's developer deployment page. Button labels may vary by platform version; verify the following stages in order.

### Prepare the manifest and form

Include `agent-manifest.json` at the project root and describe the application's actual capabilities:

```json
{
  "schema_version": 1,
  "deploy_mode": "c",
  "runtime": {
    "port": 8080,
    "health_path": "/health",
    "command": "",
    "instance_type": "basic",
    "idle_minutes": 15
  },
  "capabilities": {
    "input_types": ["text"],
    "output_types": ["text"],
    "needs_persistent_storage": false
  }
}
```

The manifest is a deployment draft, not a replacement for platform validation. If automatic import is unavailable, enter its values manually.

| Form field | Example value |
| --- | --- |
| Deployment mode | Mode B · Cloudflare Containers |
| Image source | External image registry |
| Image reference | Full `Registry/namespace/repository:version`, without `https://` |
| Entry port | `8080` |
| Health path | `/health` |
| Startup command | Leave empty to use the image's ENTRYPOINT / CMD. |
| Instance type | `basic` in this example; select based on measured resource needs and the platform's available options. |
| Idle reclamation | 15 minutes in this example; use a value supported by the platform and appropriate for the workload. |
| Non-sensitive environment variables | For example, `LLM_MODEL=claude-opus-5`. |
| Model allowlist | Include `claude-opus-5` or your actual model identifier. |

Do not enter keys in the ordinary environment-variable form. Some platform versions store and return these values as plaintext; this form is not a dedicated secret store.

### Complete the release stages

1. Save the deployment mode and runtime settings, then submit the complete image reference.
2. Pull and validate the image. Check the architecture and digest displayed by the platform.
3. Wait for scanning and image mirroring to complete. Inspect the failed stage's error before retrying.
4. Deploy the runtime and wait for it to become ready. A successfully deployed Worker does not prove that the image has been bound successfully.
5. Start a developer test instance through the platform. Open the page, inspect health, and send one short request.
6. Confirm completion, the intended model, and credential protection before submitting for review and publishing.
7. After publication, verify the ordinary user launch path and that permissions and billing attribution match platform rules.

Do not replace a version in place while it is under review or already published. Create a new candidate version. Withdraw or wait for an existing review according to platform procedures rather than bypassing state checks.

### What an ordinary user should experience

The user starts their own instance through the platform, waits for cold startup, and enters the Agent interface to use its features. The application does not request an API key. Users can stop the instance through the platform when finished. Container runtime fees and model invocation fees are separate; current charges, maximum runtime, and refund rules are those displayed by the platform.

<a id="section-8"></a>
## 8. Updates, rollback, and example-specific settings

Use a new version, such as `1.0.1`, for each update. Build, test, and push it; then submit the new reference on the platform, verify the digest, scan, deploy, stop the old instance, and start a new one. Pushing a Registry tag does not automatically update an already bound image or replace a running container.

To roll back, use the platform's supported version-switching process to select the previous verified digest and its corresponding runtime settings. Changing a tag name or retagging an image locally is not an online rollback.

### If you use the SOL Agent example directly

For SOL Agent 1.0.5, configure the application to use the platform-injected `UNEX_API_BASE_URL` and retain `claude-opus-5` only when that model is available. Its image tag is `registry.cn-hangzhou.aliyuncs.com/xxgc_lbs/study:sol-agent-mode-b-1.0.5`. Clear or replace any old `API_BASE_URL` override saved in the platform or browser. Pull, bind, deploy, and restart the instance to apply the new image.

The following notes cover upgrades from 1.0.4. The downloadable PDF is synchronized with this guide and includes both the current 1.0.5 configuration and the retained 1.0.4 upgrade notes.

The general rule in this guide is to pair the injected key with its injected Base URL. The delivered SOL Agent 1.0.4 image has a historical override: `API_BASE_URL=https://api.unexhub.ai/v1`, which takes precedence over the platform-injected address.

Configure that example for your deployment environment:

- If the platform preserves empty environment values, explicitly set `API_BASE_URL` to an empty string so the backend uses `UNEX_API_BASE_URL`. Deleting a form field alone does not remove an ENV default baked into the image.
- If empty values are not preserved, set `API_BASE_URL` to the administrator-confirmed address paired with the current managed key, or remove the override from your Dockerfile and rebuild.
- If the browser previously saved another Base URL, also select and save the correct address under “Workspace settings → Platform-managed connection.” A changed server default does not necessarily replace an existing browser preference.
- The recorded test succeeded with the platform-injected value. Confirm the injected value again for every environment.

`API_BASE_URL`, `ALLOWED_API_BASE_URLS`, and `LLM_MODEL` are configuration names supported by this example application. They are not platform-reserved variables that every Agent must implement.

<a id="section-9"></a>
## 9. Troubleshooting

| Symptom | Check first | Action |
| --- | --- | --- |
| Runs locally but fails on the platform | Architecture, listener, port, and startup command | Verify amd64 and 0.0.0.0:8080, use the image's default command, and inspect startup logs. |
| Blank page; JS / CSS returns 400 | Whether asset requests lost `session` | Inline assets or satisfy the routing contract; check that the instance uses the new digest. |
| `missing_session` | Bare hostname access or missing entry parameters | Reopen through the platform and fix session forwarding on same-origin requests. |
| Worker deployed but image binding failed | Deployment mode, review status, and image state | Confirm Mode B uses `c`, follow the review process, and avoid rebuilding without evidence of an image problem. |
| HTTP 401 / `provider_401` | Whether key and Base URL match; token validity | Compare the injected address, restart for current credentials if appropriate, and ask the administrator to inspect authentication logs. |
| HTTP 402 / `insufficient_user_quota` | Current user's wallet balance | Return to the platform to resolve the balance issue; stop automatic retries. |
| HTTP 403 | Explicit Agent-disable code versus model or group restrictions | Treat `AGENT_ACCESS_DISABLED` as an Agent ban; inspect permissions for other 403 responses. |
| HTTP 503 / `model_not_found` | User group, model allowlist, and available channels | Have the administrator inspect routing. A working upstream alone does not prove that this user's token has a usable route. |
| HTTP 400 | Request parameters, model ID, and tool-call compatibility | Inspect safe error codes and supported parameters; disable tools for a controlled comparison if needed. |
| HTTP 429 / timeout | Rate limits, capacity, and timeout configuration | Offer a later retry, bound retries, and stop upstream calls when the user cancels. |
| HTTP 200 in the network panel but an application error | SSE error and completion events | Inspect the response body, not only the HTTP status. |
| Old model or page after an update | Bound digest, existing instance, environment overrides | Deploy the new version, restart, remove the old `LLM_MODEL` override, and inspect the backend's version and model. |

When reporting a problem, include the Agent ID, application version, image digest, timestamp and timezone, request ID, HTTP status, sanitized error code, and reproduction steps. Do not paste API keys, Authorization headers, complete session URLs, or other users' messages into public tickets.

<a id="section-10"></a>
## 10. Release checklist and reusable development brief

### Before publishing

- [ ] The image is linux/amd64, runs as non-root, and listens on 0.0.0.0:8080.
- [ ] The page and /health work; missing credentials produce a clear message.
- [ ] Keys remain in the backend and are absent from image layers, browser responses, and logs.
- [ ] The default model, Agent allowlist, and account channels agree.
- [ ] The key and Base URL belong to the same trusted runtime environment.
- [ ] Page, asset, and API requests preserve the required session routing.
- [ ] A streamed answer, cancellation, and an error response have been verified.
- [ ] SIGTERM causes a bounded exit; persistent data does not depend on temporary disk.
- [ ] The platform can pull the repository, the digest is recorded, and scanning passes.
- [ ] The runtime is ready and a new instance passes testing before review and publication.

### Brief for an AI assistant or developer

```text
Build an Agent for the platform's Mode B / Cloudflare Containers.

Name: [fill in]
Users and purpose: [fill in]
Core workflow: [3-6 steps]
Inputs and outputs: [fill in]
Default model: [an available and permitted platform model]
Stack: Python FastAPI + Vue, or the existing project stack

Delivery requirements:
1. One linux/amd64 container, non-root, listening on 0.0.0.0:8080.
2. GET / serves the UI; GET /health promptly returns 200 JSON
   without calling a model.
3. Read UNEX_API_KEY and UNEX_API_BASE_URL in the backend as a pair.
   The key already includes sk-; the URL already includes /v1.
4. Do not ask end users for keys or expose keys to browsers or logs.
5. Support platform session routing and entry URL path prefixes.
6. Provide streaming results, errors, cancellation, copying,
   and a mobile-compatible interface.
7. Set timeouts, cancel upstream on disconnect, and handle SIGTERM.
8. Treat container disk as temporary; declare any external storage.
9. Include Dockerfile, .dockerignore, agent-manifest.json, README,
   and a local mock gateway or equivalent tests.
10. Include build, run, Alibaba Cloud tag/push, and docker save commands.
11. Provide platform form values and actual verification results.
    Do not describe mock calls as successful live model verification.

Use the external Registry workflow. Do not assume browser TAR upload
is already supported by the platform.
```

### References and scope

This guide is based on the supplied Mode B container, upload, usage, and billing specification dated 2026-09-23, and the SOL Agent 1.0.4 build, Alibaba Cloud push, and online connectivity verification. Planned capabilities are not presented as already available. Current platform features, repository rules, and permissions take precedence.

- [Cloudflare Containers architecture and lifecycle](https://developers.cloudflare.com/containers/concepts/architecture/)
- [Cloudflare Containers image management](https://developers.cloudflare.com/containers/guides/image-management/)
- [Cloudflare Containers limits](https://developers.cloudflare.com/containers/platform/limits/)

Cloudflare's documentation explains the underlying container capabilities. Agent developers still deploy through the platform and do not need to copy Cloudflare administration commands or supply an administration token.

<!-- DOCS-PAGER:START -->

---

[← Previous: openclaw-cn](openclaw-cn.md) · [Documentation home](README.md)
<!-- DOCS-PAGER:END -->
