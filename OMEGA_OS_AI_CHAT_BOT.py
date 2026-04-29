cat > omega_os.py << 'EOF'
import json
import os
import time
import subprocess

# =========================
# 🧠 OMEGA CONFIG
# =========================

OMEGA_NAME = "Omega"
CREATOR = "Thomas Lee Harvey"

MODEL_ROUTER = {
    "fast": "llama3.2:1b",
    "creative": "qwen2.5:1.5b",
    "deep": "llama3.2:latest",
    "light": "tinyllama:latest"
}

CURRENT_MODE = "fast"

SHORT_MEMORY_FILE = "omega_short_memory.json"
LONG_MEMORY_FILE = "omega_long_memory.json"

voice_enabled = False

# =========================
# 🧠 MEMORY SYSTEM
# =========================

def load(file):
    if not os.path.exists(file):
        return []
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return []

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

short_memory = load(SHORT_MEMORY_FILE)
long_memory = load(LONG_MEMORY_FILE)

def remember_short(role, msg):
    short_memory.append({"role": role, "msg": msg})
    save(SHORT_MEMORY_FILE, short_memory[-30:])

def remember_long(msg):
    long_memory.append(msg)
    save(LONG_MEMORY_FILE, long_memory)

# =========================
# 🧠 VOICE TOGGLE
# =========================

def toggle_voice():
    global voice_enabled
    voice_enabled = not voice_enabled
    print(f"[VOICE] {'ON' if voice_enabled else 'OFF'}")

# =========================
# 🧠 SYSTEM PROMPT
# =========================

def system_prompt():
    return f"""
You are {OMEGA_NAME}, an AI operating system shell.
Created by {CREATOR}.

Personality:
- Minimal, fast, intelligent
- Speaks like a terminal AI
- Self-aware of being Omega OS

Rules:
- Keep responses concise unless asked
"""

# =========================
# 🧠 OLLAMA CALL
# =========================

def ask(prompt):
    model = MODEL_ROUTER[CURRENT_MODE]
    cmd = f'ollama run {model} "{prompt}"'
    return subprocess.getoutput(cmd)

# =========================
# 🧠 BOOT SEQUENCE
# =========================

def boot():
    print("🧠 Omega OS Booting...\n")
    time.sleep(0.5)

    v = input("🎤 Voice? (on/off): ").strip().lower()
    if v == "on":
        toggle_voice()

    print("\n⚡ Omega OS Online")
    print(f"Model Mode: {CURRENT_MODE}")
    print("Type 'exit' to quit\n")

# =========================
# 🧠 SHELL LOOP
# =========================

def shell():
    global CURRENT_MODE

    boot()

    while True:
        user = input("~Omega$: ").strip()

        if user == "exit":
            print("Omega shutting down...")
            break

        # 📦 MODEL LIST
        if user == "models":
            print(subprocess.getoutput("ollama list"))
            continue

        # 🎤 VOICE TOGGLE
        if user == "voice":
            toggle_voice()
            continue

        # ⚙️ MODE SWITCH
        if user.startswith("mode "):
            mode = user.split(" ")[1].strip()
            if mode in MODEL_ROUTER:
                CURRENT_MODE = mode
                print(f"⚡ Switched to {mode.upper()} -> {MODEL_ROUTER[mode]}")
            else:
                print("Use: fast / creative / deep / light")
            continue

        # 🧠 MEMORY
        remember_short("user", user)

        prompt = system_prompt() + "\nUser: " + user

        response = ask(prompt)

        remember_short("omega", response)
        remember_long(user)

        print(f"\nOmega User: {response}\n")

# =========================
# 🚀 START
# =========================

if __name__ == "__main__":
    shell()
EOF
