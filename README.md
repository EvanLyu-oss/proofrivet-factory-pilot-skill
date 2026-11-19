# ProofRivet 工厂试点申请技能

用一段对话向 AI 说明您的产品，由 AI 补齐资料、展示提交摘要。您确认后，AI 将申请发到 ProofRivet，由审核人员处理。

## 给自己的 AI

复制这段话，并附上本仓库的官方链接。

> 请读取这条 GitHub 链接中的 ProofRivet 工厂试点申请技能，帮我用一款产品准备试点申请。先问我缺的信息，把完整摘要给我确认。收到我的明确同意后，再使用技能里的提交工具，把实际受理编号告诉我。

支持 Agent Skills 的客户端可读取 [SKILL.md](SKILL.md) 和其中引用的文件。需要导入时，可从仓库的 Releases 下载对应版本的技能 ZIP。提交工具需要客户端能运行 Python 3。原件留在企业受控环境，申请摘要通过 ProofRivet 官方接口提交。

已收到申请请求时，AI 会提供服务器返回的受理编号。试点资格由工作人员审核，后续邀请也由工作人员处理。

## 技能文件

- [SKILL.md](SKILL.md) 描述准备、确认和提交顺序。
- [申请字段](references/application.md) 定义结构化申请和回执格式。
- [提交工具](scripts/submit.py) 使用标准库将已确认的 JSON 发往 ProofRivet。
