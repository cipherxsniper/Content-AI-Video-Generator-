cat > omega_os.py << 'EOF'
import os
import time
import sys
import json
import requests
import threading

# =========================
# ⚡ OMEGA REAL-TIME ENGINE
# =========================

MODEL = "llama3.2:1b"
API_URL = "http://127.0.0.1:11434/api/generate"

voice_enabled = False
memory_file = "omega_memory.json"

GREEN = "\033[92m"
RESET = "\033[0m"

# =========================
# 🧠 PROMPT UI
# =========================

def prompt():
    return f"{GREEN}~Omega${RESET} "

# =========================
# 🧠 MEMORY
# =========================

def load():
    if not os.path.exists(memory_file):
        return []
    try:
        with open(memory_file, "r") as f:
            return json.load(f)
    except:
        return []

def save(data):
    with open(memory_file, "w") as f:
        json.dump(data[-50:], f, indent=2)

memory = load()

def remember(role, msg):
    memory.append({"role": role, "msg": msg})
    save(memory)

# =========================
# 🎤 VOICE ENGINE (SMOOTH)
# =========================

def toggle_voice():
    global voice_enabled
    voice_enabled = not voice_enabled
    print(f"[VOICE] {'ON (smooth)' if voice_enabled else 'OFF'}")

def speak(text):
    if voice_enabled:
        os.system(f'espeak -s 160 -p 45 -v en-us+f3 "{text}" 2>/dev/null')

# =========================
# ⚡ REAL-TIME STREAMING (OLLAMA SSE STYLE)
# =========================

def stream_ollama(prompt_text):
    payload = {
        "model": MODEL,
        "prompt": prompt_text,
        "stream": True
    }

    response = requests.post(API_URL, json=payload, stream=True)

    full_text = ""

    print("\nOmega: ", end="", flush=True)

    for line in response.iter_lines():
        if line:
            try:
                chunk = json.loads(line.decode("utf-8"))
                token = chunk.get("response", "")

                sys.stdout.write(token)
                sys.stdout.flush()

                full_text += token

            except:
                pass

    print("\n")

    return full_text

# =========================
# 🧠 SYSTEM PROMPT
# =========================

def system_prompt():
    return """
You are Omega, a real-time AI assistant.
Be concise, fast, and conversational.
"""

# =========================
# 🧠 BOOT
# =========================

def boot():
    print("🧠 Omega Real-Time Booting...\n")
    time.sleep(0.4)

    v = input("🎤 Voice (smooth)? on/off: ").strip().lower()
    if v == "on":
        toggle_voice()

    print("\n⚡ Omega LIVE MODE ACTIVE")
    print("Streaming responses enabled")
    print("Type 'exit' to quit\n")

# =========================
# 🧠 SHELL LOOP
# =========================

def shell():
    boot()

    while True:
        user = input(prompt()).strip()

        if user == "exit":
            print("Omega shutting down...")
            break

        if user == "voice":
            toggle_voice()
            continue

        if user == "models":
            print("Active Model: llama3.2:1b")
            continue

        remember("user", user)

        prompt_text = system_prompt() + "\nUser: " + user

        # ⚡ REAL-TIME STREAMING RESPONSE
        response = stream_ollama(prompt_text)

        remember("omega", response)

        speak(response)

# =========================
# 🚀 START
# =========================

if __name__ == "__main__":
    shell()
EOF
