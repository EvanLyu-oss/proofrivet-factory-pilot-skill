---
name: proofrivet-factory-pilot
description: Guides an authorized company contact through preparing a ProofRivet enterprise onboarding application by primary industry and business activity. Use to collect missing company information and, with the applicant's confirmation, submit synthetic applications to the isolated preview.
---

# ProofRivet 企业入驻申请

1. 本预览仅使用合成企业、合成联系人和测试邮箱。用申请人的语言交谈。读取 [申请字段和行业选项](references/application.md)，使用已有信息并集中询问缺项。请申请人选择一个主营行业，并用一句话描述日常经营，例如「生产销售工程塑料」。登记号使用申请人确认的合成值。入驻后，企业可在自己的工作台添加具体产品并提交证据。
2. 逐项展示将发送的完整摘要，包括企业法定名称、登记号、主营行业、主营业务、联系人姓名、职务、企业邮箱和授权依据。请申请人确认有权代表企业，并同意将这些内容发送到 ProofRivet 审核后台。摘要修改后，再次展示并取得确认。
3. 明确同意后，为这份申请生成 UUID v4 作为 `requestId`，将 `applicantConfirmed` 设为 JSON 布尔值 `true`。按 [提交说明](references/application.md#提交和回执) 运行固定地址的 [提交脚本](scripts/submit.py)，通过标准输入交付 UTF-8 JSON。遇到验收站暂不可用，保留摘要并说明提交结果，等待该站恢复。若使用临时文件，限制为仅本人可读并在提交后清理。申请内容留在私密渠道。
4. 只有服务端返回有效受理编号才报告“申请请求已收件”，把实际编号告诉申请人。人工审核和邀请另行进行。遇到超时、连接中断或结果无法核实，说明提交结果待确认。确需重试时，在申请人确认后复用原请求 ID 和原内容。

原件、交易凭证和真实企业资料留在企业受控环境。客户端无法运行工具时，交付合成摘要供申请人在[验收站申请页](https://defensive-sort-six-albert.trycloudflare.com/apply)填写。
