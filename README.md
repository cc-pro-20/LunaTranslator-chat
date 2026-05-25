# LunaTranslator

基于 [LunaTranslator](https://github.com/HIllya51/LunaTranslator) 实现的游戏/软件实时双向翻译工具，专注于提供流畅的跨语言游戏体验。

## 核心功能

- **文本钩取** — 通过 DLL 注入直接截获游戏文本输出（支持 DirectWrite、Win32 GDI、Unity 等引擎），零延迟获取游戏内文字
- **OCR 识别** — 对于无法注入的游戏，支持截图 + OCR 文字提取（本地 ONNX 引擎 + 多家云服务）
- **屏幕镜像** — 集成 Magpie 工具，支持 UWP/应用窗口画面捕获
- **实时翻译** — 支持 50+ 翻译引擎，涵盖大模型、云 API、免费在线接口
- **双向翻译** — 中日/中英等多语种互译，适配大多数游戏场景

## 翻译引擎

| 类型           | 引擎                                                         |
| -------------- | ------------------------------------------------------------ |
| **大模型**     | OpenAI / ChatGPT、Claude、Gemini、SakuraLLM（专为日→中小说/游戏翻译优化）、本地 llama.cpp |
| **云 API**     | 百度翻译、阿里云、腾讯云、有道、微软、Google Cloud、DeepL、彩云、Papago、Yandex、火山、华为云、小牛 |
| **免费在线**   | Google 翻译、Bing、有道词典、Dreye、QQ 翻译、ModernMT 等     |
| **浏览器集成** | Chrome AI（调用浏览器内置 AI）、CDP ChatGPT Mirror           |
| **自定义扩展** | 支持用户自建翻译模块                                         |

## 系统要求

- **操作系统**: Windows 10 1803+ (x64) / Windows 11
- **运行时**: 无需额外安装 Python，程序自带 Python 3.13 运行时
- **权限**: 进程注入功能需要管理员权限（`LunaTranslator_admin.exe`）

## 快速开始

1. 下载解压后直接运行 `LunaTranslator.exe`
2. 若需文本钩取功能，右键 → **以管理员身份运行** `LunaTranslator_admin.exe`
3. 在设置中配置翻译引擎（首次使用建议选择免费引擎如 Google 翻译或 Bing）
4. 选择目标游戏进程，开始自动翻译

> **提示**: 使用大模型翻译时，需在设置中填入 API 地址和密钥。支持所有兼容 OpenAI API 格式的服务。

## 配置说明

所有配置文件位于 `userconfig/` 目录：

| 文件                     | 说明                             |
| ------------------------ | -------------------------------- |
| `config.json`            | 主配置（语言、显示、快捷键等）   |
| `translatorsetting.json` | 翻译引擎配置（API 密钥、端点等） |
| `ocrsetting.json`        | OCR 引擎配置                     |
| `postprocessconfig.json` | 文本后处理规则                   |

## 鸣谢

- [LunaTranslator](https://github.com/HIllya51/LunaTranslator) — 原始项目
- [SakuraLLM](https://github.com/SakuraLLM/SakuraLLM) — 日→中翻译专用大模型
- 所有翻译引擎 API 提供方

## 许可证

本项目基于原 LunaTranslator 项目，各第三方组件的许可证详见 `LICENSES/` 目录。
