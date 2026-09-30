# Remotion 1.1 集成验证

2026-10-01。独立工程位于 `starter/`，未修改既有博客视频。

- 依赖：Remotion 全套 4.0.531、React 19.1.0、Node 24.18.0；已保存 npm 锁文件。
- 类型检查通过，4 项运动测试通过：非整数拍点无累计漂移、轨迹端点平滑、30/60 fps 非顺序求帧一致、片尾稳定停留。
- 实际导出 `starter/out/motion-study.mp4`：8 秒、1280×720、60 fps、480 帧，H.264 + AAC。
- FFmpeg 完整解码退出码 0，无指定阈值下的黑场，音频峰值约 -24 dBFS。
- Chromium 无头正常速度静音播放到 ended，480 帧，丢帧 0，无媒体错误。限于本机环境。
- F180 在非顺序抽帧后再次渲染，PNG 字节一致。
- 实际查看 F120、F210、F330，修正主体消失后残留的阴影，以及球体的高光方向。最终构图可读，卡片与标题层次明确。
- 这是机制验证样片，不是用户审美验收通过的宣传片。完整主观运动评价和实际听感未验证，不能把无头播放与音频峰值当作这些证据。

实际执行：`npm run check`、`npm test`、`npm run render`，以及此目录的 `check.mjs` 与 FFmpeg 全量解码。`check.mjs` 复用了本机既有 Playwright 路径，不随插件分发；插件模板没有本机绝对路径。

证据：`technical.json`、`decode.log`、`playback.json`、`starter/out/render.json`、关键帧 PNG。

播放样片：打开 `starter/out/preview.html`，或直接打开 MP4。模板源码在插件的 assets/remotion-starter 内，不包含 node_modules、视频和验证日志。
