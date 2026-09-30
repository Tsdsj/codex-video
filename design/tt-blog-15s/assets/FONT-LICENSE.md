# 字体来源与授权

全部字体自托管，运行时不请求任何外部字体服务。更新方式：`pnpm fonts`（见 `scripts/fetch-fonts.ts`）。

| 文件 | 字体 | 来源 | 授权 |
|---|---|---|---|
| `clash-display-500.woff2` · `clash-display-600.woff2` | Clash Display | [Fontshare](https://www.fontshare.com/fonts/clash-display)（Indian Type Foundry） | ITF Free Font License，可免费商用与自托管 |
| `satoshi-400.woff2` · `satoshi-500.woff2` · `satoshi-700.woff2` | Satoshi | [Fontshare](https://www.fontshare.com/fonts/satoshi)（Indian Type Foundry） | ITF Free Font License，可免费商用与自托管 |
| `jetbrains-mono-latin-wght.woff2` | JetBrains Mono（可变字体，latin 子集） | npm `@fontsource-variable/jetbrains-mono` | SIL Open Font License 1.1 |

中文不下发字体，回退到系统黑体：`PingFang SC, HarmonyOS Sans SC, Microsoft YaHei`。
