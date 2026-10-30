# Mode A · Unexhub Containers development guide

<!-- DOCS-NAV:START -->
[Documentation home](README.md) · [Chat Completions API](chat-completions.md) · [Agent Developer Center ↗](https://unexhub.ai/agent-doc) · [简体中文](../zh-CN/agent-development-mode-a.md)

**Browse:** [Start here](README.md#start-here) · [API & account](README.md#api-and-account) · [Apps & editors](README.md#apps-and-editors) · [CLI & coding agents](README.md#cli-and-coding-agents) · [Agent development](README.md#agent-development) · [API reference](README.md#api-reference)
<!-- DOCS-NAV:END -->

For Agent developers · Mode A / Unexhub Containers

Updated: 2026-10-23

Mode A starts an isolated application container from your OCI image for each user session. Developers select an administrator-defined **instance type** in deployment configuration. Users choose a runtime, review the estimate, and launch. Expiry or an explicit stop releases the container and its temporary files.

For Cloudflare Containers, use the [Mode B guide](agent-development-upload.md). Names, CPU, memory, and hourly prices for both modes come from the current platform catalog. Old screenshots and sample prices do not determine the actual bill.

<a id="section-1"></a>
## 1. Prerequisites

- A developer account that can edit an Agent.
- One `linux/amd64` OCI image serving the web interface and backend API.
- A complete registry reference and read-only pull credentials for private images.
- Measured CPU, memory, temporary disk, and startup requirements.
- If SQL is needed, a PostgreSQL/MySQL version supported by the [database catalog](agent-databases.md).

<a id="section-2"></a>
## 2. Application delivery

Only **Single container (frontend and backend in one image)** is currently available. Prefer same-origin relative URLs between the web interface and backend API.

**Separate frontend/backend containers** and **Static frontend + backend container** are hidden and disabled for new launches. Agents with either saved configuration must revalidate a single-container image before starting a new instance. Existing instances remain accessible and can still be stopped. Do not bypass the UI through direct API requests.

Mode A currently has no directory-mount configuration or custom GPU, CPU, memory, or disk inputs. Previous resource fields are hidden; select resources through the instance-type catalog. **Idle shutdown (minutes)** defaults to 15; set it to 0 to disable it. Saved changes apply to newly launched instances. Containers and temporary files are released after continuous inactivity. Active connections, CPU, network traffic, or reported jobs delay idle release; sampling and keep-alive connections can add a delay. The maximum runtime selected by the user still applies independently.

<a id="section-3"></a>
## 3. Image and runtime requirements

| Item | Requirement |
| --- | --- |
| Architecture | `linux/amd64` OCI image |
| Listener | Listen on `0.0.0.0` at the configured port, within `1024–65535`, such as `8080` |
| Health | A lightweight path starting with `/`, such as `/health`, without model calls |
| Command | Optional; leave empty to use the image's `ENTRYPOINT` / `CMD` |
| Process | Run in the foreground, handle SIGTERM, and close requests and database connections |
| Environment | Non-sensitive application settings only; `UNEX_` is reserved |
| Files | Temporary data; no dependency on host directories, Docker socket, or privileged mode |
| Logs | Stages and sanitized errors; no passwords, keys, database URIs, or complete authorization values |

For example:

```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "app.py"]
```

Python is only an example. Other languages can use the same image and runtime requirements. `EXPOSE` does not make the application listen.

<a id="section-4"></a>
## 4. Publish and validate the image

1. Build and push an image with a fixed version tag. Exclude `.env`, personal model keys, registry passwords, and database passwords.
2. Open **Deployment configuration → Mode A · Unexhub Containers → Image source**. If the platform offers a Docker Push address, follow its generated commands. For an external registry, enter the complete image reference.
3. For a private registry, select a read-only credential through the registry-credential manager. Never put registry passwords in application environment settings.
4. Validate the image and wait for its digest and security scan. If the page requires a platform copy, wait for that copy to finish.
5. Confirm that the bound image is the release you tested rather than an older validation result.

A first launch may download the image; startup time depends on its size and registry connectivity. Registry or authorization failures are reported as launch failures. Do not make an image public merely to bypass a credential error.

<a id="section-5"></a>
## 5. Select resources and databases

Choose **Minimum resource requirements → Instance type**. Options show the instance name, CPU, memory, and hourly price. Each mode has a separate catalog; switching modes refreshes the list and does not reuse another mode's selections.

Mode A initially includes tiers based on `lite`, `basic`, and `standard-1` through `standard-4`. Administrators can change names, resources, prices, or availability. **The live catalog is authoritative.** A code alone is not a permanent resource guarantee.

If needed, add PostgreSQL, MySQL, or both in **Database configuration**, choose versions, and save. Backend connection settings such as `UNEX_DATABASE_POSTGRESQL_URL` and `UNEX_DATABASE_MYSQL_HOST` are injected when the container starts. See the [database guide](agent-databases.md) for every variable and working examples. Leave the configuration empty if SQL is unnecessary.

Read passwords only in the backend. Do not send them to the browser, logs, or a frontend build. Stopping a container does not automatically erase its independent database.

<a id="section-6"></a>
## 6. Launch, runtime, and billing

1. Open the Agent; the platform checks for a reusable active instance.
2. If none exists, review the developer-configured instance type and select an available runtime.
3. Review the estimate and select **Launch**. The platform pulls the image if needed and starts the container.
4. Wait until ready, then use the platform's open-instance action.
5. The instance stops at the selected runtime limit or when explicitly stopped. Selecting Stop immediately shows the stopping animation; final status and billing update after resource cleanup is confirmed.

Compute cost uses the displayed **hourly price × billable duration**, rounding the duration up to whole hours. Launch reserves the selected maximum duration from the recharge balance. Stop settles actual running time and refunds any excess reservation. Preparation and creation are excluded from successful runtime, and a failed launch does not incur successful-runtime charges. Model calls are charged separately under the platform's model-billing rules.

Existing instances retain their launch-time price after an administrator changes the catalog. New launches use the latest available price. Disabled types cannot start new instances. The server-returned estimate and final bill determine the charge.

Mode A container links use `/?session=<session ID>`. Once an instance is ready, the same link opens directly on another computer or in a fresh browser. A missing session returns `{"error":"missing_session"}`; an incorrect session or an instance that is not ready, stopped or expired returns `{"error":"session_not_ready"}`. Application login state is separate for each browser.

<a id="section-7"></a>
## 7. Test locally

```bash
docker buildx build --platform linux/amd64 -t registry.example.com/team/my-agent:1.0.0 --load .
docker run --rm -p 8080:8080 registry.example.com/team/my-agent:1.0.0
curl --fail http://127.0.0.1:8080/health
```

Verify the homepage, API, streaming, database connections, and process shutdown. Check private-registry pull access locally without copying Docker login files into the image.

<a id="section-8"></a>
## 8. Self-test and publish

Save the image and runtime configuration, then use **Developer self-test → Open launch page** below **Minimum resource requirements** in deployment settings. The launch confirmation page is also available from compute configuration. Choose a duration, review the estimate, and start a test instance. Verify a cold start, page access, API calls, database reads/writes, an explicit stop, and expiry.

Once image binding and scanning are complete, submit the Agent for review. Investigate and fix image vulnerabilities; a risk-confirmation dialog does not replace runtime testing. Market users receive approved configuration. Follow the version/review workflow when changing images or runtime requirements.

After your test instance starts, expand **Technical details** to view container runtime logs on the right. Logs are available only to the Agent developer for an instance they launched themselves. The expanded panel updates the latest output and supports pause and follow controls. Collapsing it, hiding the page, or stopping the instance stops automatic fetching. Ordinary users do not see this panel.

<a id="section-9"></a>
## 9. Troubleshooting

| Symptom | Check |
| --- | --- |
| No available type | Reload the catalog and check whether the administrator disabled the type |
| Private pull fails | Complete reference, digest, registry connectivity, and read-only credential |
| Running but cannot open | `0.0.0.0`, matching ports, valid health path, and sanitized application logs |
| Database failure | Selected engine, injected variables, version, and TLS requirements |
| Files disappear after stop | Container files are temporary; use SQL or export important output |
| Split delivery is disabled | Use a single container |
| Idle shutdown is delayed | Check active connections, CPU, network traffic, and background tasks; sampling and keep-alive connections may delay release |
| A screenshot shows GPU or dedicated-node settings | It predates this workflow; follow the current instance-type and cost form |

<a id="section-10"></a>
## 10. Release checklist

- The bound digest matches the tested artifact and scanning is complete.
- The selected type has sufficient resources and the expected current hourly price.
- One application image runs without host-directory mounts; idle shutdown and maximum runtime are tested.
- SQL configuration, variable handling, and isolation between users work.
- Cold start, explicit stop, expiry, page access, and APIs work.
- No platform management credentials or registry passwords appear in the image, frontend, logs, or errors.
- User-facing instructions explain temporary files, runtime limits, and compute charges.

[Database guide](agent-databases.md) · [Mode B guide](agent-development-upload.md) · [Documentation home](README.md)
