

import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

from app.services.vector_db_service import (
    get_security_context
)


def extract_json(text: str) -> dict:
    """
    Extract JSON even if model adds extra text accidentally
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM output")

    return json.loads(match.group())

def analyze_architecture_with_llm(
    architecture_text: str
) -> dict:

    # Retrieve relevant security knowledge
    security_context = get_security_context(
        architecture_text
    )

    enhanced_prompt = f"""
Architecture:

{architecture_text}

Relevant Security Knowledge:

{security_context}

Analyze this architecture from a security perspective.

Identify:
- Authentication issues
- Authorization issues  
- Data protection issues
- Network security issues
- Infrastructure risks
- Cloud security risks
- DevSecOps risks

Return ONLY valid JSON in this exact format:
{{
  "findings": [
    {{
      "title": "string",
      "severity": "LOW|MEDIUM|HIGH|CRITICAL",
      "stride": "string",
      "owasp": "string",
      "mitre": ["string"],
      "recommendation": "string"
    }}
  ]
}}
"""


    response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a senior security architect. "
                "You MUST respond with ONLY a valid JSON object. "
                "No markdown, no code blocks, no backticks, no explanation. "
                "Start your response with { and end with }.\n\n"
                "JSON format:\n"
                "{\n"
                "  \"findings\": [\n"
                "    {\n"
                "      \"title\": \"string\",\n"
                "      \"severity\": \"LOW|MEDIUM|HIGH|CRITICAL\",\n"
                "      \"stride\": \"Spoofing|Tampering|Repudiation|Information Disclosure|Denial of Service|Elevation of Privilege\",\n"
                "      \"owasp\": \"OWASP Top 10 category\",\n"
                "      \"mitre\": [\"MITRE technique IDs\"],\n"
                "      \"recommendation\": \"Concrete mitigation steps\"\n"
                "    }\n"
                "  ]\n"
                "}"
            )
        },
        {
            "role": "user",
            "content": enhanced_prompt
        }
    ],
    temperature=0.1,       # ← lower temperature for more deterministic output
    max_tokens=1500        # ← increase tokens so JSON doesn't get cut off
)
    print("\n========== FINAL PROMPT ==========")
    print(enhanced_prompt)

    raw_output = response.choices[0].message.content

    print("Retrieved Security Context:")
    print(security_context)

    print("Raw LLM Output:")
    print(repr(raw_output))

    try:
        parsed_json = extract_json(raw_output)

    except Exception as e:
        print("LLM returned invalid JSON:")
        print(raw_output)
        raise e

    return parsed_json
