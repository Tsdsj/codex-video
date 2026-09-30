# Remotion 制作指南

适用于用户选择 Remotion 或新建代码驱动的视频工程。此文是本插件的整合建议，不是官方技能的复制品。Remotion 解决可编程时间线与渲染；审美仍由 Brief、画面设计和回放判断决定。

## 建立工程

1. 检查 Node、现有 package.json、锁文件和 Composition。已有工程复用入口，不在旁边重复搭建。
2. 新项目可复制本技能 `assets/remotion-starter/` 到用户工程下的新目录，运行 `npm ci`。不要复制已有 node_modules；不直接改插件缓存。
3. 模板验证版本为 Remotion 4.0.531。所有 remotion / @remotion/* 包使用完全一致的版本并保留锁文件。已有项目保持已验证版本，升级作为明确动作处理。
4. `npm run studio` 用于人工预览；`npm run check`、`npm test`、`npm run render` 用于检查和输出。默认本地渲染，不引入 Lambda、账号或云端费用。
5. 初次依赖安装与浏览器准备可能需要联网；不要把本地渲染称为零依赖或永远免费。商业使用前核对 [Remotion 当前许可](https://www.remotion.dev/docs/license) 与[价格条件](https://www.remotion.dev/pricing)，不硬编码旧价格。

起步工程是八秒机制验证样片，不是所有产品的视频模板。复用时间函数和渲染链，按已确认设计重新组织构图、文案、色彩和运动。

## 时间与镜头

- Composition 定义画幅、fps、总帧数；所有运动取自 `useCurrentFrame()` 和 `useVideoConfig()`。禁止 CSS animation/transition、setInterval、墙钟或依赖上一个渲染帧的累积更新。
- `Sequence from={...}` 内的 `useCurrentFrame()` 是局部帧号。不要再次减去全局起点；需要全局帧时从父组件显式传入。
- 镜头拆成组件，镜头内部再分主体、辅助层、文字与相机；共享主时钟但参数和相位独立。
- 编排表使用 `[start,end)`，`durationInFrames=end-start`；渲染器 `frameRange` 是包含两端的 `[start,end-1]`，转换时明确处理差一帧。
- 跨镜头保留身份的主体不要在两个 Sequence 内分别从初始状态弹出；可放在父级持续渲染，用同一条轨迹跨越边界。
- 用 `TransitionSeries` 时，总时长减去重叠 transition 帧数；转场不能长于相邻片段，不能连续放两个 transition。简单连续运动不必引入转场包。

## 选择运动机制

| 表达目标 | 合适的机制 | 要检查的失败 |
|---|---|---|
| 阅读信息、淡入、遮罩展开 | 有边界的 interpolate / 明确缓动 | 文案提前消失、opacity 越界 |
| 实物受力后的回稳 | spring，按材质调 damping/stiffness/mass | 文字和背景一起弹、无能量来源的过冲 |
| 物体从 A 到 B 后停住 | 端点平滑的轨迹 | 停止瞬间速度突变 |
| 不停顿地经过多个点 | 连续样条或 Hermite 轨迹并传递速度 | 每段都 ease-in-out 导致走走停停 |
| 飞行、碰撞 | 显式受力、接触时刻与分段解析状态 | 穿地、阴影脱离、形变先于接触 |

`spring()` 输出可能超出 0–1：位置可以有设计过的过冲，透明度或合法区间内的数值需要限制。不要把物理参数写成统一“高级预设”；先按对象用途选择是否弹，再调参数。`durationInFrames` 会改变时间分布，不能等同于真实物理常量。

模板的 quintic travel 在端点速度与加速度归零，适合“移动后停住”；不适合跨段保速。模板中 spring 仅用于辅助回稳，不能把模板的短片当作真实碰撞仿真。

## 资产、文字与声音

- 本地素材放 `public/`，用 `staticFile()` 引用；图片用 Remotion 的 `Img` 等能参与加载等待的组件。
- 字体固定到项目并等待加载后导出；Canvas 绘制或异步数据用对应加载屏障，失败应明确抛错并清理等待，不无限增加超时。
- 随机分布用固定种子或 Remotion `random(seed)`；每帧不得重新随机。
- 已安装版本的 Audio / Html5Audio / OffthreadVideo 等接口以该版本官方文档为准。裁剪、Sequence 起点及音量回调的帧坐标分别核对。
- SFX 瞬态对准事件帧，补偿素材前导静音；音乐/旁白淡入淡出在自己的局部帧上计算，音量不要突跳。模板合成音仅为事件定位示例，不等于正式配乐。
- 添加动态模糊、颗粒或 3D 前，先在小段渲染中检验性能、文字清晰度和真实收益。不要默认安装所有 Remotion 扩展。

## 交付门槛

先渲染代表镜头或低分辨率整片，检查正常速度，再做正式输出。高风险帧包括边界、峰值速度、接触、最大形变和文字交接。重复以不同顺序渲染同一帧，确认没有依赖运行次序的状态；同机像素一致不能扩展为跨机器承诺。

最终检查实际 MP4 的解码、分辨率、时长和帧数；浏览器播放、静帧检查、听音分开记录。静帧复核只证明构图，不证明节奏。`check` 与单元测试不能代替视听验收。

## 官方文档（2026-10-01 核实）

- [逐帧动画](https://www.remotion.dev/docs/animating-properties)、[避免闪烁](https://www.remotion.dev/docs/flickering)
- [spring](https://www.remotion.dev/docs/spring)、[Sequence](https://www.remotion.dev/docs/sequence)
- [TransitionSeries](https://www.remotion.dev/docs/transitions/transitionseries)
- [renderMedia](https://www.remotion.dev/docs/renderer/render-media)、[renderStill](https://www.remotion.dev/docs/renderer/render-still)
- [音量](https://www.remotion.dev/docs/audio/volume)、[Audio](https://www.remotion.dev/docs/media/audio)
- [官方 Agent Skills](https://www.remotion.dev/docs/ai/skills)：如环境已安装可协同使用，只读取当前任务相关规则；本插件不依赖它必须存在，也不自动全局安装另一套技能。
