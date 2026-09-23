# CC Switch

[文档目录](README.md) · 简体中文 | [English](../en/cc-switch.md)

适用站点：[UNEXHub](https://unexhub.ai/) · 文档更新：2026-09-23

CC Switch 用来管理 Claude Code、Codex 等工具的服务商配置，也提供本地协议转换。它本身不是模型服务，调用仍需 UNEXHub Key 和可用模型。

## 1）安装 CC Switch

从 [官方 Releases](https://github.com/farion1231/cc-switch/releases)下载对应系统安装包。macOS 也可使用：

```bash
brew install --cask cc-switch
```

先安装你要使用的 [Claude Code](claude-code-install.md)或 [Codex](codex-install.md)，再打开 CC Switch。更换配置前，保留原有服务商配置，便于恢复。

## 2）添加 UNEXHub 服务商

选择目标应用页签 → Add Provider → Custom，名称填 `UNEXHub`，填写专用 API Key。若表单提供模型列表获取，获取失败时可手动填写准确模型 ID。

地址按目标应用和接入模式区分：

| 目标与模式 | 配置地址 | 上游协议 |
| --- | --- | --- |
| Claude Code 直连 | `https://api.unexhub.ai` | Anthropic Messages，需先确认开放。 |
| Codex 直连 | `https://api.unexhub.ai/v1` | Responses，需先确认开放。 |
| 本地转换到 UNEXHub 聊天接口 | 使用下述完整 URL 模式或检查客户端拼接结果。 | Chat Completions。 |

不要把「Base URL 一律不加 `/v1`」当成所有应用通用规则。检查最终生效配置，直连 Codex 示例见 [Codex](codex.md)，直连 Claude 示例见 [Claude Code](claude-code.md)。

## 3）Claude Code：将 Chat Completions 转为 Messages

如果上游只有 Chat Completions：

1. 在 Claude 服务商高级选项中，将 **API Format** 设为 **OpenAI Chat Completions**。
2. 在支持 **Full URL Mode** 的版本中启用该选项，地址填 `https://api.unexhub.ai/v1/chat/completions`。未使用完整 URL 模式时，按照该版本的路径拼接规则填写前缀，确保最终到达同一端点。
3. 填写真实上游模型 ID；如有主模型与辅助模型映射，都使用当前可用模型。
4. 保存并启用服务商，启动本地代理，开启 **Claude Code takeover**（接管），再重新启动 Claude Code。

转换必须由运行中的本地代理处理。只保存服务商但未启动代理和接管，不能完成协议转换。

## 4）Codex：将 Responses 转为 Chat Completions

1. 切到 Codex 服务商，添加或编辑 UNEXHub 配置。
2. 开启 **Needs Local Routing**。
3. 在 **Model Mapping** 中填写 UNEXHub 实际模型 ID，显示名称可自定义。
4. 按当前版本的上游地址设置配置 UNEXHub；支持完整 URL 模式时可填完整聊天端点，最终请求应到达 `/v1/chat/completions`。
5. 启动本地路由并开启 **Codex takeover**，启用服务商后重新启动 Codex，使模型列表更新。

本地代理负责把 Codex 的 Responses 请求转换成上游 Chat Completions。使用期间保持 CC Switch 的代理运行；本地代理地址由工具生成，不要手动固定成别人的端口。

## 5）验证与恢复

在目标工具中发送「只回复一句问候，不读取或修改文件」。确认 CC Switch 请求记录和 UNEXHub 日志都能找到该调用。

工具调用、推理内容和流式转换依赖 CC Switch 版本及上游模型。文本成功后再验证需要的工作流。如果不再使用本地代理，先通过 CC Switch 关闭接管并恢复原服务商配置，再退出代理。

## 6）查看计费

记录本次调用的时间、Key 名称和模型 ID，打开 [UNEXHub 调用日志](https://unexhub.ai/console/log)，按这些条件筛选，再进入「详情 → 计费详情」核对「最终扣费」。自动重试、辅助模型和多轮工具调用可能产生多笔请求。账单导出见[计费记录与导出](billing.md)。

CC Switch 的本地用量统计便于定位，最终消费仍以 UNEXHub 记录为准。此处配置 UNEXHub API Key，不需要切换到其他服务商的订阅或 OAuth 接入。

## 参考资料

- [PoloAPI](https://poloapi.apifox.cn/9111176m0)
- [CC Switch](https://github.com/farion1231/cc-switch)
- [Provider manual](https://github.com/farion1231/cc-switch/blob/main/docs/user-manual/en/2-providers/2.1-add.md)
