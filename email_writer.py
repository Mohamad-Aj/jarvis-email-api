import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_email(prompt):
    system_prompt = "You are an AI assistant that writes well-structured, polite, and professional emails."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    response = openai.chat.completions.create(model="gpt-4", messages=messages)

    text = response.choices[0].message.content.strip()

    if "Subject:" in text:
        parts = text.split("Subject:", 1)[1].split("\n", 1)
        subject = parts[0].strip()
        body = parts[1].strip() if len(parts) > 1 else ""
    else:
        subject = "Generated Email"
        body = text

    return {"subject": subject, "body": body}
