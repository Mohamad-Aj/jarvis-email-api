import openai
import os
import threading

openai.api_key = os.getenv("OPENAI_API_KEY")


# ---------------- WARM-UP (cold-start killer) ----------------
def _warm_up():
    """
    One fire-and-forget request that runs as soon as the module is
    imported.  It costs < 1¢ / month on gpt-4o-mini and chops 3-5 s
    off the first real request.
    """
    try:
        openai.chat.completions.create(
            model="gpt-4o-mini",  # tiny, cheap, instant
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1,
        )
        print("[warm-up] OK")
    except Exception as e:
        # Never crash the app if Render is still pulling secrets, etc.
        print(f"[warm-up] {e}")


# launch the warm-up in a daemon thread immediately
threading.Thread(target=_warm_up, daemon=True).start()


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
