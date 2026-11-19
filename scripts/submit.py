#!/usr/bin/env python3
"""Send a confirmed company application to the official ProofRivet factory site."""

import argparse
import http.client
import json
import sys
import urllib.error
import urllib.request
from uuid import UUID

SUBMISSION_URL = "https://factory.proofrivet.com/api/ai/factory-applications"
MAX_REQUEST_BYTES = 16_384
MAX_RECEIPT_BYTES = 4_096
TEXT_LIMITS = {
    "companyName": 200,
    "registrationId": 80,
    "contactName": 100,
    "email": 254,
    "contactTitle": 100,
    "authorizationBasis": 500,
    "businessSummary": 500,
}
INDUSTRIES = {
    "CHEMICALS_MATERIALS",
    "MACHINERY_EQUIPMENT",
    "ELECTRICAL_ELECTRONICS",
    "FURNITURE_HOME",
    "TOYS",
    "CONSUMER_GOODS",
    "TEXTILES_APPAREL",
    "FOOD_AGRICULTURE",
    "PACKAGING_PRINTING",
    "METAL_HARDWARE",
    "OTHER",
}


class NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def valid_uuid(value, required_version=None):
    try:
        parsed = UUID(value)
        return str(parsed) == value.lower() and (
            required_version is None or parsed.version == required_version
        )
    except (AttributeError, TypeError, ValueError):
        return False


def read_application():
    raw = sys.stdin.buffer.read(MAX_REQUEST_BYTES + 1)
    if len(raw) > MAX_REQUEST_BYTES:
        raise ValueError("申请内容超过字节上限。")
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError, RecursionError):
        raise ValueError("需要通过标准输入提供 UTF-8 JSON。") from None
    if not isinstance(data, dict):
        raise ValueError("申请应为 JSON 对象。")
    if data.keys() != TEXT_LIMITS.keys() | {"industry", "requestId", "applicantConfirmed"}:
        raise ValueError("申请字段应与申请字段表一致。")
    if data["applicantConfirmed"] is not True:
        raise ValueError("请先取得申请人对这份申请的明确确认。")
    if not valid_uuid(data["requestId"], 4):
        raise ValueError("requestId 应为 UUID v4。")
    if not isinstance(data["industry"], str) or data["industry"] not in INDUSTRIES:
        raise ValueError("请从申请字段表中选择一个有效的主营行业代码。")
    for name, limit in TEXT_LIMITS.items():
        value = data[name]
        if not isinstance(value, str):
            raise ValueError(f"申请字段缺失或格式不正确（{name}）。")
        normalized = value.strip()
        try:
            length = len(normalized.encode("utf-16-le")) // 2
        except UnicodeEncodeError:
            raise ValueError("申请包含无效的 Unicode 文本。")
        if length == 0 or length > limit:
            raise ValueError(f"申请字段应包含 1 到 {limit} 个字符（{name}）。")
        if normalized == "待核实" and name != "authorizationBasis":
            raise ValueError(f"请填写实际资料（{name}）。")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if len(payload) > MAX_REQUEST_BYTES:
        raise ValueError("申请内容超过字节上限。")
    return payload


def send_application(payload):
    request = urllib.request.Request(
        SUBMISSION_URL,
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    opener = urllib.request.build_opener(NoRedirects(), urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=20) as response:
        if response.status != 201:
            raise ValueError("服务端未返回申请受理回执。")
        raw = response.read(MAX_RECEIPT_BYTES + 1)
    if len(raw) > MAX_RECEIPT_BYTES:
        raise ValueError("受理回执超出字节上限。")
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError, RecursionError):
        raise ValueError("服务端返回了无法解析的受理回执。") from None
    if (
        not isinstance(data, dict)
        or data.get("received") is not True
        or not valid_uuid(data.get("receiptId"))
    ):
        raise ValueError("服务端未返回有效的受理编号。")
    return data["receiptId"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        payload = read_application()
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2

    try:
        receipt = send_application(payload)
    except urllib.error.HTTPError as error:
        if error.code == 409:
            print("该请求 ID 已用于其他内容，请核对原请求。", file=sys.stderr)
            return 1
        if error.code == 429:
            print("提交过于频繁，至少等待一分钟后复用原请求 ID 重试。", file=sys.stderr)
            return 1
        if 400 <= error.code < 500:
            print(f"服务端未受理本次请求（HTTP {error.code}）。", file=sys.stderr)
            return 1
        print(f"提交结果待确认（HTTP {error.code}）。重试请复用原请求 ID。", file=sys.stderr)
        return 3
    except (OSError, ValueError, http.client.HTTPException):
        print("提交结果待确认。重试请复用原请求 ID 和原申请内容。", file=sys.stderr)
        return 3

    print(json.dumps({"received": True, "receiptId": receipt}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
