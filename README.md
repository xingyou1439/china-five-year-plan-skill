# 未来五年，普通人的机会与避坑指南

基于十五五规划的职业与小生意决策参考。帮你看清可以服务谁、交付什么，以及下一步先验证什么；每项判断附政策出处、参与门槛和停止条件。

[打开手机阅读页](https://xingyou1439.github.io/china-five-year-plan-skill/) · [免费下载短版PDF](https://github.com/xingyou1439/china-five-year-plan-skill/releases/download/v0.2.0/five-year-guide-v0.2.0.pdf) · [English](README.en.md)

## 先看与你有关的一个问题

无需安装即可阅读。以下均为构造场景；政策依据与商业假设分别标明，真实需求、付款和个人适配待验证。

| 你的问题 | 从这里开始 |
| --- | --- |
| 给制造企业做AI，先培训、实施还是做软件？ | [决策卡01](guide/card-01.md) |
| 不会造机器人，小团队能参与哪一段？ | [决策卡02](guide/card-02.md) |
| 想做养老业务，谁使用、谁决定、谁付钱？ | [决策卡03](guide/card-03.md) |
| 国家支持的行业，为什么仍然接不到订单？ | [决策卡04](guide/card-04.md) |
| 已有营销、设计或培训能力，怎样迁移？ | [决策卡05](guide/card-05.md) |

每张卡都沿“政策方向 → 实施工具与项目 → 客户与付款方 → 可交付任务 → 验证行动”展开。查不到的一环先留空，不把规划目标写成个人订单。

[阅读全部卡片](guide/README.md) · [下载分享图与发布包](https://github.com/xingyou1439/china-five-year-plan-skill/releases/tag/v0.2.0) · [反馈使用结果](https://github.com/xingyou1439/china-five-year-plan-skill/issues/new?template=guide-feedback.yml)

## 把你自己的情况带入分析

底层仍是“**中国十五五决策参考 Skill**”：基于十三五、十四五与十五五规划提供可追溯的政策依据、跨期对照和行动建议。

- 国内职业、学习、创业与项目选择。
- 海外用户了解中国的发展重点、术语、制度和变化。
- 海外用户进入中国市场时，分别核实机会、主体、地区和经营条件。

支持中英文。政策关联、实施证据、需求、能力和时机分别判断；允许“证据不足”或“与规划不明显相关”。

## 安装与使用

[下载 v0.2.0 安装包](https://github.com/xingyou1439/china-five-year-plan-skill/releases/download/v0.2.0/china-five-year-plan-skill-v0.2.0.zip) · [查看版本](https://github.com/xingyou1439/china-five-year-plan-skill/releases)

### WorkBuddy

复制到 WorkBuddy 对话框，下载安装包：

```text
请下载这个 Skill 安装包到本机，告诉我保存位置，保留 ZIP 不解压：
https://github.com/xingyou1439/china-five-year-plan-skill/releases/download/v0.2.0/china-five-year-plan-skill-v0.2.0.zip
```

然后点击 **专家·技能·连接器 → 技能 → 添加技能 → 上传技能**，选择下载的 ZIP。在“已安装”中搜索 `china-five-year-plan-skill`，确认已启用，再新建对话使用。也可直接点击上方下载链接。[WorkBuddy 官方说明](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)：自定义包需上传导入，对话一键安装目前仅适用于技能市场中的技能。

### Codex

复制到本机 Codex 对话框：

```text
$skill-installer 请安装 GitHub 仓库 https://github.com/xingyou1439/china-five-year-plan-skill
版本 ref：v0.2.0；仓库内路径：.；安装名称：china-five-year-plan-skill。
请安装完整目录，检查 SKILL.md 和 references/ 是否齐全；如已存在，请先检查，不要覆盖。
```

安装后开启新对话；未识别时重启 Codex。见 [Codex 官方说明](https://learn.chatgpt.com/docs/build-skills)。

### Claude Code

复制到本机 Claude Code 对话框：

```text
请将 https://github.com/xingyou1439/china-five-year-plan-skill 的 v0.2.0 版本完整安装到
~/.claude/skills/china-five-year-plan-skill，保留所有文件的相对位置。
如目标目录已存在，请先检查，不要覆盖。完成后检查 SKILL.md 和 references/ 是否齐全。
```

安装后输入 `/china-five-year-plan-skill` 调用。个人技能目录见 [Claude Code 官方说明](https://code.claude.com/docs/en/skills#choose-where-skills-load)。

v0.1.0曾验证 Codex 官方安装器下载、完整安装及证据检索。v0.2.0本次完成发布包完整性与本地证据检索检查；客户端安装状态以对应实测记录为准。WorkBuddy 实际导入、Claude Code 客户端调用尚未完成实测。安装时应保留完整文件夹，不能只复制 `SKILL.md`。

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

PDF和分享二维码的重建另需ReportLab，以及支持中文的TrueType字体。日常阅读、Skill检索与校验不需要这些依赖。PDF和PNG写到仓库外，核验后作为Release附件发布：

```sh
python3 scripts/build_qr.py
python3 scripts/build_pdf.py --output ../guide-output/five-year-guide-v0.2.0.pdf --font /path/to/cjk-font.ttf
```

[发布文案与两周验证流程](launch/launch-kit.md) · [20个问题与进度](launch/question-backlog.md) · [匿名试用记录模板](launch/reader-test-template.csv)

## 资料范围

本地资料于 **2026-10-17** 整理。原目录含 133 份 PDF、2 张图片及 2 个按要求跳过的视频/下载文件；PDF 内容去重后为 126 份、2,590 页。**全文提取与索引不等于每页都经过人工核验**，具体覆盖见说明。

基础语料主要截至 2026 年 3 月附近，不能证明此后政策已经落地。公众指南另补查4条官方依据，含2026年6月机器人专项行动与9月中小企业专项规划，核验于2026-10-18；范围见 [cards.json](guide/cards.json)。补查不代表已全面更新所有政策。市场准入、许可、数据、税务等当前问题需要另查当期官方文件。研究报告中的预测、评级和短期行情不作为已实现事实或当前建议。

原始券商研报、课程 PDF 和本机路径不随公开包分发；参考目录用于溯源，不能保证每份报告都有公开下载入口。见[来源与使用说明](SOURCE_NOTICE.md)。

## 状态

`v0.2.0`。这是独立的政策参考工具，新增公众指南与阅读页；尚未提交技能市场，未声称获得官方背书、完成所有宿主实测或验证商业效果。
