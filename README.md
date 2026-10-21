# 十五五规划解读与职业创业决策指南

**看懂国家的发展方向，想清楚自己的下一步。**

这是一套免费的 AI Skill，帮助你结合十三五、十四五与十五五规划，分析职业选择、技能学习、创业和项目方向。安装到支持 Skill 的 AI 助手后，用自己的情况提问，就能得到有政策出处、也有下一步行动的分析。

[开始使用](#安装与使用) · [先看看怎么提问](#可以这样提问) · [English](README.en.md)

## 它能帮你做什么？

- **看懂变化**：一个方向在历次规划中有什么变化，哪些是原文明确提出的重点？
- **比较选择**：结合你的经验、城市和投入条件，比较转行、学习或创业的不同选项。
- **找到下一步**：把一个大方向拆成需要核实的信息，以及现在可以做的小行动。

## 可以这样提问

安装后，从一句话开始：**“我现在做____，最近想弄清楚____。”** 不用先填完整问卷。

| 你想做什么 | 可以直接发给助手的话 |
| --- | --- |
| 看懂一个方向 | 请使用 china-five-year-plan-skill。十五五和十四五相比，养老服务的重点有哪些变化？请解释并给出原文链接。 |
| 比较两个选择 | 请使用 china-five-year-plan-skill。我做了5年品牌营销，想学AI。先提高现有工作效率，还是试着做新服务？ |
| 安排下一步 | 请使用 china-five-year-plan-skill。我有企业培训经验，想试本地制造企业的AI服务。投入前今天先找谁、问什么？ |

没有选项，也可以先探索。只有会改变判断的信息才需要补问，例如具体项目的城市、能力或投入；只解释一个词，不要求预算。也支持英文，适用于了解中国与市场进入研究。

[网页里填写并复制提问](https://xingyou1439.github.io/china-five-year-plan-skill/#start) · [看一次完整演示](https://xingyou1439.github.io/china-five-year-plan-skill/first-session.html)

## 回答会给你什么？

先给一屏左右的回答：**当前判断、相关依据、最该查清的事、今天能做的一步**。复杂条件会保留，需要时再展开。解释类问题先把概念说清楚；决策类问题把政策、真实需求、个人能力和准入条件分开看。

例如，“做了5年品牌营销，想学AI”会先比较怎样沿用已有能力，再给一个可评估的小任务；不会从政策支持直接推导出新收入。[完整演示](examples/first-session.md)包括一句输入、必要追问、政策引用、选项比较、本周行动与后续复盘，明确标为构造示范。

### 用完可以带走什么？

在助手里说：**“请把刚才的分析整理成我的职业与创业选择单。”** 可以保存选项、当前判断、来源、最大未知、核实动作和复盘条件。[查看选择单模板](references/decision-note.md)。

下次贴回选择单，加上“新了解到____，请重新判断”，就能继续分析。跨对话需要自己带回记录。

想分享时再说：**“请精简为适合截图的分享版，删去个人条件和商业细节，保留来源、关键不确定性和一个动作。”** 请自行复核隐私后决定是否发布。网站提供提问模板；分析和选择单由已安装 Skill 的助手生成。

## 安装与使用

[下载 v0.3.0 安装包](https://github.com/xingyou1439/china-five-year-plan-skill/releases/download/v0.3.0/china-five-year-plan-skill-v0.3.0.zip) · [查看版本](https://github.com/xingyou1439/china-five-year-plan-skill/releases)

### WorkBuddy

复制到 WorkBuddy 对话框，下载安装包：

```text
请下载这个 Skill 安装包到本机，告诉我保存位置，保留 ZIP 不解压：
https://github.com/xingyou1439/china-five-year-plan-skill/releases/download/v0.3.0/china-five-year-plan-skill-v0.3.0.zip
```

然后点击 **专家·技能·连接器 → 技能 → 添加技能 → 上传技能**，选择下载的 ZIP。在“已安装”中搜索 `china-five-year-plan-skill`，确认已启用，再新建对话使用。也可直接点击上方下载链接。[WorkBuddy 官方说明](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)：自定义包需上传导入，对话一键安装目前仅适用于技能市场中的技能。

### Codex

复制到本机 Codex 对话框：

```text
$skill-installer 请安装 GitHub 仓库 https://github.com/xingyou1439/china-five-year-plan-skill
版本 ref：v0.3.0；仓库内路径：.；安装名称：china-five-year-plan-skill。
请安装完整目录，检查 SKILL.md 和 references/ 是否齐全；如已存在，请先检查，不要覆盖。
```

安装后开启新对话；未识别时重启 Codex。见 [Codex 官方说明](https://learn.chatgpt.com/docs/build-skills)。

### Claude Code

复制到本机 Claude Code 对话框：

```text
请将 https://github.com/xingyou1439/china-five-year-plan-skill 的 v0.3.0 版本完整安装到
~/.claude/skills/china-five-year-plan-skill，保留所有文件的相对位置。
如目标目录已存在，请先检查，不要覆盖。完成后检查 SKILL.md 和 references/ 是否齐全。
```

安装后输入 `/china-five-year-plan-skill` 调用。个人技能目录见 [Claude Code 官方说明](https://code.claude.com/docs/en/skills#choose-where-skills-load)。

建议先用 Codex；安装后发一句“请使用 china-five-year-plan-skill；如果未找到请明确说明”，并检查回答能否给出实际读取的来源。v0.1.0曾验证 Codex 官方安装器的完整安装与证据检索；v0.3.0的包校验与复制安装后的检索记录见[验证说明](tests/v0.3-validation.md)。本次没有完成新会话自动发现和独立模型行为测试；WorkBuddy 导入、Claude Code 调用也未实测。安装时保留完整文件夹，不能只复制 `SKILL.md`。

### 安装后怎么用

复制以下问题，替换为自己的情况（Claude Code 也可用 `/china-five-year-plan-skill` 开头）：

```text
请使用 china-five-year-plan-skill，判断我给本地制造企业做 AI 服务的想法，
与十五五有哪些直接关联。请引用实际读取的规划原文和来源，区分政策事实和商业假设。
如果未找到该 Skill，请直接说明。
```

```text
Use $china-five-year-plan-skill to explain China's priorities for eldercare
and what an overseas technology supplier should verify before market entry.
```

普通聊天用户也可以提供资料和 `SKILL.md`，要求按该流程分析，但这不等同宿主已安装 Skill。

## 想先阅读，再决定是否安装？

[在线了解与阅读](https://xingyou1439.github.io/china-five-year-plan-skill/) · [下载短版 PDF](https://github.com/xingyou1439/china-five-year-plan-skill/releases/download/v0.3.0/five-year-guide-v0.3.0.pdf) · [专题参考资料](guide/README.md)

阅读材料用5个假设案例演示分析方法，适合先了解内容；个性化分析需要安装 Skill，并带入自己的情况。PDF 是本项目的短版指南，官方规划全文请看[《十五五规划纲要》](https://www.bjrd.gov.cn/zyfb/zt/14jqgrd04chybjdbthdztbd/wjbg/202603/t20260314_4557219.html)。

### 十五五规划怎么用于职业和创业选择？

十五五规划对应2026—2030年。可以先查原文提出的具体任务，再核实所在城市的岗位、实施项目或客户需求，最后结合已有能力比较选项。需要了解方法时，可阅读[从政策支持到客户订单](guide/card-04.md)。

### 可以直接根据规划决定转行或创业吗？

还需要核实目标岗位或客户需求、预算、能力与经营条件。项目区分官方事实、分析推导和待验证假设；规划目标不能直接证明个人收入、补贴资格或客户订单。

## 信息安全

公开内容仅包含审核后的 Skill、政策知识与方法、公开文献书目、构造示例和校验脚本。内部人员姓名、联系方式、学员名单、个人作业、原始内部课件、本机路径和密钥不进入发布包。Git 提交使用公开账号与 GitHub no-reply 邮箱。

发布前按固定文件白名单核查内容和压缩包；后续提交会运行同一套扫描。检查机制与范围见[发布信息安全说明](PUBLICATION_SECURITY.md)。

## 内含内容

- [Skill 入口](SKILL.md)：任务选择、检索、判断、引用与回答规则。
- [决策方法](references/decision-method.md)：从政策到执行主体、工具、付款方和用户角色。
- [28 张政策卡](references/policy-cards.json)：已与正文页位置校验的引文和分别标注的应用推导。
- [官方文本语料](references/official-corpus.json)：三个规划的文本层，保留 PDF 页定位与提取方式。
- [跨期核对](references/cross-plan-comparison.md)、[研报蒸馏](references/research-synthesis.md)、[纠偏记录](references/corrections.md)。
- [产业参与环节图](references/industry-entry-map.md)：把两张专栏图片中的产业和设施任务，映射为需要验证的参与角色。
- [来源目录](references/source-catalogue.json)与[覆盖说明](references/coverage.md)：可读取范围、重复、提取质量和未验证部分。
- [三个使用示例](examples/domestic.md)与[行为验收场景](tests/behavioral-cases.md)。

## 检索与校验

日常使用不要求运行脚本；支持读取文件的宿主可直接阅读参考资料。检索与校验脚本仅需 Python 3.9+ 标准库，不访问网络、不读取仓库外资料。

```sh
python3 scripts/search_evidence.py --query "AI services for Chinese SMEs" --plan 15
python3 scripts/search_evidence.py --query "改革" --plan 14
python3 scripts/search_evidence.py --query "AI" --as-of 2024-12-31
python3 scripts/verify_bundle.py
python3 -m unittest discover -s tests -v
```

搜索排序仅表示文字关联，不能替代阅读上下文。历史日期检索排除发布日期晚于截止日或发布日期未知的文件。OCR 提取的数值需再对照页面。

## 重建阅读页与发布材料

```sh
python3 scripts/build_reader.py
python3 scripts/verify_guide.py
```

如需附精确页码的核验版，可给PDF生成命令加 `--audit-citations`；普通读者版默认只显示书名、章节和来源链接。

PDF和分享二维码的重建另需ReportLab，以及支持中文的TrueType字体。日常阅读、Skill检索与校验不需要这些依赖。PDF和PNG写到仓库外，核验后作为Release附件发布：

```sh
python3 scripts/build_qr.py
python3 scripts/build_pdf.py --output ../guide-output/five-year-guide-v0.3.0.pdf --font /path/to/cjk-font.ttf
```

[发布文案与两周验证流程](launch/launch-kit.md) · [20个问题与进度](launch/question-backlog.md) · [匿名试用记录模板](launch/reader-test-template.csv)

## 资料范围

本地资料于 **2026-10-17** 整理。原目录含 133 份 PDF、2 张图片及 2 个按要求跳过的视频/下载文件；PDF 内容去重后为 126 份、2,590 页。**全文提取与索引不等于每页都经过人工核验**，具体覆盖见说明。

基础语料主要截至 2026 年 3 月附近，不能证明此后政策已经落地。公众指南另补查4条官方依据，含2026年6月机器人专项行动与9月中小企业专项规划，核验于2026-10-18；范围见 [cards.json](guide/cards.json)。补查不代表已全面更新所有政策。市场准入、许可、数据、税务等当前问题需要另查当期官方文件。研究报告中的预测、评级和短期行情不作为已实现事实或当前建议。

原始券商研报、课程 PDF 和本机路径不随公开包分发；参考目录用于溯源，不能保证每份报告都有公开下载入口。见[来源与使用说明](SOURCE_NOTICE.md)。

## 状态

`v0.3.0`。本版增加三个提问入口、简短首问、选择单与复盘、完整使用演示；尚未提交技能市场，未声称获得官方背书、完成所有宿主实测或验证商业效果。
