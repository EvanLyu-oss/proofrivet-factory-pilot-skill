# ProofRivet 企业入驻技能预览版

版本 `v0.3.0-rc.2` 用于独立公网验收。可用合成申请验证企业官网或独立站的选填字段。企业也可以激活账号后在工作台补填网址。审核员核对后，由企业授权公开。

## 交给 AI

> 请读取 [ProofRivet 企业入驻预览技能](SKILL.md)，用合成资料准备入驻申请。如果我提供企业官网或独立站，请把网址列入摘要。请让我确认摘要，随后用技能的提交工具发到独立验收站，并报告返回的受理编号。

从 [SKILL.md](SKILL.md) 开始，按 [申请字段与回执](references/application.md) 核对表单并运行 [提交工具](scripts/submit.py)。工具使用 Python 3 标准库，提交地址固定为独立验收站 `https://passengers-bridge-hosts-relate.trycloudflare.com/api/ai/factory-applications`。
