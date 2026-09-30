# Remotion 起步工程

8 秒 / 1280×720 / 60 fps 的原创机制样片，用于验证帧时钟、主体运动、辅助层错相、局部 Sequence、稳定阅读与输出。画面采用简洁纸色和绿色图形，仅为示例，不是插件强制的品牌风格或物理仿真。

复制整个文件夹到用户项目的空目录，再运行（Node >=22.18）：

```sh
npm ci
npm run check
npm test
npm run render
npm run studio
```

`render` 先生成原创合成提示音，再渲染关键帧和 `out/motion-study.mp4`。`npm run render -- --silent` 输出静音版本。Studio 启动前会自动生成提示音；需要静音预览时将默认 props 的 sound 设为 false。

所有 Remotion 包锁定到 4.0.531；npm lockfile 随模板提供。Remotion 可能下载专用无头浏览器。已有兼容 Chromium 可通过 `REMOTION_BROWSER_EXECUTABLE` 指定，本机路径不写入工程。

## 复用部分

- `src/motion.ts`：精确拍点、端点平滑的停靠运动、纯函数帧状态。
- `src/scene.tsx`：画面与时间分离、局部帧文字、克制辅助回稳。
- `scripts/render.mjs`：本地 bundle、Composition 选择、关键帧和 H.264 导出。
- `scripts/sound.mjs`：仅用于事件对齐的原创合成音，不是正式音乐混音。
- `src/motion.test.ts`：拍点累计误差、端点速度、非顺序求帧及阅读停留检查。

`out/frame-180.png` 与 repeat 文件用于核对同帧重复渲染。不同 OS 的 Arial/字体渲染可能不同，正式作品需固定有授权的字体。新视频需重做 Brief 与具体视觉，不要只替换标题就声称完成设计。

本模板的源代码可用于用户自己的视频项目；第三方依赖遵循各自许可，尤其是 [Remotion 许可](https://www.remotion.dev/docs/license)。不附带第三方图片、音乐或付费服务。
