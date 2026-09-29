# 模式 B Agent 开发与上传指南

<!-- DOCS-NAV:START -->
[English (primary)](../en/agent-development-upload.md) · [中文目录](README.md) · [模式 A 技术预览](agent-development-mode-a.md) · [聊天补全 API](chat-completions.md) · [Agent 开发中心 ↗](https://unexhub.ai/agent-doc)

**目录：** [开始使用](README.md#start-here) · [API 与账户](README.md#api-and-account) · [客户端与编辑器](README.md#apps-and-editors) · [命令行与编程 Agent](README.md#cli-and-coding-agents) · [Agent 开发](README.md#agent-development) · [API 参考](README.md#api-reference)
<!-- DOCS-NAV:END -->

<!-- DOCS-TOC:START -->
<details open>
<summary><strong>本页目录</strong></summary>

1. [1. 开始前准备什么](#section-1)
2. [2. 运行规范与实例规格](#section-2)
3. [3. 模型访问与持久存储的当前边界](#section-3)
4. [4. 页面路由与流式响应](#section-4)
5. [5. 构建镜像并在本机验证](#section-5)
6. [6. 推送到自己的外部镜像仓库](#section-6)
7. [7. 配置、部署与提交审核](#section-7)
8. [8. 版本更新与规划中的上传入口](#section-8)
9. [9. 常见问题排查](#section-9)
10. [10. 发布前检查与可复制的开发需求](#section-10)
</details>
<!-- DOCS-TOC:END -->

[项目首页](../../README.md)

面向 Agent 开发者 · 模式 B / Cloudflare 容器

文档版本：1.1　更新日期：2026-09-29

> **范围说明：** 本指南覆盖模式 B。独立节点流程请查看[模式 A 技术预览指南](agent-development-mode-a.md)。下文“当前”指现有流程，“规划中”指尚未实现的工作。

模式 B 在 Cloudflare Containers 上运行你提供的单个 OCI 容器镜像。你负责构建并发布镜像，平台将其搬运到平台的 Cloudflare 镜像仓库，并部署 Worker/Container 运行时。用户实例按会话启动，空闲后回收。开发者无需自行部署平台的 Worker。

当前制品流程是：**构建 `linux/amd64` 镜像 → 推送到自己的外部 Registry → 校验源镜像并扫描 → 保存运行配置 → 部署运行时 → 自测并提交审核**。外部公共和私有仓库均可使用；私有镜像通过平台的凭证管理功能保存并选择 Registry 只读凭证。

> **发布限制：** 镜像流程已经存在，但面向不可信第三方镜像的安全模型访问尚未完成。当前运行时会注入“用户 × Agent”长期模型 Key；这一机制应仅用于可信内部兼容测试，不能作为安全的生产契约。[第 3 节](#section-3)中的可信模型代理和每用户 D1/R2 工作区均为规划能力。部署成功不能消除这些限制。

示例使用 `my-agent:1.0.0` 和端口 `8080`。请将 Registry 占位信息和模型标识替换为自己项目的实际值。本文不提供某个示例项目的镜像或凭据。

<a id="section-1"></a>
## 1. 开始前准备什么

| 准备项 | 需要确认的内容 |
| --- | --- |
| 平台开发者账号 | 可以创建 Agent 并编辑部署配置 |
| 本地 Docker | Docker Desktop 或 Docker Engine 已运行，`docker version` 可用 |
| 应用 | 有 Dockerfile、锁定的依赖、网页入口、业务 API 和轻量健康接口 |
| 自己的外部镜像仓库 | 知道完整镜像地址且可以推送；私有镜像为平台另行准备只读拉取凭证 |
| 资源测量 | 选择实例规格前测量内存、CPU、启动时间和临时磁盘用量 |
| 模型与数据需求 | 明确 Agent 所需模型及长期保存的数据，并核对第 3 节的发布限制 |

不要将个人模型 Key、Registry 密码或 Cloudflare 管理凭据写进镜像。这些凭据用途不同。Registry 凭证应保存在平台凭证管理功能中，不应放进 Agent 环境变量。

### 选择当前可用的制品路径

| 入口或制品 | 当前状态 |
| --- | --- |
| 外部 Registry 中的单个镜像 | 模式 B 当前可用流程；填写完整镜像地址，私有仓库选择只读凭证 |
| Docker Push 到自己的 Registry | 平台拉取之前，开发者在本地完成的镜像发布步骤 |
| 浏览器上传镜像 TAR | 尚未实现；模式 B 当前没有浏览器 TAR 上传路由 |
| 直接 Docker Push 到平台 | 尚未实现；不要假定平台提供推送地址或写入凭证 |
| 源码 ZIP 或 `docker export` 归档 | 不是本流程支持的镜像制品 |

规划中的三入口上传体验见[第 8 节](#section-8)，当前仍按外部 Registry 流程操作。

<a id="section-2"></a>
## 2. 运行规范与实例规格

| 项目 | 要求与建议 |
| --- | --- |
| 部署模式 | 选择“模式 B · Cloudflare 容器” |
| 系统与架构 | 构建 `linux/amd64`，Apple Silicon 电脑也需显式指定 |
| 监听地址 | 在配置的端口监听 `0.0.0.0`；仅监听 `127.0.0.1` 时，容器外无法访问 |
| 入口端口 | 必填，平台允许 `1024–65535`；本文使用 `8080`，应用实际监听端口必须与运行配置一致 |
| 网页入口 | `GET /` 提供界面，网页与业务 API 优先使用同源请求 |
| 健康路径 | 必填、非空、以 `/` 开头，例如 `/health`；建议快速返回 HTTP 200 JSON，不调用模型 |
| 启动命令 | 可选；留空使用镜像的 `ENTRYPOINT` / `CMD`，即使当前表单显示必填标记也可留空 |
| 自定义环境变量 | 以明文保存并原样返回；仅放非敏感配置，名称不能以保留前缀 `UNEX_` 开头 |
| 进程与退出 | 非 root 运行，主进程保持前台，处理 SIGTERM 并取消未完成的上游请求；不依赖特权模式或 Docker socket |
| 数据保存 | 容器内存和磁盘均为临时资源，每用户平台持久化尚未实现 |
| 网络与日志 | 设置连接与响应超时，取消时关闭流；记录请求编号、阶段、耗时和安全错误，不记录 Key、完整会话地址或敏感输入 |

**当前就绪判定检查暴露端口是否可连，不检查健康路径的 HTTP 响应。** 即使 `/health` 返回 404，或业务 API 不可用，只要端口可达仍可能显示就绪。应配置有效健康路径，并单独验证响应。

`EXPOSE 8080` 只声明预期端口，不会创建监听。建议与应用和表单保持一致。默认监听 80 的 nginx 镜像，需要修改应用配置以监听 8080 等允许的端口。本地 `docker run -p 80:80` 成功，不代表能通过平台端口校验。

### 从六档平台实例规格中选择

| 实例类型 | vCPU | 内存 | 磁盘 | 常见用途 |
| --- | --- | --- | --- | --- |
| `lite` | 1/16 | 256 MiB | 2 GB | 很小的前置处理服务 |
| `basic` | 1/4 | 1 GiB | 4 GB | 轻量 API 与脚本 |
| `standard-1` | 1/2 | 4 GiB | 8 GB | 常规单容器应用 |
| `standard-2` | 1 | 6 GiB | 12 GB | 中等负载 |
| `standard-3` | 2 | 8 GiB | 16 GB | 资源需求较高的应用 |
| `standard-4` | 4 | 12 GiB | 20 GB | 重负载 |

以上为平台当前档位定义，不代表 Cloudflare 所有方案的规格。审核前选择并保存实例类型。**模式 B 在版本发布时固定规格，用户启动时不能修改。** 模式 A 则由用户在启动前选择节点 SKU。

`lite` 只有 256 MiB 内存，不要假定它能容纳 JVM 或依赖较多的应用，应先测量。并发实例数由平台控制，当前默认上限为 50。并发上限限制的是同时运行的成本暴露，不是总费用上限。总成本还取决于实例规格、运行时长、实际资源计量，以及平台独立的预算与结算规则。

### 临时状态必须允许丢弃

浏览器 `localStorage` 只能保存少量非敏感、可丢弃的界面状态，例如显示偏好。它受浏览器配置文件和来源域限制，可能被清除，也不能可靠地跨设备或用户同步。禁止保存 Key、Authorization、`session` 值、登录凭据、敏感对话或必须恢复的记录。

不能依靠容器磁盘或浏览器存储承诺文件长期保存。另行安排的外部数据服务需要单独审查访问控制与保留方案，不能将其等同于规划中的平台工作区。

适合时使用多阶段构建，例如先构建 Vue 静态资源，再将资源和生产后端依赖放入单个运行镜像。从 Docker 构建上下文中排除本地密钥和开发制品：

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

真实 `.env` 也不能进入版本控制。必须扫描最终镜像：在后一层删除密钥，不能将其从之前的镜像层中移除。

<a id="section-3"></a>
## 3. 模型访问与持久存储的当前边界

### 当前模型 Key 注入及兼容使用边界

当前运行时会注入 `UNEX_API_KEY`、`UNEX_API_BASE_URL`、`UNEX_AGENT_ID` 和 `UNEX_USER_ID`。模型 Key 按“用户 × Agent”生成，但它是容器进程可读取的长期凭据。开发者控制的镜像、镜像内的依赖，或能读取运行环境的运维人员都可能取得它。Key 没有进入浏览器，不能防止上述暴露。

已有的可信内部测试镜像可能仍需兼容这一行为。**不要将真实 `UNEX_API_KEY` 注入列为新第三方 Agent 的交付要求，也不要将其视为生产环境的安全隔离。** 因此本文不提供真实 Key 注入模板。缺少凭据时，不要通过硬编码 Key、要求用户在浏览器填写 Key 或共享开发者 Key 来绕过。镜像实例通常不会提供 `unex_agent_token` URL fragment。

### 规划中的模型契约——尚未实现

目标方案是平台控制的出站代理。容器只会收到：

```text
UNEX_MODEL_BASE_URL=http://model.unex.invalid/v1
```

该虚拟地址**目前尚未提供，也不可用**。实现后，容器后端向它发送标准模型请求，不持有真实用户 Token。可信出站处理器识别容器对应的受信会话，模型网关在计量用量前核对用户、Agent、会话有效性、模型允许列表和本次预算。容器自行提供的用户 ID、身份请求头或 `session_id` 不能决定计费主体。

以下只是未来契约的接入示意，并非当前平台可运行示例。预期契约不可用时会明确失败，没有 Key 或域名回退：

```javascript
// 仅用于规划中的契约：平台模型代理尚未实现。
const baseURL = process.env.UNEX_MODEL_BASE_URL;
if (baseURL !== "http://model.unex.invalid/v1") {
  throw new Error("此运行环境尚未启用平台模型代理");
}
const model = process.env.LLM_MODEL;
if (!model) throw new Error("请选择平台允许的模型");

const response = await fetch(`${baseURL}/chat/completions`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    model,
    messages: [{ role: "user", content: "你好" }],
  }),
  signal: AbortSignal.timeout(30_000),
});
if (!response.ok) throw new Error(`模型请求失败：${response.status}`);
```

自行设置该环境变量不会启用代理。未来若某个 SDK 必须填写 `apiKey`，只能使用固定的非密钥占位值；可信代理必须丢弃容器带来的 Authorization。不得回退到真实 Key 或公共模型域名。

当你的发布版本获得支持的模型访问能力后，应保持实际模型 ID、`LLM_MODEL` 等应用配置、Agent 模型允许列表和账号可用路由一致。前端显示的模型应由后端返回。不支持的参数或工具调用应明确报错，不要静默切换模型或反复重试收费请求。

### 规划中的每用户存储——尚未实现

当前没有每用户 D1/R2 工作区。实例停止时本地容器文件可能丢失；界面出现“R2/D1 持久化”文案并不代表功能已可用。

目标是为每个 `(agent_id, user_id)` 提供稳定工作区，由同一用户的新会话和镜像版本共同使用。D1 保存小状态、版本、文件索引和配额；私有 R2 保存上传文件和结果字节。平台控制的 Storage Broker 通过规划中的虚拟地址，仅开放当前会话被授权的数据：

```text
UNEX_STORAGE_BASE_URL=http://storage.unex.invalid/v1
```

该地址与工作区均**尚未实现**。未来存储接入在平台明确启用契约之前必须保持禁用，不能回退到容器磁盘却显示“已保存”。容器不会取得 D1 binding、R2 账号密钥、桶级权限或任意对象 key 的访问能力。

规划中的文件流程从已鉴权会话页面开始：预留工作区容量 → 签发单个暂存对象的短时上传权限 → 上传并显示进度 → 核对实际大小、内容、扫描结果和配额 → 提升为正式私有对象并返回 `file_id`。此后即使容器停止，用户也应能从平台查看、下载并明确删除自己的文件。其他用户即使知道文件 ID，也必须被拒绝。这条完整链路仍待实现和验证。

部署制品暂存区与用户持久工作区属于不同存储和权限域。用于暂存镜像 TAR 的桶不是用户文件持久化。模型费用、运行时费用和未来存储费用或免费额度，也需要分别公示。在这些改造完成前，不能向不可信镜像承诺 Token 隔离或跨会话文件恢复。

<a id="section-4"></a>
## 4. 页面路由与流式响应

### 让每次请求进入同一实例

当前平台通过入口 URL 中的 `session` 参数路由用户请求。浏览器不会自动将页面查询参数复制到 JavaScript、CSS、图片或 API 请求。HTML 请求成功不代表其他资源能加载。

一种实用做法是：

1. 将 JavaScript、CSS 和小图标内联到生产 HTML；Vue/Vite 项目可采用单文件构建。
2. API 使用同源相对地址，显式携带当前 `session`。
3. 保留入口 URL 的路径前缀，设置 `Referrer-Policy: no-referrer`，避免将 session 发送到外部请求或日志。

API URL 构造示例：

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

只为同源请求读取当前入口 URL 中的 `session`。不要将其复制到 `localStorage` 或 `sessionStorage`，也不要将其当作容器自行声明的计费身份。若资源保持独立，字体、图片和动态加载模块都要验证。仅设置 Vite 的 `base: "./"` 不会保留查询参数。

在本地容器直接测试 `/health`。公开 Worker 请求仍受平台会话路由约束；用户应从平台打开实例，不应直接访问裸域名。

### HTTP 200 不代表生成成功

流式响应可能在生成结束前就返回 HTTP 200。前后端应约定终止事件，例如应用可使用：

```text
event: token
data: {"content":"OK"}

event: done
data: {"model":"your-allowed-model-id"}
```

HTTP 200 响应正文中仍可能出现错误：

```text
event: error
data: {"code":"upstream_unavailable","retryable":false}
```

这些是应用层 SSE 事件示例，不是所有模型 API 的通用事件名。应明确处理成功、失败、取消和流意外终止，并在浏览器断开时关闭上游请求。

<a id="section-5"></a>
## 5. 构建镜像并在本机验证

以下 Bash/zsh 示例在自己的应用项目根目录执行。

### 构建 amd64 镜像

```bash
docker buildx build \
  --platform linux/amd64 \
  --load \
  -t my-agent:1.0.0 .

docker image inspect my-agent:1.0.0 \
  --format '{{.Os}}/{{.Architecture}} user={{.Config.User}}'
```

确认结果为 `linux/amd64`，且运行用户为非 root。即使设置 `EXPOSE 8080`，应用仍需真正监听 `0.0.0.0:8080`。

### 检查启动、页面与资源占用

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

在浏览器打开 `http://127.0.0.1:8080/`。没有模型访问能力时，页面和健康接口仍应正常；对话入口应明确提示受支持的模型接入不可用。选择规格前，除空闲内存外，还需检查启动和业务峰值内存。

### 不使用真实凭据测试流式流程

通过应用自己的测试配置提供本地模拟模型服务或等效测试工具，覆盖请求路径、模型 ID、输出片段、完成事件、上游错误、超时和取消。只使用虚假数据，不使用真实用户或开发者 Key。本地模拟成功不能证明规划中的平台代理已经可用，也不能证明生产计费隔离有效。

Docker Desktop 中的容器可通过 `host.docker.internal` 访问宿主机测试服务；Linux Docker Engine 需要配置适当的宿主机路由。容器中的 `127.0.0.1` 指向容器自身。正式发布配置不得保留模拟端点或仅供测试的覆盖项。

在生成过程中取消，确认上游调用停止，然后验证进程能在有限时间内退出：

```bash
docker stop --time 15 my-agent-local
```

页面、健康响应、业务流程、会话路由和退出行为应分别验证。端口就绪本身不能证明其他结果。

<a id="section-6"></a>
## 6. 推送到自己的外部镜像仓库

### 发布你控制的镜像

使用所选 Registry 提供的主机名、仓库路径和登录说明。公共镜像允许平台匿名拉取；私有镜像通过平台配置只读拉取凭证。本地用于推送的凭证可以具有不同权限。

替换下面全部占位值，每次发布使用新版本标签：

```bash
AGENT_REGISTRY='YOUR_REGISTRY_HOST'
AGENT_REPOSITORY='YOUR_NAMESPACE/YOUR_REPOSITORY'
AGENT_VERSION='1.0.0'
AGENT_IMAGE="$AGENT_REGISTRY/$AGENT_REPOSITORY:$AGENT_VERSION"

docker login "$AGENT_REGISTRY" --username 'YOUR_LOGIN_NAME'
docker tag my-agent:1.0.0 "$AGENT_IMAGE"
docker push "$AGENT_IMAGE"
```

密码仅在 Docker 交互提示中输入，不要写入脚本、Dockerfile、源代码、聊天记录或 Agent 环境变量。这一步推送到的是自己的 Registry，不是直接推送到平台。

### 记录并核对源 digest

记录推送输出中的 `sha256:...` digest。Tag 是方便使用的名称，digest 标识实际内容。需要时检查远端镜像：

```bash
docker manifest inspect "$AGENT_IMAGE"
```

公共镜像还应在没有保存 Registry 凭证的环境中验证访问。已登录环境拉取成功不能证明可以匿名访问。私有镜像则在平台选择已保存的只读凭证。

平台校验源镜像时固定源 digest、记录大小和架构，并触发扫描。之后移动 Tag 不会改变已绑定的 digest；新候选版本必须重新提交镜像引用并校验。

<a id="section-7"></a>
## 7. 配置、部署与提交审核

在开发者控制台打开 [Agent 部署配置](https://unexhub.ai/console/my_agents?tab=deploy)。模式 B 当前使用外部 Registry 中的单个镜像。共用表单中出现的本地归档、其他计算服务商、GPU 或 R2/D1 持久化文案，不能作为模式 B 已支持这些能力的依据。

### 填写运行配置

| 表单项目 | 示例与规则 |
| --- | --- |
| 部署模式 | 模式 B · Cloudflare 容器 |
| 镜像来源 | 外部镜像仓库 |
| 镜像地址 | 完整 `Registry/命名空间/仓库:版本`，不带 `https://` |
| Registry 凭证 | 公共镜像匿名拉取，私有镜像选择只读凭证 |
| 入口端口 | `8080`，与实际监听一致，且在 `1024–65535` 范围内 |
| 健康路径 | `/health`，必填且以 `/` 开头 |
| 启动命令 | 留空使用镜像的 `ENTRYPOINT` / `CMD` |
| 实例类型 | 必填；依据测量结果从六档中选择，例如 `basic` |
| 空闲回收 | 在平台允许范围内选择适合业务的时长，实例停止时临时文件可能丢失 |
| 自定义环境变量 | 仅非敏感应用配置，如 `LLM_MODEL` 中的允许模型 ID；明文存储，名称不以 `UNEX_` 开头 |
| 模型允许列表 | 只包含 Agent 实际需要的模型；此配置不会启用规划中的代理 |

### 按阶段完成部署

1. 创建 Agent，选择模式 B，填写完整外部镜像地址。私有镜像先保存并选择只读凭证。
2. 点击**拉取并校验镜像**，核对源 digest、大小和 `linux/amd64` 架构。校验会触发镜像扫描；生产发布需要平台启用扫描并通过扫描。
3. 配置入口端口、健康路径、实例类型、空闲时长和非敏感设置，点击**保存运行配置**。实例类型在版本发布时固定。
4. 点击**部署运行时**。平台先将已校验镜像异步搬运到 Cloudflare 镜像仓库。页面展示搬运进度或失败原因；搬运完成后，由页面触发后续 Worker/Container 部署。
5. 保持部署页面打开直到就绪。若中途离开，回来后检查状态，页面要求时重新触发部署。不要假定关闭页面后所有后续阶段都会自动完成。
6. 分别确认各阶段：**源镜像校验成功 ≠ Cloudflare 镜像副本就绪 ≠ Worker 运行时可用**。检查失败阶段的错误。平台提供开发者测试入口时，从平台打开新测试实例，验证页面、路由、业务响应和退出。可信内部兼容测试不能消除第 3 节的第三方凭据限制。
7. 扫描通过且运行时就绪后，才提交候选版本进行上架审核。普通用户只有在审核通过后才能启动。第三方模型 Agent 还必须满足第 10 节的发布前提，不能只看运行时已部署。

审核中或已发布的版本不要原地替换。应创建新候选版本，并遵循平台支持的审核流程。

### 用户启动与计费

用户从平台启动实例，平台在启动前检查访问权限、余额和预扣规则。运行时长计费从实例进入 `running` 后开始，不从开发者上传或镜像搬运时开始。审核前的镜像处理可能产生平台成本，但上传成功本身不会向终端用户计收运行时长。

用户通过平台打开和停止实例。容器运行费与模型用量费分开计算；费率、预算、结算、最长时长和退款遵循平台展示的规则。未来持久存储的费用或免费额度需要另行公示。

<a id="section-8"></a>
## 8. 版本更新与规划中的上传入口

### 按版本和 digest 更新或回滚

构建、测试并推送新版本，例如 `1.0.1`。提交镜像地址，重新校验 digest、扫描、保存对应版本的运行配置、部署，并完成所需审核。打开新实例验证发布版本。只向 Registry 推送 Tag，不会自动更改平台绑定的镜像或正在运行的容器。

回滚应使用平台支持的版本切换流程，选择上一已验证的 digest 及其匹配的运行配置。本地重新打标签不能回滚线上实例。发布记录应保留源 digest、所选实例规格、配置和验证结果。

### 规划中的三入口上传体验

下表描述目标体验。目前只有外部 Registry 入口存在，浏览器 TAR 上传与直接向平台 Docker Push 尚未提供。

| 入口 | 预期开发者体验 | 状态与边界 |
| --- | --- | --- |
| 浏览器镜像上传 | 上传 `docker save` 或 OCI Image Layout TAR，查看进度并续传中断的上传 | 规划中；通过短时权限写入私有镜像暂存区，再完成归档校验和扫描，不是用户文件工作区 |
| Docker Push 到平台 | 取得仅限当前 Agent 仓库的短期凭证，推送并检测新候选镜像 | 规划中；本文不提供当前模式 B 的平台推送端点或凭据 |
| 外部 Registry | 填完整引用，按需选择私有只读凭证，并校验镜像 | 当前入口，会保留在规划中的统一流程中；凭证不得进入用户容器 |

可在本地准备归档，用于备份或未来明确支持的导入功能：

```bash
docker save -o my-agent-1.0.0-amd64.tar my-agent:1.0.0
```

模式 B 当前没有接收该 TAR 的浏览器控件。`docker save` 包含镜像配置和层；`docker export` 是容器文件系统，两者不能互换。TAR 文件哈希与 Registry 镜像 digest 也不是同一个对象的摘要。

目标流水线是：**接收 → 校验 → 扫描 → 镜像搬运 → 运行时部署 → 可审核**。它需要可追溯的源 digest、平台副本 digest、扫描结果、实例规格和版本标识。最终应由持久后台任务推进已完成上传的后续工作，即使用户关闭页面也能继续，并提供分阶段状态与重试。以上是规划行为，不是当前依赖页面触发部署的流程。

未来上传入口必须在部署前校验所有权、大小、内容、配额和归档，拒绝不安全或被阻断的制品，并发布不可变镜像引用。短时暂存 URL 是 bearer 能力，不能代替平台鉴权。任何规划中的上传入口都不能单独证明模型隔离或用户持久存储已完成。

<a id="section-9"></a>
## 9. 常见问题排查

| 现象 | 检查与处理 |
| --- | --- |
| 本地能跑，平台失败 | 确认 `linux/amd64`、监听 `0.0.0.0`、配置端口在 `1024–65535`；检查启动日志和镜像默认命令 |
| 应用监听了其他端口 | 修改应用监听或运行配置的入口端口；`EXPOSE` 本身不会改变两者 |
| 运行时就绪，但 `/health` 返回 404 | 当前就绪只检查端口可达；修复并单独测试健康路径和业务 API |
| 没有可用的平台镜像副本 | 搬运尚未完成或失败；先检查搬运状态，再判断 Worker 部署 |
| 离开页面后部署未完成 | 返回页面检查搬运和运行时状态，必要时重新触发部署 |
| 未选择实例类型 | 审核前选择并保存六档中的一个必填规格 |
| 环境变量提示保留前缀错误 | 自定义变量名不能以 `UNEX_` 开头；不能把密钥改放到另一个明文变量中 |
| 找不到浏览器 TAR 或平台 Docker Push | 两者仍在规划中，当前使用外部 Registry |
| 旧测试镜像读不到 `UNEX_API_KEY` | 这是可信测试兼容路径的问题；不要硬编码长期 Key 或让浏览器用户填写 |
| URL 没有 `unex_agent_token` fragment | 镜像实例通常不会提供，不应要求用户粘贴 Token |
| 规划中的模型或存储虚拟地址不可用 | 对应代理与每用户工作区尚未实现，自行设置变量不会启用能力 |
| 模型请求返回鉴权或权限错误 | 在受支持的可信测试中，检查脱敏错误及平台会话、模型和预算设置；不要用共享 Key 或自报用户 ID 绕过 |
| 限流、超时或余额不足 | 限制重试次数，余额不足时停止收费重试，用户取消时结束上游请求 |
| 白屏、资源失败或 `missing_session` | 从平台重新打开，确认资源和同源 API 保留会话路由及入口路径前缀 |
| HTTP 200 但界面提示失败 | 检查 SSE 错误与终止事件，不能只看 HTTP 状态 |
| 重启后文件消失 | 容器磁盘是临时的，每用户 D1/R2 持久化尚未提供 |
| 更新后仍显示旧页面或模型 | 检查已绑定 digest、实例版本和应用设置，再打开发布版本的新实例 |

报告问题时提供 Agent ID、应用版本、镜像 digest、所处阶段、时间及所在时区、请求编号、HTTP 状态、脱敏错误和复现步骤。不要公开 Key、Authorization、完整 session URL、Registry 凭证或其他用户的数据。

<a id="section-10"></a>
## 10. 发布前检查与可复制的开发需求

### 制品与运行时检查

- [ ] 单个 `linux/amd64` 镜像以非 root 运行，在 `0.0.0.0` 监听配置端口，端口处于 `1024–65535`。
- [ ] 根页面和健康路径可用，健康路径以 `/` 开头，业务验证独立于端口就绪检查。
- [ ] 所选实例规格符合实测资源需求，并已为候选版本保存。
- [ ] 镜像层、浏览器响应和日志不含 Key；自定义环境变量非敏感且不以 `UNEX_` 开头。
- [ ] 页面、资源和 API 保留会话路由，session 不进入外部请求或浏览器存储。
- [ ] 已验证流式成功、错误、取消、超时及 SIGTERM 后限时退出。
- [ ] 容器磁盘按临时数据处理；`localStorage` 仅保存非敏感、可丢弃的界面状态。
- [ ] 平台能拉取源镜像，已记录校验后的 digest，扫描已启用且通过，Cloudflare 副本就绪，运行时可用。
- [ ] 普通用户启动前已获得审核批准；不把上传成功当作运行时计费或模型与数据隔离的验收通过。

### 第三方生产发布的额外前提

以下平台工作仍需完成，不能因为内部测试或 Worker 部署成功就勾选：

- [ ] 停止向第三方容器注入长期 `UNEX_API_KEY`，轮换受影响的旧 Key，并交付可信模型代理；验证两用户计费归属、模型权限、预算和会话停止后的撤销，包括任何旧 Token 兑换路径。
- [ ] 承诺持久数据前，交付每用户 D1/R2 工作区、可信 Storage Broker 和用户文件管理；验证跨用户拒绝、重启恢复、配额处理和明确删除。
- [ ] 提供规划中的上传入口前，验证归档拒绝、断点续传、范围受限且会过期的推送权限、不可变 digest 和分阶段恢复。

这些检查提供具体的发布证据，不能据此笼统宣称任何镜像或依赖都安全。

### 交给 AI 或开发人员的需求模板

```text
请开发一个能够部署到模式 B / Cloudflare 容器的 Agent。

名称：[填写]
用户与用途：[填写]
核心流程：[3–6 个步骤]
输入与输出：[填写]
需要的模型与持久数据：[填写，并标明当前不可用的能力]
技术栈：[已有技术栈，或 Python FastAPI + Vue]

交付要求：
1. 单个非 root 的 linux/amd64 镜像，监听 0.0.0.0:8080。
2. GET / 提供界面，GET /health 不调用模型并快速返回 200 JSON；
   平台端口就绪不能代替这些验证。
3. 不要求注入真实 UNEX_API_KEY，不使用个人或共享 Key。
   尚不可用的模型和存储接入保持禁用。规划中的虚拟代理仅在平台
   启用支持后使用；明确报错，不回退到真实 Key、其他域名或假持久化。
4. 同源请求保留 session 路由与入口路径前缀，不将 session 写入
   日志或浏览器存储。
5. 支持流式结果、明确的完成与错误、取消、请求超时及限时 SIGTERM 退出。
6. 容器磁盘按临时数据处理，localStorage 仅保存非敏感、可丢弃的
   界面状态；工作区和代理未实现时，不承诺平台 D1/R2 持久化。
7. 提供 Dockerfile、.dockerignore、README 和无需真实凭据的模拟测试，
   明确区分模拟结果与真实接入验证。
8. 提供构建、本地运行、外部 Registry tag/push 说明、实测资源需求
   和选择的平台实例规格。
9. 提供运行表单填写值和分阶段部署验证；自定义环境变量明文存储，
   必须保持非敏感。

使用当前外部 Registry 流程。浏览器 TAR 上传和直接向平台 Docker Push
尚在规划中。镜像可部署本身不代表第三方生产发布前提已经完成。
```

### 参考与适用范围

本指南反映截至 2026-09-29 的平台模式 B 基线。实例档位与用户收费按平台定义和公开价格执行。Cloudflare 的限制与价格可能变化，以下链接解释底层服务，不代表平台额外提供了对应能力：

- [Cloudflare Containers 架构与生命周期](https://developers.cloudflare.com/containers/concepts/architecture/)
- [Cloudflare Containers 镜像管理](https://developers.cloudflare.com/containers/guides/image-management/)
- [Cloudflare Containers 规格与限制](https://developers.cloudflare.com/containers/platform/limits/)
- [R2 预签名 URL](https://developers.cloudflare.com/r2/api/s3/presigned-urls/)
- [D1 Worker API](https://developers.cloudflare.com/d1/worker-api/)

Agent 开发者通过平台部署页操作。规划中的 D1/R2 binding 属于平台控制的服务，不是开发者应为容器索取的凭据。

<!-- DOCS-PAGER:START -->

---

[← 上一篇：模式 A Agent 开发](agent-development-mode-a.md) · [中文目录](README.md)
<!-- DOCS-PAGER:END -->
