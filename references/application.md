# 申请字段与回执

申请面向一个企业的一款产品。所有文本字段都应使用申请人提供的信息。暂时没有授权依据或材料说明时，使用「待核实」，保留给工作人员确认。

| 字段 | 填写内容 | 文本长度上限 |
| --- | --- | ---: |
| `companyName` | 企业登记全称 | 200 |
| `contactName` | 经办联系人姓名 | 100 |
| `email` | 经办联系人使用的企业邮箱 | 254 |
| `contactTitle` | 联系人职务 | 100 |
| `authorizationBasis` | 代表企业申请及处理本次材料的依据 | 500 |
| `productName` | 一款拟试点产品的名称 | 200 |
| `productModel` | 产品完整型号 | 100 |
| `productSpecification` | 产品的主要规格 | 300 |
| `productUse` | 产品主要用途 | 300 |
| `materialSummary` | 拟核验的报告类型、适用型号或案例概况。只填目录与摘要 | 500 |
| `requestId` | 申请人确认后生成的 UUID v4，同一份申请重试时复用 | |
| `applicantConfirmed` | 申请人明确同意后填写 JSON 布尔值 `true` | |

下面是供隔离验收使用的合成示例。

```json
{
  "requestId": "6d032c28-1b2c-4d52-8743-d408713aa99d",
  "applicantConfirmed": true,
  "companyName": "DEMO 合成试点组",
  "contactName": "合成联系人",
  "email": "factory@example.invalid",
  "contactTitle": "试点经办人",
  "authorizationBasis": "合成流程中的授权说明，待核实",
  "productName": "合成装配夹具",
  "productModel": "DEMO-JIG-01",
  "productSpecification": "测试规格 100 × 50 mm",
  "productUse": "合成装配定位试验",
  "materialSummary": "拟核对尺寸检测报告与模拟应用案例的材料范围"
}
```

## 提交和回执

客户端用 `python3 scripts/submit.py` 启动工具，将 UTF-8 JSON **通过标准输入**传给脚本。请保持用户材料中的商业机密在企业受控环境，以便后续在明确授权范围后处理。

脚本向 `https://factory.proofrivet.com/api/ai/factory-applications` 发出 HTTPS POST，仅接受 HTTP 201 和 `{"received":true,"receiptId":"<uuid>"}` 回执。回执代表收到申请请求，企业资质和联系人授权由审核人员核对。已有进行中的申请或账号时，后台对新请求去重，仅记录本次收件。回执格式对所有已收件请求一致，只含收件标记和受理编号。

网络中断后，先说明结果待确认。申请人同意重试时，复用原请求 ID 和完整内容。收到 HTTP 429 时等待至少一分钟，再按同样方式重试。HTTP 409 表示请求 ID 已用于其他内容。修改已确认内容时，重新展示摘要、取得明确同意，并为新请求生成新 ID。
