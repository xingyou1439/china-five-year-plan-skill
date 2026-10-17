# 发布信息安全 / Publication security

## 公开范围

仅发布 `scripts/verify_publication.py` 的固定文件白名单：Skill 指令、整理后的知识、公开文献书目、构造示例、源文引文、代码、测试与项目说明。官方语料仅来自三个规划纲要；原始研报、课程、OCR 中间文件和研究工作目录不上传。

来源目录保留文献标题、类别、日期、页数、内容指纹和覆盖记录；剔除本机目录及原始文件位置。内部人员姓名、联系方式、学员名单、个人作业、账户资料和密钥不属于任何允许发布的数据类别。

## 发布检查

1. 从审核后的文件创建独立、全新 Git 历史，避免带入其他项目文件、旧提交或原始资料。
2. 逐项检查固定文件白名单，不接受符号链接、未列出的文件和原始附件。
3. 扫描邮箱、手机号、座机号、证件号、本机绝对路径、私钥和常见访问令牌；JSON 内容指纹按完整字段识别，避免把哈希中的数字误当作电话号码。
4. 可在本机额外使用私有敏感词表；敏感词表及命中内容均不写入公开文件或日志。
5. 人工复核资料来源、示例、书目与说明文字，确认未夹带内部人员信息。自动扫描不能识别所有人名，不能替代来源限定和内容审阅。
6. 为每个公开文件生成路径、SHA-256 和大小组成的清单；创建压缩包后核对文件集合及每份内容。
7. 使用公开 GitHub 账号和 no-reply 邮箱提交；发布后核对远程文件、提交身份及下载包。

持续集成执行相同的公开内容检查与证据测试。自动检查覆盖的是列明的内容与规则，不等于对任何未来新增资料作出预先保证。新增发布文件或数据类型需明确更新白名单并重新审阅。

## English

Only explicitly allowlisted, reviewed project files are published. Raw research documents, internal materials, participant information, personal assignments, local source paths and credentials are excluded. Bibliographic metadata is reduced to public document identity and review coverage.

Pre-publication checks combine provenance and manual review, sensitive-data scanning, a fixed file allowlist, a fresh Git history with a public no-reply identity, a content-hash manifest and verification of the remote tree and release archive. A private local denylist can supplement the scan without publishing its contents. Automated patterns cannot identify every personal name, so future changes require the same review rather than inheriting an unlimited assurance.
