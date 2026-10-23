"""MCP server for Prompt Injection Dual-LLM Canary Verifier."""
import sys
import json
from client import PromptInjectionCanaryVerifier

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "verify_prompt_payload",
                "description": "Inspects prompt strings for injection attempts and canary tampering",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_input": {"type": "string"},
                        "canary_token": {"type": "string"}
                    },
                    "required": ["user_input"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "verify_prompt_payload":
            args = params.get("arguments", {})
            res = PromptInjectionCanaryVerifier.inspect_payload(
                args.get("user_input", ""),
                args.get("canary_token", "CANARY_SEC_TOKEN_88")
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
