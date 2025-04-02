import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_email(prompt):
    system_prompt = (
        "You are JARVIS, a smart AI assistant that writes emails based on user intent and tone.\n"
        "The email should match the context and sound natural — professional when needed, casual if appropriate, funny if asked.\n"
        "Always write the email in a clean, readable structure.\n"
        "Start the output with 'Subject: ...' and then add the email body.\n"
        "Be helpful, engaging, and adjust your style to fit the user’s request."
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
