---
name: proofrivet-factory-preview
description: Prepare and submit synthetic enterprise onboarding data for the isolated ProofRivet acceptance site, including an optional company website.
disable-model-invocation: true
---

# ProofRivet 企业入驻预览

1. 读取 [申请字段与行业选项](references/application.md)。用申请人的语言核对已有合成资料并补问必填缺项。可选填一个企业官网或独立站。申请人留空时，省略 `websiteUrl`，继续准备申请。
2. 逐项展示将提交的摘要。网址随摘要展示，让申请人核对本次提交的内容。向申请人说明网址会先进入审核，企业随后可在工作台决定是否公开。取得本次提交的明确同意后，生成 UUID v4，设置 `applicantConfirmed` 为 JSON 布尔值 `true`。摘要有改动时，重新确认。
3. 按 [提交与回执](references/application.md#提交与回执) 运行 [预览提交工具](scripts/submit.py)。若当前客户端无法访问独立验收站，将摘要交给申请人在 [独立验收站申请页](https://passengers-bridge-hosts-relate.trycloudflare.com/apply) 填写。
4. 以服务端实际返回的受理编号作为提交结果。未能核实回执时，说明结果待确认，并按提交与回执中的规则处理重试。
