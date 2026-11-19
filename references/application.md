# 企业入驻申请字段与回执

每份申请对应一家企业，表中字段均为必填。验收使用用户确认的合成资料，登记号、联系人和邮箱均使用合成值。授权依据暂未核对时，可填写「待核实」，由审核人员复核。主营业务填写具体经营活动。报告、产品名、型号、规格和用途在企业进入工作台后按需添加。

| 字段 | 填写内容 | 文本长度上限 |
| --- | --- | ---: |
| `companyName` | 企业登记全称 | 200 |
| `registrationId` | 统一社会信用代码或企业登记号。境外企业可填当地登记号 | 80 |
| `contactName` | 经办联系人姓名 | 100 |
| `email` | 经办联系人使用的企业邮箱 | 254 |
| `contactTitle` | 联系人职务 | 100 |
| `authorizationBasis` | 代表企业申请及处理本次材料的依据 | 500 |
| `industry` | 从主营行业选项中选一项，提交对应代码 | |
| `businessSummary` | 用一句话说明主营业务，例如「生产销售工程塑料」 | 500 |
| `requestId` | 申请人确认后生成的 UUID v4，同一份申请重试时复用 | |
| `applicantConfirmed` | 申请人明确同意后填写 JSON 布尔值 `true` | |

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

## 合成申请示例

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
  "businessSummary": "生产销售工程塑料（合成验收资料）"
}
```

## 提交和回执

客户端运行 `python3 scripts/submit.py`，将合成申请的 UTF-8 JSON **通过标准输入**交给脚本。

脚本只向固定地址 `https://defensive-sort-six-albert.trycloudflare.com/api/ai/factory-applications` 发出 HTTPS POST，禁用地址覆盖和跳转。脚本仅接受 HTTP 201 和 `{"received":true,"receiptId":"<uuid>"}` 回执。回执代表收到申请请求，资质和联系人授权由审核人员核对。已有进行中的申请或账号时，后台对新请求去重，仅记录本次收件。

网络中断后，先说明结果待确认。申请人同意重试时，复用原请求 ID 和完整内容。收到 HTTP 429 时等待至少一分钟，再按同样方式重试。HTTP 409 表示请求 ID 已用于其他内容。修改已确认内容时，重新展示摘要、取得明确同意，并为新请求生成新 ID。

如验收站暂时不可用，等待该站恢复并按上述重试规则处理。
