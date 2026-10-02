# Launch notes / 首发建议

## Positioning

**Paper Video Classic — explain the idea, keep the evidence.**

中文一句话：**让论文留在画面里，把复杂机制讲清楚。**

不宣传“全自动一键读懂任何论文”，不声称速度/质量提升百分比。展示确实能运行的原文定位、渐进画线、教学层和原生语音对齐。

## Repository front page

1. 标题和一句话说明。
2. 先放短动图，再放安装命令。
3. 三个具体特点：原文不丢、重点有真实坐标、音画用同一时间轴。
4. 可复现样例、Agent Skill、能力边界及许可。
5. 作者 Thomas Li 的简洁署名。个人账号链接在发布前确认，不猜用户名或借用公司标识。

“Classic”表示一个可独立使用的稳定方法，不把README写成“淘汰版清仓”；同时诚实说明它是第一代公开适配，不暗示包含未开放的笔触系统。

## 中文首发草案

我把自己做论文讲解视频的第一代方法整理开源了。

不是先把论文变成一叠摘要幻灯片，而是让原文留在画面里：讲到哪句，就在真实位置画线；遇到复杂关系，再从原文旁展开解释。

这次开放了 Agent Skill、可运行的 Python 渲染示例，以及可选的原生语音时间戳对齐。默认示例不需要 API key，几条命令就能生成视频。

它还不是“把任何论文扔进去就自动讲懂”的黑盒。我更希望公开的是一种可检查、可修改、可复现的讲解方法。

欢迎拿自己在读的论文试试，也欢迎反馈具体问题。

## English draft

I open-sourced the classic workflow behind my paper explainers.

Instead of replacing a paper with summary slides, it keeps the original passage on screen, highlights exact source locations, and unfolds a teaching layer beside the evidence.

The repo includes an Agent Skill, a credential-free Python demo, and an optional native-word-timing speech adapter. It is a small, inspectable workflow—not a claim that one prompt can understand every paper.

Built by Thomas Li. Try it with a paper you are reading and share a reproducible example.

## Release sequence

先确认一个人能从干净目录跑通，再发布仓库和演示；社交帖子用同一段真实demo，不堆功能清单。收集首批安装/使用问题后做修订。首发不同时发布三路工程，避免主旨分散。不得把这些草案当成已发布帖子。
