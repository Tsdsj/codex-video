# 免费本地声音流程

本插件当前只采用免费音频来源和本地处理。不要以免费试用、赠送额度为由接入付费服务；不请求 ElevenLabs 等 API Key。现有视频渲染软件仍遵守它自身的许可，本规则不改变 Remotion 的许可条件。

## 先设计声音，再选文件

从分镜读取事件，不给每个运动都配声音。列出：事件帧、物体材质/重量、情绪、声音功能（预备、接触、完成或环境）、重要性、需要保留的静默区间。声音不应比画面更夸张，品牌短片尤其避免混搭大量游戏提示音。

选择顺序：用户已有且授权清楚的本地素材 → 本插件原创合成/CC0 候选 → 其他可核验的免费素材 → 定制原创程序合成。复杂拟音不能靠几个正弦波假装真实，缺少合适素材应明确说明并换用克制表达。没有配乐需求就不强加背景音乐。

## 候选素材与试听

内置两个素材目录：`assets/original-audio/` 是 24 个原创合成音效（柔和交互、空气转场、材质触感、完成提示），见 [原创包说明](../assets/original-audio/README.md)；`assets/audio/` 包含 8 个 Kenney Interface Sounds 候选。原创包使用 `anchor_seconds` 设计锚点，Kenney 目录使用 `estimated_anchor_seconds` 估算锚点，选取后统一填入混音清单的 `anchor_seconds`。读取 `catalog.json` 查看时长、文件哈希、许可和建议用途。它们按文件类别选入，未经过实际听感筛选，不声称全部适合某个品牌。

`estimated_anchor_seconds` 是最大绝对采样值的位置，仅用于初始对齐，可能不是感知起音或正确撞击点。应结合波形与试听校正；多段提示音不能简单把最大峰值当第一声。保留尾音，不在任意采样点生硬截断。

用浏览器/播放器展示候选和画面，用户明确选择过的声音可以复用。工具没有听音能力时，把试听状态标记为未验证，并交付可听的预览；不能根据文件名、峰值或解码成功宣布音色高级。

## 本地混音

使用 `scripts/mix_audio.py`。只需要 Python 标准库和 FFmpeg；若没有系统 FFmpeg，可在项目隔离环境使用免费的 `imageio-ffmpeg`，不要改全局 Python。已存在可用 FFmpeg 时直接复用。

将候选素材和 `example-cues.json` 复制到作品目录，编辑清单。不要在插件缓存内输出作品。

```sh
python3 /absolute/path/to/skill/scripts/mix_audio.py cues.json out/audio-v1 --ffmpeg /path/to/ffmpeg
```

无系统 FFmpeg 时的可选隔离环境：

```sh
uv venv .audio-venv
uv pip install --python .audio-venv/bin/python imageio-ffmpeg==0.6.0
.audio-venv/bin/python /absolute/path/to/skill/scripts/mix_audio.py cues.json out/audio-v1
```

这些是命令示例，替换为实际技能与项目路径。已经验证的本机路径不要硬编码进可分发工程。

### 清单字段

- `fps`、`duration_seconds`：与视频一致，短片最长 300 秒。脚本按 48 kHz 双声道处理。
- `cues[].file`：相对清单的本地文件路径，也接受绝对路径；不接受远程 URL。
- `event_frame`：希望音效锚点到达的视频帧，帧号从 0 开始。
- `anchor_seconds`：**裁剪后**音效内部的锚点；起始采样位置为 `round(event_frame*48000/fps)-round(anchor_seconds*48000)`。
- `trim_start_seconds` / `trim_end_seconds`：原素材的裁剪范围。
- `gain_db`：单音效增益；默认 0。建议先衰减，听过后再调，不能统一假定原素材电平。
- `role`：`sfx`、`music`、`ambience` 或 `voice`；`bus_gain_db` 可统一调每组。
- `fade_in_seconds` / `fade_out_seconds`：剪口淡化，默认 3 ms / 25 ms；瞬态素材需要减少淡入，但不应产生剪口爆音。
- `master_ceiling_db`：默认 -3 dBFS。只在必要时整体衰减，不向上归一化，不宣称它是 true-peak limiter。
- `ducks`：显式音量避让区间，如 `{ "start_frame": 60, "end_frame": 120, "gain_db": -10, "attack_seconds": 0.08, "release_seconds": 0.25, "roles": ["music", "ambience"] }`。区间重叠取最强避让，不相乘。这是离线包络自动化，不是实时侧链检测。

输出 `mix.wav`、存在的分组 WAV、`report.json`。拒绝覆盖已有 mix；迭代使用新目录。超出片头片尾的音效会截断并报告，必须检查是否误切瞬态或尾音。总混音和分组共享必要的衰减，避免单独导出的分组削波。

## 接入 Remotion

把输出 WAV 复制到作品 `public/audio/`，使用该工程当前版本的音频组件加载，从第 0 帧开始。不要再叠加旧合成音、旧 SFX 或重复音乐。混音清单 fps 必须与 Composition 相同，改 fps 后重新计算音效。

验证用已渲染视频也可用 FFmpeg 替换音轨：明确映射原视频流和新音轨，避免同时保留旧音。先检查两者时长；输出新文件，不覆盖已交付作品。正式 MP4 编码后再做音频检查。

## 混音与验收

先使主体音效和语音清晰，再加环境和配乐。语音/关键事件出现时让音乐适度降低，避免突然抽吸。无需旁白的短片不强行创建 Voice 轨。

报告中的 `input_i` 是已输出 WAV 的综合响度（LUFS），`input_tp` 是测得真峰值（dBTP）；静音可能显示 `-inf`。短且稀疏的 SFX 轨不应机械追求 -14 LUFS。响度目标由投放和内容决定，不能用响度处理代替逐轨平衡。

交付前检查：原素材与最终编码可解码、输出时长、锚点对齐、削波/真峰值、剪口、单声道兼容性，以及正常速度实际试听。脚本不验证主观听感，也不自动证明单声道兼容；缺少对应证据要标注。

审美不确定时，用同一画面做少量 A/B：例如少事件的克制版与增加材质层的层次版。先匹配感知响度并核对峰值，避免只是把 B 调响；保留分轨和清单以便只调整有问题的部分。

## 来源与范围

- [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds)：CC0；原许可随素材保留，2026-10-01 取得。
- [Remotion 音频规则](https://github.com/remotion-dev/remotion/blob/main/packages/skills/skills/remotion-markup/audio.md)：用于接入与时间线参考。
- [FFmpeg Filters](https://ffmpeg.org/ffmpeg-filters.html)：解码、混音处理与 loudnorm 测量参考。

本流程独立编写；未复制社区技能代码，未附带商业音效、付费模型或生成服务。32 个音效也不等于完整电影音效库；原创包不包含真实环境录音、语音或完整配乐。
