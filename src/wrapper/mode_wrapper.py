#!/usr/bin/env python3
"""
Minimal wrapper that forces GPT requests into FLOW or VERIFY mode
and protects <KEEP-AS-IS> blocks.
"""

import os, re, sys, argparse, json
import openai
from pathlib import Path

TEMPLATES = {
    "flow": Path("prompt_flow.txt").read_text(),
    "verify": Path("prompt_verify.txt").read_text(),
}

# very simple VERIFY-mode drift filter
DISALLOWED_VERIFY_PHRASES = {"😊", "😉", "I feel", "in my opinion"}

def protect_keep_blocks(text: str) -> str:
    """Wrap <KEEP-AS-IS> … </KEEP-AS-IS> content in triple back-ticks."""
    return re.sub(
        r"<KEEP-AS-IS>(.*?)</KEEP-AS-IS>",
        lambda m: f"```{m.group(1)}```",
        text,
        flags=re.DOTALL,
    )

def violates_verify(output: str, original_blocks):
    if any(p in output for p in DISALLOWED_VERIFY_PHRASES):
        return "Contains informal/disallowed phrasing."
    for block in original_blocks:
        if block not in output:
            return "KEEP-AS-IS block altered or missing."
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["flow", "verify"], required=True)
    parser.add_argument("prompt", nargs="+")
    args = parser.parse_args()

    mode = args.mode
    user_msg = " ".join(args.prompt)
    system_prompt = TEMPLATES[mode]

    # extract KEEP blocks for later comparison
    keep_blocks = re.findall(r"<KEEP-AS-IS>(.*?)</KEEP-AS-IS>", user_msg, re.DOTALL)

    user_msg_protected = protect_keep_blocks(user_msg)

    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg_protected},
        ],
        temperature=0.2 if mode == "verify" else 0.7,
    )
    output = response.choices[0].message.content.strip()

    if mode == "verify":
        violation = violates_verify(output, keep_blocks)
        if violation:
            sys.stderr.write(f"[VERIFY-BLOCKED] {violation}\n")
            sys.exit(1)

    print(output)

if __name__ == "__main__":
    main()
