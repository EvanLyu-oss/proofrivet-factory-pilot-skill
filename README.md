# ProofRivet 企业入驻技能

用一段对话准备企业入驻申请。资料包括企业登记全称、统一社会信用代码或当地企业登记号、主营行业、主营业务，以及经办联系人和授权说明。AI 会展示申请摘要，经您确认后再提交审核。激活账号后，可在工作台添加具体产品。

提交工具固定连接 [ProofRivet 正式企业入驻站](https://factory.proofrivet.com/apply)。

## 给自己的 AI

复制这段话，并附上本仓库的官方链接。

> 请读取这个 GitHub 版本中的 ProofRivet 企业入驻技能，帮我按企业登记信息、主营行业、主营业务和联系人授权准备申请。先询问缺项，再给我确认完整摘要。得到我明确同意后，运行技能附带的提交工具，并告诉我接口实际返回的受理编号。

支持 Agent Skills 的客户端可读取 [SKILL.md](SKILL.md) 和引用的文件。需要导入时，可从 Releases 下载本版本的技能 ZIP。提交工具使用 Python 3 标准库，调用方式见 [提交说明](references/application.md#提交和回执)。

申请收到后，AI 会提供服务器返回的受理编号。工作人员核对企业资料及经办人授权后处理后续邀请。

## 技能文件

- [SKILL.md](SKILL.md) 描述准备、确认和提交顺序。
- [申请字段](references/application.md) 定义结构化申请和回执格式。
- [提交工具](scripts/submit.py) 使用标准库将已确认的 JSON 发往 ProofRivet。
