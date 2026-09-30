# tt-blog · 信号，在线。

2026-10-01，按用户确认的五镜头方案制作。15 秒，16:9，1920 × 1080，30 fps，450 帧。

## 交付

- `tt-blog-15s.mp4`：有声版本，H.264 High / yuv420p + AAC 48 kHz stereo，约 3.1 MiB。
- `tt-blog-15s-silent.mp4`：静音版本，约 2.8 MiB。
- `preview.html`：视频播放器、下载链接、0–449 帧检查滑块。直接用浏览器打开；不依赖网络。
- `frames/`：从最终有声 MP4 解码出的 450 张 JPEG，每张对应一个实际输出帧。文件编号为帧号 + 1。
- `motion.js`、`scene.html`、`render.mjs`、`sound.py`：确定性动效、场景、导出和原创声音源。
- `checks/technical.json`、`checks/decode.log`、`checks/playback.json`：技术验证证据。

## 实现

沿用已确认 Signal 构图、字色、作品及文章内容。开场点阵使用固定 Fibonacci 分布的 10,500 个点进行聚拢与旋转，不使用每次不同的随机数。城市图像微推 4%，玻璃窗口平移 48px 回稳；文章卡片承接演示窗口；片尾线条先收拢再横向展开。网址从 f378 起稳定保留至 f449。

所有视觉状态由 `renderFrame(frame)` 控制，30 fps 逐帧截图编码，不依赖录屏的实时运行速度。文字、窗口与底栏分别设定进出时机，修正了初版转场中的标题叠影。镜头仍沿用已确认顺序和时长，转场在镜头边界附近重叠。

声音为 `sound.py` 原创合成：低电平氛围层，以及 f12 / f189 / f378 附近的信号、就位、确认音。不含旁白、不引用商业音乐。声音总长 15 秒，尾部淡出。

## 本机复现

在 `/Users/tt/projects/codex-video` 执行，以下为本次实际使用的命令：

```sh
python3 production/tt-blog-15s/build-scene.py
python3 production/tt-blog-15s/sound.py
node production/tt-blog-15s/render.mjs
production/tt-blog-15s/.venv/bin/python production/tt-blog-15s/verify.py
node production/tt-blog-15s/check-playback.mjs
```

运行环境：Node 24.18.0、Python 3.14.6、Playwright 1.63.0、imageio-ffmpeg 0.6.0（所带 FFmpeg 7.1）。使用已有 tt-site 的 Playwright/Chromium；未改动或安装到博客项目。仅在本视频工程 `.venv` 安装编码工具：

```sh
uv venv production/tt-blog-15s/.venv
uv pip install --python production/tt-blog-15s/.venv/bin/python -r production/tt-blog-15s/requirements.txt
```

现有脚本中的 Playwright 导入指向 `/Users/tt/projects/tt-site/node_modules/playwright/index.mjs`。换机器时需改为对应安装路径，并安装相同版本。场景构建依赖 `../../design/tt-blog-15s/keyframes.html` 与 assets；迁移时一起保留 `design/tt-blog-15s`。中文为本机 PingFang SC，换系统需固定字体后重新检查排版；不声称跨机器逐像素一致。

## 验收结果

| 项目 | 结果与证据 |
|---|---|
| 分辨率、时长、帧数 | 通过：1920 × 1080，15.00 秒，30 fps，完整解码 450 帧 |
| 编码、音轨 | 通过：H.264 / yuv420p，AAC 48 kHz 双声道 |
| 完整解码 | 通过：FFmpeg 退出码 0；blackdetect 指定阈值下无黑场区间 |
| 页面播放 | 通过：无头 Chromium 以 1 倍速静音播放至 ended，450 帧、0 丢帧、无媒体错误；此结果限本机浏览器 |
| 关键画面 | 已实际检查首尾帧、代表帧和转场邻域；修正容器遮挡、文字叠影与抢眼的片尾斜线 |
| 精确逐帧预览 | 通过：滑块 F263 对应 8.767 秒实际解码帧，非近似视频 seek |
| 音频技术检查 | 通过：15 秒完整音轨，解码峰值约 -18.01 dBFS，无削波；事件包络与帧时间绑定 |
| 听感、主观声画同步 | 未验证：浏览器回放保持静音，当前工具没有实际听音证据，不将波形与时间检查等同于听感验收 |

本轮未发布视频、未改动线上博客。素材来源与字体许可证见设计目录的 storyboard.md 和 assets/FONT-LICENSE.md；原项目截图继承其素材授权范围。
