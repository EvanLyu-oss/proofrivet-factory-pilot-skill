#!/usr/bin/env python3
"""Send a confirmed ProofRivet factory onboarding application from standard input."""

import argparse
import http.client
import json
import re
import sys
import urllib.error
import urllib.request
from uuid import UUID

OFFICIAL_ORIGIN = "https://factory.proofrivet.com"
APPLICATION_PATH = "/api/ai/factory-applications"
MAX_REQUEST_BYTES = 16_384
MAX_RECEIPT_BYTES = 4_096
TEXT_LIMITS = {
    "companyName": 200,
    "contactName": 100,
    "email": 254,
    "contactTitle": 100,
    "authorizationBasis": 500,
    "productName": 200,
    "productModel": 100,
    "productSpecification": 300,
    "productUse": 300,
    "materialSummary": 500,
}


class NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def demo_origin(value):
    match = re.fullmatch(r"http://(127\.0\.0\.1|\[::1\]):([1-9][0-9]{0,4})", value)
    if not match or int(match.group(2)) > 65535:
        raise argparse.ArgumentTypeError(
            "use an explicit loopback origin, such as http://127.0.0.1:3100"
        )
    return value


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
    if data.keys() != TEXT_LIMITS.keys() | {"requestId", "applicantConfirmed"}:
        raise ValueError("申请字段应与申请字段表一致。")
    if data["applicantConfirmed"] is not True:
        raise ValueError("请先取得申请人对这份申请的明确确认。")
    if not valid_uuid(data["requestId"], 4):
        raise ValueError("requestId 应为 UUID v4。")
    for name, limit in TEXT_LIMITS.items():
        value = data[name]
        if not isinstance(value, str):
            raise ValueError(f"申请字段缺失或格式不正确（{name}）。")
        try:
            length = len(value.strip().encode("utf-16-le")) // 2
        except UnicodeEncodeError:
            raise ValueError("申请包含无效的 Unicode 文本。")
        if length == 0 or length > limit:
            raise ValueError(f"申请字段应包含 1 到 {limit} 个字符（{name}）。")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if len(payload) > MAX_REQUEST_BYTES:
        raise ValueError("申请内容超过字节上限。")
    return payload


def send_application(payload, origin, is_demo):
    request = urllib.request.Request(
        origin + APPLICATION_PATH,
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    handlers = [NoRedirects()]
    if is_demo:
        handlers.append(urllib.request.ProxyHandler({}))
    with urllib.request.build_opener(*handlers).open(request, timeout=20) as response:
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
    parser.add_argument(
        "--demo-origin", type=demo_origin, help="explicit loopback origin for synthetic acceptance"
    )
    args = parser.parse_args()
    try:
        payload = read_application()
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2

    try:
        receipt = send_application(
            payload, args.demo_origin or OFFICIAL_ORIGIN, is_demo=bool(args.demo_origin)
        )
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
