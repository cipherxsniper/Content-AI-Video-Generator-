cat > ~/Omega-Studios-Omega/core/scene_engine_v2.py << 'EOF'
import requests

OLLAMA = "http://127.0.0.1:11434/api/generate"
MODEL = "qwen2.5:1.5b"

def generate_scenes(script):
    prompt = f"""
Turn this into 4 scenes.

Each scene:
TITLE:
MOOD: (dark, futuristic, intense)
VISUAL:

SCRIPT:
{script}
"""

    try:
        r = requests.post(OLLAMA, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=15)

        data = r.json()

        if "response" in data:
            return data["response"]

    except:
        pass

    return """Scene 1
MOOD: dark

Scene 2
MOOD: intense

Scene 3
MOOD: futuristic

Scene 4
MOOD: dark
"""
EOF
