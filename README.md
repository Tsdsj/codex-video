# 动效视频导演 · Codex 插件

基于[观默的动效视频文章](https://x.com/guanmo_ai/status/2105146205915283737)独立整理的本地插件。它提供可执行的制作方法，不是独立视频生成模型或渲染引擎。

1.1.0 增加 Remotion 专用制作指南、视觉与运动判断，以及可复制运行的 Remotion 4.0.531 工程。包含导演 Brief、分镜和节拍组织、运动因果、声画事件、可复现渲染指导，以及技术和视听验收清单。没有 MCP 服务、自动执行 hooks 或付费接口。

## 使用

安装后新开 Codex 聊天，调用 `$motion-director`，或在插件选择器搜索“动效视频导演”。

> 用 $motion-director 为我的产品制作一支 15 秒宣传片。先整理 Brief、分镜和可查看的关键画面，设计确认后再制作成片。

已有确认分镜可以直接要求实施；只需审查时可以要求按时间码分析现有视频。具体制作仍依赖项目可用的渲染和媒体工具。

## 本地安装、更新和移除

本项目作为本地 marketplace，由 Codex CLI 安装用户级插件：

```sh
codex plugin marketplace add /Users/tt/projects/codex-video
codex plugin add motion-director@tt-motion-local
codex plugin list --marketplace tt-motion-local --json
```

修改源文件后重新安装并新开聊天；若桌面目录未刷新，重启 Codex。安装缓存由 Codex 管理，不手工编辑。市场源路径需要保留以便更新。

```sh
codex plugin remove motion-director@tt-motion-local
codex plugin marketplace remove tt-motion-local
```

## 文件

- `plugins/motion-director/skills/motion-director/SKILL.md`：技能入口。
- `references/`（在技能目录内）：制作模板、验收清单、来源与整理边界。
- `.agents/plugins/marketplace.json`：本地市场清单。
- `plugins/motion-director/.codex-plugin/plugin.json`：Codex 插件清单。

来源正文经公开读取入口取得，嵌图与示例视频未验证；没有复制作者素材或完整提示词。插件没有把代码量、模型优劣、费用等经验性描述当作保证。

安装格式参考 [OpenAI 插件文档](https://developers.openai.com/plugins/build/plugins)。

## Remotion 集成（1.1.0）

新建视频可使用插件内 `skills/motion-director/assets/remotion-starter/`，复制到作品目录后运行 `npm ci`、`npm run check`、`npm test`、`npm run render`。已有视频工程不强制迁移。

建议请求：“用 $motion-director 和 Remotion 制作视频，先做关键视觉与运动设计，确认后按帧实现和渲染。检查构图主次、动作因果、稳定阅读时间和声画同步。”

Remotion 是本地渲染依赖，安装时需要下载包和浏览器；商业使用遵守其许可。插件不新增云端渲染服务或订阅。样片与验证记录见 `verification/remotion-1.1/`，现有博客视频保持不变。

## 免费音效流程（1.2.0）

继续调用 `$motion-director` 即可。有声任务会读取声音设计指南，使用本地免费素材与混音工具，无 API Key、试用额度或订阅。新增 8 个保留 CC0 许可的候选素材、事件清单、Python + FFmpeg 本地分轨混音器。

见插件 `references/sound-design.md`（技能目录内）。该流程支持采样级锚点、裁剪淡化、分组音量、显式避让包络、峰值保护与响度测量。实际听感须另行试听，不由技术指标代替。

验证与 A/B 成片位于 `verification/audio-1.2/`。原有博客视频与 Remotion 样片不覆盖。Remotion 渲染软件自身的许可条件仍适用，本次免费约束针对音效素材和处理链路。

## 原创音效扩展（1.3.0）

新增四组共 24 个原创合成音效：柔和交互、空气转场、材质触感、完成提示。与原 8 个 Kenney 候选并存，共 32 个。独立 WAV、目录、试听页和可复现生成器均随插件分发。

试听页位于 `plugins/motion-director/skills/motion-director/assets/original-audio/preview.html`；分组下载包位于 `dist/`。音效技术检查通过，听感待用户试听；材质名称代表风格化合成方向。
