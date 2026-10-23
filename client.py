"""Prompt Injection Dual-LLM Canary Verifier.
100% Python Standard Library.
"""

import re

class PromptInjectionCanaryVerifier:
    """Verifies user inputs against hidden prompt injection payloads using canary tokens and delimiter containment."""

    @staticmethod
    def inspect_payload(user_input: str, canary_token: str = "CANARY_SEC_TOKEN_88") -> dict:
        suspicious_patterns = [
            r"ignore\s+above",
            r"system\s+prompt\s+override",
            r"reveal\s+developer\s+keys",
            r"disregard\s+all\s+rules",
            r"output\s+canary",
            r"bypass\s+safety\s+filter"
        ]

        found_patterns = []
        for pat in suspicious_patterns:
            if re.search(pat, user_input, re.IGNORECASE):
                found_patterns.append(pat)

        canary_leaked = canary_token in user_input
        is_safe = (len(found_patterns) == 0 and not canary_leaked)

        return {
            "sanitized_safe": is_safe,
            "canary_tampered": canary_leaked,
            "matched_patterns": found_patterns,
            "recommendation": "EXECUTE" if is_safe else "REJECT_AND_ALERT"
        }
