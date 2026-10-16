<p align="center">
  <img src="assets/banner.svg" alt="Divan——由 AI 智能体组成的产品团队，围绕一位做决定的人而构建" width="100%">
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.fa.md">فارسی</a> · <a href="README.ar.md">العربية</a> · <b>中文</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-3B82F6" alt="version 0.1.0">
  <img src="https://img.shields.io/badge/status-early-EAB308" alt="status: early">
  <img src="https://img.shields.io/badge/licence-MIT-22C55E" alt="MIT licence">
  <img src="https://img.shields.io/badge/for-Claude%20Code-6366F1" alt="for Claude Code">
</p>

# Divan（迪万）

**为软件项目打造的 AI 智能体产品团队——围绕一位做决定的人而构建。**

[方法论（英文）](docs/method.md) · [适配现有仓库（英文）](docs/adapting.md) · [案例研究（英文）](docs/case-studies/taghvim.md) · [关于作者](#about)

> **状态：早期（v0.1）。** Divan 已在一个线上产品中完成安装与适配
> （[案例研究](docs/case-studies/taghvim.md)）。从想法到发布的完整功能循环**尚未**端到端运行过。
> 运行之后，结果（包括失败之处）将在此公开。

---

## 问题所在

AI 编程智能体很快，速度不是问题。问题在于：当你让一个智能体"把这个功能做出来"时，它同时充当产品经理、架构师、开发者和评审者，**还给自己的工作打分**。结果是：代码又多又快，但其中一部分解决的是错误的问题、违反了没人告诉过它的规则，或者直接推送到了生产环境。

人类团队早已通过**职责分离和审批节点**解决了这个问题。Divan 把同样的结构带给智能体。

## 团队

<p align="center">
  <img src="assets/team.svg" alt="负责人位于七个专业智能体之上" width="100%">
</p>

| | 智能体 | 对应的人类角色 | 修改代码？ |
|:-:|---|---|---|
| <img src="assets/icons/spec-writer.svg" width="28" alt=""> | `spec-writer` | 产品经理——功能定义 | 否 |
| <img src="assets/icons/architect.svg" width="28" alt=""> | `architect` | 技术负责人——设计、三个备选方案、任务拆分 | 否 |
| <img src="assets/icons/builder.svg" width="28" alt=""> | `builder` | 全栈与移动端开发者，一次只做一个任务 | 是 |
| <img src="assets/icons/reviewer.svg" width="28" alt=""> | `reviewer` | 资深工程师与质量保证——**独立于**开发者 | 否 |
| <img src="assets/icons/security-checker.svg" width="28" alt=""> | `security-checker` | 安全与隐私——核查产品的公开承诺 | 否 |
| <img src="assets/icons/feature-engineer.svg" width="28" alt=""> | `feature-engineer` | 机器学习工程师——**仅当产品包含模型时** | 仅限 ML 目录 |
| <img src="assets/icons/release-docs.svg" width="28" alt=""> | `release-docs` | DevOps 与技术文档——只做准备，从不发布 | 仅限文档 |

此外还有：
- **`feature-loop`**：把智能体串联起来的流程，设有**三道关口**，由你做决定。
- **`feature-definition`**：把需求转化为小而可测试、带有成功信号的功能。
- **`divan-adapt`**：在**不破坏既有规则**的前提下，把这套工具适配到成熟的仓库。
- **质量关卡钩子（hook）**：测试或类型检查失败时，阻止智能体结束工作。
- **禁止规则**：禁止 push、打 tag、发布，禁止读取 `.env` 或签名密钥。

## 功能循环

<p align="center">
  <img src="assets/loop.svg" alt="带有三道审批关口的功能循环" width="100%">
</p>

- **关口 A——范围：** 你批准功能卡片，包括被砍掉的部分。
- **关口 B——设计：** 你批准方案，并从三个备选方案中选择一个。
- **关口 C——发布：** 由你合并、部署和发布。智能体从不做这些事。

## 安装

```bash
git clone --depth 1 https://github.com/farjadp/divan.git
./divan/install.sh /path/to/your/project
```

安装脚本**从不覆盖已有文件**。如果你的项目已有 `CLAUDE.md`，Divan 的模板会以 `CLAUDE.divan.md` 的名称写在旁边，供你手动合并。如果 `.gitignore` 忽略了 `.claude/` 目录，或仓库中已有智能体说明（如 `AGENTS.md`），它会给出提醒。使用 `--dry-run` 可以预览操作而不做任何更改。

然后：

1. 填写 `CLAUDE.md`，最重要的是**第 2 节**（下面的三个事实）和**第 4 节**（项目的真实命令）。
2. 在 Claude Code 中打开项目，运行 `/agents` 查看团队。
3. **已有项目？** 输入：*"adapt Divan to this repo"*。
4. 输入：*"run the feature loop for: <一个小而真实的功能>"*。

## 每个智能体都必须知道的三个事实

智能体团队的失败大多不是编码错误，而是某个智能体违反了以下事实之一——因为没人把它写下来：

1. **什么会触发生产环境部署？** 如果推送到 `main` 就会部署，那么智能体推送就等于发布。
2. **追踪策略是什么？** 它决定了成功如何衡量。对于承诺不做追踪的产品，Divan 绝不添加任何追踪。
3. **产品做过哪些公开承诺？**（如"不向第三方发送请求"、"可离线使用"。）安全智能体会逐条按名称核查每一次改动。

## "功能定义"不是"特征工程"

**特征工程（Feature Engineering）** 是机器学习术语：构建模型从中学习的输入变量。把用户需求转化为产品功能，则叫**功能定义（Feature Definition）**，属于需求工程的一部分。Divan 把两者分开：不同的智能体，不同的术语。

## 为什么叫"Divan"？

在历史上的波斯政府中，"diwan（迪万）"指行政机构：由文书、财政、军籍等专业部门组成，每个部门把一件事做好，并共同向一位决策者负责。这正是这个团队的形态。

## 坦诚的局限

- **需求发现靠你。** 智能体无法访谈用户。请给它们真实证据，或把论断标注为假设。
- **审美靠你。** 智能体能做出合格的设计，但很少做出出色的设计。
- **账号靠你。** 应用商店、支付、签名密钥和法律事务只能由人处理。
- **速度会掩盖技术债。** 如果你无法在两分钟内讲清一个模块，就停下来评审。
- **成本。** 长时间运行智能体会消耗大量 token。小任务更便宜，效果也更好。
- **工具在变化。** 智能体、技能和钩子的格式在不断演进；请对照最新的 [Claude Code 文档](https://docs.claude.com/en/docs/claude-code/overview)核实。

## 参与贡献

最有价值的贡献是**真实使用报告**：你在真实项目中安装了 Divan——哪里有冲突、哪里出了问题、你改了什么？参见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

<a id="about"></a>

## 关于作者

<img src="assets/logo.svg" width="72" align="left" alt="">

**Farjad Pourmohammad** 是一位常驻加拿大多伦多的 AI 战略顾问、创业导师和产品构建者。二十多年来，他在伊朗和加拿大创办和建设科技公司：创立并经营过一家软件公司，以首席技术官（CTO）身份带领过工程团队，也构建了自己的产品，其中包括 [Taghvim](https://taghv.im)——一款覆盖网页、浏览器和手机的开源波斯历。如今，他为早期创业者提供指导，并帮助企业判断 AI 真正能在哪里创造价值。Divan 正源于这些工作：他对创始人提出的同一套纪律——定义问题、收缩范围、衡量结果——如今应用于一支 AI 智能体团队。

*从复杂，到清晰，再到行动。*

### 服务

| | 服务 | 说明 |
|:-:|---|---|
| 🧭 | **AI 战略** | 找出 AI 在你的业务中真正能创造价值的地方，然后进行设计、构建与安全加固。 |
| 🚀 | **创业指导——The Founder Lab** | 面向五个团队的免费八周项目：在动手构建之前完成客户发现与精益验证。 |
| 🤝 | **创始人咨询与教练** | 一对一辅导：为只有你才能做的决定，提供一位思维陪练。 |
| 🛠️ | **网站、应用与 AI 产品开发** | 通过 AshaVid 提供：网站、浏览器扩展、Android 和 iPhone 应用、桌面小组件与自动化。 |
| 🔤 | **波斯语与从右到左（RTL）产品** | 正确的 RTL 排版、字体、波斯数字与伊朗太阳历日期，服务于波斯语用户。 |

**从小处开始：** 在网站上预约一次免费诊断通话，或完成一份十分钟的自我评估。

🌐 **[farjadp.info](https://farjadp.info)** ·
💼 [LinkedIn](https://www.linkedin.com/in/farjadpourmohammad) ·
▶️ [YouTube @FarjadTalks](https://www.youtube.com/@FarjadTalks) ·
🐙 [GitHub @farjadp](https://github.com/farjadp)

---

## 许可证

MIT 许可证，详见 [LICENSE](LICENSE)。智能体图标来自 [Lucide](https://lucide.dev)（ISC 许可证），详见 [assets/NOTICE-lucide.txt](assets/NOTICE-lucide.txt)。

Divan 是一个独立项目，与 Anthropic 无关联，也未获得其背书。"Claude"和"Claude Code"是 Anthropic 的商标。
