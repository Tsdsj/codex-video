# 免费音效流程 1.2.0 验证

2026-10-01。只使用 CC0 本地音效、Python 标准库与已有 FFmpeg。没有付费 API、账户连接或试用额度。

## 试听交付

- preview.html：A/B 视频与 8 个原素材试听；一个开始播放会暂停其他播放器，不自动播放。
- restrained.mp4：克制版，移动/到位/完成三个事件。
- layered.mp4：层次版，增加到位时的玻璃层与展开点击。
- matched/{restrained,layered}/mix.wav：匹配响度的混音，sfx.wav 为音效分组。
- *-matched.json：最终事件和音量清单。文件绝对路径用于本机验证，插件模板用相对路径。

复用上轮 8 秒 Remotion 机制样片的视频流，替换音轨输出新文件。没有覆盖旧样片或博客成片。无背景音乐需求，因此未强行加配乐。避让能力用独立合成测试音验证，未把测试音加入成片。

两版最终编码后的综合响度均为 -25.99 LUFS，真峰值分别为 -8.36 / -8.13 dBTP。选择约 -26 仅用于这段稀疏 SFX 的比较，不是品牌视频的统一响度标准，也不建议给所有作品机械归一化。

## 已验证

- 7 项单元测试通过：帧/采样换算、非整数 fps、dB 增益、避让的进入/保持/恢复、重叠区间、淡化与非法输入。
- 实际音频集成测试通过：合成瞬态精确落在目标采样，音效叠加后峰值受控，输出时长和分组正确，拒绝覆盖。
- 避让集成测试通过：导出的音乐轨在指定区间实测衰减 12 dB，随后恢复。
- 两个最终 MP4 完整解码，各 480 帧、8 秒、1280×720、60 fps；音轨 AAC 48 kHz 双声道。
- 浏览器无头静音播放两个版本到结束，各 480 帧、0 丢帧，无媒体错误。8 个候选均可加载音频元数据。
- 技能结构、Python 语法、JSON、相对引用已校验。

## 验证边界

素材按类别、许可和技术检查选入；未实际听音，不能声称已完成主观选音、混音审美或声画感知验收。catalog.json 的最大幅值锚点只是初始估算，实际听感可能要求调整。用户可在试听页选择更合适的密度和音色。

候选之一的浮点解码峰值超过 0 dBFS；素材原文件保留，混音时先衰减，未直接以满电平叠加。

## 证据与复现

- test_audio.py、integration.py：测试。
- matched/*/report.json：WAV 真峰值和响度，音效实际起始采样与锚点。
- encoded-checks.json、*-decode.log：最终 AAC 编码复查。
- playback.json、check-preview.mjs：浏览器播放与候选素材加载结果。

混音命令：

```sh
production/tt-blog-15s/.venv/bin/python plugins/motion-director/skills/motion-director/scripts/mix_audio.py verification/audio-1.2/restrained-matched.json verification/audio-1.2/recheck-a
production/tt-blog-15s/.venv/bin/python plugins/motion-director/skills/motion-director/scripts/mix_audio.py verification/audio-1.2/layered-matched.json verification/audio-1.2/recheck-b
```

已有环境中的 imageio-ffmpeg 提供本轮 FFmpeg。verification 中的测试使用本机 Playwright 路径；插件源码及资产没有这些机器路径。Kenney 原包仅留作来源证据，插件只分发 8 个候选与原许可。
