# 企业入驻申请字段与回执

预览只接收合成资料。企业名称以 `DEMO` 开头，企业登记号以 `DEMO-` 开头，联系人邮箱以 `.invalid` 结尾。每份申请对应一家企业。证据原件和产品资料在企业进入工作台后按需处理。

| 字段 | 填写内容 | UTF-16 长度上限 |
| --- | --- | ---: |
| `companyName` | 企业登记全称 | 200 |
| `registrationId` | 统一社会信用代码或企业登记号 | 80 |
| `contactName` | 经办联系人姓名 | 100 |
| `email` | 经办联系人使用的企业邮箱 | 254 |
| `contactTitle` | 联系人职务 | 100 |
| `authorizationBasis` | 代表企业申请的依据，尚待审核时可填「待核实」 | 500 |
| `industry` | 主营行业代码 | |
| `businessSummary` | 一句话说明主营业务 | 500 |
| `websiteUrl` | **选填**，企业官网或独立站的公开 HTTPS 地址 | 2048 |
| `requestId` | 申请人确认后生成的 UUID v4，同一份申请重试时复用 | |
| `applicantConfirmed` | 申请人明确同意后填写 JSON 布尔值 `true` | |

网址可含页面路径。请使用公开域名，省略登录凭据、查询参数、片段以及非默认端口。留空时省略整个 `websiteUrl` 字段。提交网址仅供审核，网站公开由企业在工作台确认。

## 主营行业

| 行业 | 接口代码 |
| --- | --- |
| 化工与材料 | `CHEMICALS_MATERIALS` |
| 机械与设备 | `MACHINERY_EQUIPMENT` |
| 电气与电子 | `ELECTRICAL_ELECTRONICS` |
| 家具与家居 | `FURNITURE_HOME` |
| 玩具 | `TOYS` |
| 日用品 | `CONSUMER_GOODS` |
| 纺织与服装 | `TEXTILES_APPAREL` |
| 食品与农业 | `FOOD_AGRICULTURE` |
| 包装与印刷 | `PACKAGING_PRINTING` |
| 金属与五金 | `METAL_HARDWARE` |
| 其他 | `OTHER` |

## 合成示例

给每次新申请生成请求 ID。测试留空时，从示例删除 `websiteUrl` 一行。

```json
{
  "requestId": "6d032c28-1b2c-4d52-8743-d408713aa99d",
  "applicantConfirmed": true,
  "companyName": "DEMO 合成新材料科技有限公司",
  "registrationId": "DEMO-REG-20261119",
  "contactName": "合成联系人",
  "email": "factory@example.invalid",
  "contactTitle": "入驻经办人",
  "authorizationBasis": "合成流程中的授权说明，待核实",
  "industry": "CHEMICALS_MATERIALS",
  "websiteUrl": "https://example.com/demo-website-profile",
  "businessSummary": "生产销售工程塑料（合成验收资料）"
}
```

## 提交与回执

运行 `python3 scripts/submit.py`，通过标准输入提供已经确认的 UTF-8 JSON。脚本仅向固定的独立验收站地址 `https://passengers-bridge-hosts-relate.trycloudflare.com/api/ai/factory-applications` 提交请求，禁用代理和重定向。

HTTP 201 及 `{"received":true,"receiptId":"<uuid>"}` 表明请求已收件。以实际返回的受理编号为准。网站和企业资料仍需人工审核。

超时、连接中断或未能核实回执时，将结果告知申请人，待其确认后用原请求 ID 和原内容重试。收到 HTTP 429 时至少等待一分钟。HTTP 409 表示原请求 ID 对应其他内容。修改内容后需重新确认并生成新请求 ID。
