# 工厂入驻申请字段与回执

每份入驻申请包含一个企业和一款拟核验产品。表中字段均为必填。使用申请人提供的实际信息，统一社会信用代码或当地企业登记号以登记文件为准。授权依据或材料说明有待补充时，可在对应字段写「待核实」，交由工作人员复核。

| 字段 | 填写内容 | 文本长度上限 |
| --- | --- | ---: |
| `companyName` | 企业登记全称 | 200 |
| `registrationId` | 统一社会信用代码或企业登记号。境外企业可填当地登记号 | 80 |
| `contactName` | 经办联系人姓名 | 100 |
| `email` | 经办联系人使用的企业邮箱 | 254 |
| `contactTitle` | 联系人职务 | 100 |
| `authorizationBasis` | 代表企业申请及处理本次材料的依据 | 500 |
| `productName` | 拟核验产品名称 | 200 |
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
  "companyName": "DEMO 合成入驻申请企业",
  "registrationId": "DEMO-REG-20261119",
  "contactName": "合成联系人",
  "email": "factory@example.invalid",
  "contactTitle": "入驻经办人",
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

新版技能提交新申请时须填写企业登记号。升级前已使用 v0.1.1 提交且结果待确认时，可用 v0.1.1 脚本复用原请求 ID 和原内容。已收件的请求会返回原受理编号。缺企业登记号的旧请求收到 HTTP 400 后，补齐资料，按新版重新确认并生成新 ID。
