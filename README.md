# 中国十五五决策参考 Skill

[English](README.en.md)

一个面向国内决策者和海外用户的开源、双语 AI Skill。基于中国十三五、十四五与十五五（2026–2030）规划，为了解中国、进入中国市场，以及职业、创业和项目选择，提供可追溯的政策依据、跨期趋势对照和行动建议。

它沿着“政策方向 → 实施工具 → 客户与付款方 → 可参与环节 → 验证行动”分析问题，把政策事实、研究观点和商业假设分别说明。

## 两类用户，三种任务

- 国内用户：职业、学习、创业和项目选择。
- 海外用户了解中国：发展重点、政策术语、制度和跨期变化。
- 海外用户进入中国市场：行业、地区、合作方式、机会与待核验的进入条件。

支持中英文问答。规划支持、市场需求、个人能力与准入条件分别分析，允许“证据不足”或“与规划不明显相关”。

## 使用

[下载 v0.1.0 安装包](https://github.com/xingyou1439/china-five-year-plan-skill/releases/download/v0.1.0/china-five-year-plan-skill-v0.1.0.zip) · [查看版本](https://github.com/xingyou1439/china-five-year-plan-skill/releases)

在支持 Agent Skills 的宿主中安装整个 `china-five-year-plan-skill` 文件夹，保留 `SKILL.md`、`references/`、`scripts/` 的相对位置。安装后可显式请求：

```text
使用 $china-five-year-plan-skill，判断我给本地制造企业做 AI 服务的想法，
与十五五有哪些直接关联。请引用原文，区分政策事实和商业假设。
```

```text
Use $china-five-year-plan-skill to explain China's priorities for eldercare
and what an overseas technology supplier should verify before market entry.
```

Codex 的本地技能目录和安装方式以[官方 Skills 文档](https://learn.chatgpt.com/docs/build-skills)为准。可将完整文件夹放入 `~/.agents/skills/`，或在 Codex 中让 `$skill-installer` 安装已发布的仓库。其他宿主的安装方式应按其文档核实；本包尚未声称通过全部宿主实测。

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

## 资料范围

本地资料于 **2026-10-17** 整理。原目录含 133 份 PDF、2 张图片及 2 个按要求跳过的视频/下载文件；PDF 内容去重后为 126 份、2,590 页。**全文提取与索引不等于每页都经过人工核验**，具体覆盖见说明。

材料主要截至 2026 年 3 月附近，不能证明此后政策已经落地。市场准入、许可、数据、税务等当前问题需要另查当期官方文件。研究报告中的预测、评级和短期行情不作为已实现事实或当前建议。

原始券商研报、课程 PDF 和本机路径不随公开包分发；参考目录用于溯源，不能保证每份报告都有公开下载入口。见[来源与使用说明](SOURCE_NOTICE.md)。

## 状态

`v0.1.0`。这是独立的政策参考工具，尚未提交技能市场，未声称获得官方背书、完成所有宿主实测或验证商业效果。
