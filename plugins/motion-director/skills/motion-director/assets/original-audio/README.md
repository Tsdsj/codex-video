# 原创动效音效包 · Volume 1

24 个程序合成音效，48 kHz、16-bit PCM WAV、双声道。生成源代码在技能 `scripts/build_sound_pack.py`，不依赖第三方录音、模型、API、订阅或 Python 扩展包。

打开 preview.html 逐个试听或整组串听；每个系列的 `*-reel.json` 记录串听起点。catalog.json 是各独立音效的路径、时长、设计锚点、起始增益和文件哈希。

| 系列 | 文件 | 用途方向 |
|---|---|---|
| 柔和交互 | soft-tap、felt-click | 小元素选中、轻触 |
| 柔和交互 | toggle-on、toggle-off | 开/关、状态切换 |
| 柔和交互 | select-double、quiet-dismiss | 两步确认、轻收起 |
| 空气转场 | air-pass、silk-swipe | 移动、柔和扫过 |
| 空气转场 | quick-cut、rise-soft | 短切、逐渐建立张力 |
| 空气转场 | fall-soft、reverse-bloom | 回落、反向聚拢后展开 |
| 材质触感 | wood-touch、ceramic-touch | 风格化的干燥木质、陶质落点 |
| 材质触感 | glass-tick、metal-soft | 风格化的玻璃、金属轻响 |
| 材质触感 | paper-settle、cushioned-land | 纸面收拢、缓冲到位 |
| 完成提示 | confirm-warm、complete-clear | 两段温暖确认、清晰完成 |
| 完成提示 | reveal-spark、resolve-low | 多段揭示、低调收束 |
| 完成提示 | soft-attention、brand-signoff | 温和提醒、片尾短句 |

## 选择与对齐

- 材质词表示合成声音设计方向，不是真实采样拟音。不要用于声称真实录音的场景。
- `anchor_seconds` 是设计上的主动作点，不一定是最大幅值采样。多音符提示保留前奏和尾音，避免为了对齐截掉前半段。
- 空气类通常与运动的中段/速度峰值对应，接触类与接触对应，完成类与信息确立时刻对应。不是每镜都要用。
- `suggested_gain_db=-9` 只是安全的起始衰减，需与当前视频整体混音一起调整，不是响度匹配后的固定预设。
- 输出峰值控制在约 -7 至 -9 dBFS；混音器仍要检查多轨叠加和 AAC 编码后真峰值。
- 左右差异采用幅度声像，避免用反相拓宽声场。重要信息不要依赖耳机宽度才能听清。
- 没有自动循环标记，不把衰减尾音直接拼成无限循环或环境底噪。

## 复现

```sh
python3 /path/to/skill/scripts/build_sound_pack.py /path/to/new-empty-directory
```

生成器拒绝覆盖非空目录。相同脚本/运行环境生成的 WAV 已核对一致；不承诺不同数学库和架构下逐字节一致。README 与使用说明是打包时附加的文档，生成器输出 WAV、目录与试听页。

已完成技术检查；实际音色、观感和感知同步仍需试听，不宣称这 24 个声音已经通过用户主观验收。
