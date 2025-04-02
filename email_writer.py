import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_email(prompt):
    system_prompt = (
        "You are JARVIS, an intelligent email-writing assistant.\n"
        "You generate short, clear, and effective emails based on the user's prompt.\n"
        "The tone should adapt to the context — professional, casual, friendly, or even witty — based on what the user asks.\n"
        "Limit the email to 150 words maximum unless the user asks for something longer.\n"
        "Always start with 'Subject: ...' followed by the email body on the next line.\n"
        "Avoid unnecessary fluff, and focus on clarity and purpose."
    )

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
