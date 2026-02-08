"""
AI 财报解析助手：解析财报片段并返回结构化数字。
使用标准库进行 HTTP 请求，避免新增依赖。
"""
from __future__ import annotations

import json
import os
import re
import urllib.request
from typing import Dict, Optional, Tuple


def _extract_json(text: str) -> Dict:
    """
    从模型输出中提取 JSON。
    允许输出包含解释性文本，提取第一个 {...} 作为 JSON。
    """
    if not text:
        return {}
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return {}
    raw = text[start : end + 1]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # 尝试清理多余逗号
        raw = re.sub(r",\s*}", "}", raw)
        raw = re.sub(r",\s*]", "]", raw)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}


def _openai_chat(text: str, model: str, api_key: str) -> Tuple[Dict, str]:
    url = "https://api.openai.com/v1/chat/completions"
    prompt = _build_prompt(text)
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "你是财报解析助手，只输出 JSON。",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.0,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    data = json.loads(raw)
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    return _extract_json(content), content


def _anthropic_chat(text: str, model: str, api_key: str) -> Tuple[Dict, str]:
    url = "https://api.anthropic.com/v1/messages"
    prompt = _build_prompt(text)
    payload = {
        "model": model,
        "max_tokens": 800,
        "temperature": 0.0,
        "messages": [{"role": "user", "content": prompt}],
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    data = json.loads(raw)
    content = ""
    if data.get("content") and isinstance(data["content"], list):
        content = data["content"][0].get("text", "")
    return _extract_json(content), content


def _build_prompt(text: str) -> str:
    return f"""
你将从财报片段中提取可量化数字。请严格输出 JSON，不要输出其他文本。

字段说明（单位约定）：
- ppe_adjustment_b: PPE 调整额（十亿美元 $B）
- land_area_k_sqft: 土地面积（千平方英尺）
- land_price_per_sqft: 土地单价（美元/平方英尺）
- building_area_k_sqft: 建筑面积（千平方英尺）
- building_price_per_sqft: 建筑单价（美元/平方英尺）
- depreciation_b: 折旧与摊销（十亿美元 $B）
- capex_b: 资本支出（十亿美元 $B）
- rou_b: 经营租赁使用权资产（十亿美元 $B）
- notes: 任何补充说明（字符串）

若未找到字段，请返回 null。

财报片段：
\"\"\"{text}\"\"\"
"""


def parse_financial_text(
    text: str,
    provider: str = "openai",
    model: str = "gpt-4o",
    api_key_override: Optional[str] = None,
) -> Tuple[Optional[Dict], str, Optional[str]]:
    """
    解析财报片段。
    Returns: (parsed_dict, raw_response, error_message)
    """
    if not text or not text.strip():
        return None, "", "文本为空"
    provider = (provider or "").lower()
    if provider == "openai":
        api_key = api_key_override or os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            return None, "", "缺少 OPENAI_API_KEY"
        parsed, raw = _openai_chat(text, model, api_key)
        return parsed or None, raw, None
    if provider == "anthropic":
        api_key = api_key_override or os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key:
            return None, "", "缺少 ANTHROPIC_API_KEY"
        parsed, raw = _anthropic_chat(text, model, api_key)
        return parsed or None, raw, None
    return None, "", "未知 provider"

