# Aider

[文档目录](README.md) · 简体中文 | [English](../en/aider.md)

适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

Aider 是终端编程助手。它支持自定义 OpenAI 兼容接口，本页使用 UNEXHub 的 Chat Completions 地址。

## 1）安装 Aider

按照官方安装器方式，在已有 Python 的终端执行：

```bash
python -m pip install aider-install
aider-install
aider --version
```

macOS / Linux 若只有 `python3` 命令，将第一行改为 `python3 -m pip install aider-install`；Windows 使用 Python Launcher 时可执行 `py -m pip install aider-install`。官方安装器会为 Aider 创建独立环境。安装后找不到命令时重开终端并检查 Python scripts 目录是否在 PATH。

## 2）设置 API 地址和密钥

创建专用 UNEXHub Key，例如 `aider-test`。macOS / Linux：

```bash
export OPENAI_API_BASE='https://api.unexhub.ai/v1'
export OPENAI_API_KEY='YOUR_API_KEY'
```

Windows PowerShell：

```powershell
$env:OPENAI_API_BASE = "https://api.unexhub.ai/v1"
$env:OPENAI_API_KEY = "YOUR_API_KEY"
```

Aider 的配置名是 `OPENAI_API_BASE`。替换密钥占位符，地址写到 `/v1`。

## 3）指定模型并启动

进入测试项目目录，执行：

```bash
aider --model openai/YOUR_MODEL_ID
```

`openai/` 是 Aider／LiteLLM 的提供商前缀，后面才是 UNEXHub 的准确模型 ID。不要因为模型来自其他品牌就移除本教程所用的兼容提供商前缀。

## 4）可选：保存非敏感配置

在用户级 `~/.aider.conf.yml` 保存：

```yaml
model: openai/YOUR_MODEL_ID
openai-api-base: https://api.unexhub.ai/v1
```

Key 继续通过环境变量提供。配置文件中替换准确 ID，合并已有配置即可。Aider 不认识某模型时可能提示上下文或价格信息缺失，这不直接说明 API 不可用；费用按 UNEXHub 实际记录核对。

## 5）测试对话

在 Aider 交互界面输入：

```text
/ask Reply with one short greeting. Do not edit files.
```

收到回复后，再添加需要协作的文件并进入编辑工作流。辅助模型、提交消息生成或其他自动任务可能增加请求，检查当前配置中的模型选择。

## 6）查看费用

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

## 参考资料

- [PoloAPI](https://poloapi.apifox.cn/9111349m0)
- [Aider installation](https://aider.chat/docs/install.html)
- [OpenAI-compatible API configuration](https://aider.chat/docs/llms/openai-compat.html)
