---
name: proofrivet-factory-pilot
description: Guides an authorized factory contact through preparing and submitting a ProofRivet factory onboarding application for one product. Use when a factory wants to apply or check which information is missing before submitting.
---

# ProofRivet 工厂入驻申请

1. 用申请人的语言交谈。读取 [申请字段](references/application.md)，复用申请人提供的信息，集中询问仍缺的字段。收齐企业法定名称和统一社会信用代码或当地登记号。型号、规格、用途分别填写。授权依据或材料准备情况暂不清楚时，按实际情况写「待核实」。
2. 把将发送的完整摘要逐项给申请人看，包含企业登记号、联系人及其邮箱和授权、产品名称、型号、规格、用途及材料清单。说明这些字段将进入 ProofRivet 的人工审核后台。请申请人确认自己有权代表企业并明确同意发送所展示的全部字段。对方补充或修改任何字段时，请重新展示并确认。
3. 收到明确确认后，再执行提交。为这份已确认的申请生成一个 UUID v4 作为 `requestId`，并设置 `applicantConfirmed` 为 JSON 布尔值 `true`。通过标准输入将 JSON 交给 [提交脚本](scripts/submit.py)。客户端需要从文件提供标准输入时，使用仅申请人可读的临时文件，提交后清理。申请内容请留在私密渠道，切勿写入共享目录、日志或终端命令参数。
4. 只有服务端返回有效受理编号才报告“申请请求已收件”，把实际编号告诉申请人。人工审核和邀请另行进行。遇到超时、连接中断或结果无法核实，说明提交结果待确认。确需重试时，在申请人确认后复用原请求 ID 和原内容。

脚本只发送申请字段。报告原件、交易凭证、买方身份及价格请留在企业内部，后续按授权通过私密渠道提供。技能负责提交入驻申请。若客户端无法运行提交工具，先交付摘要，并给出 [ProofRivet 工厂入驻申请表](https://factory.proofrivet.com/apply) 供申请人继续提交。
