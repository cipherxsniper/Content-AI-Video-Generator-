cat > ~/Omega-Studios-Omega/tools/voice_v2.py << 'EOF'
import os
import time

def generate_voice(script, output):
    tmp = "/sdcard/Download/tmp_voice.wav"

    safe = script.replace('"','').replace("\n"," ")

    # Speak OUT LOUD (Termux TTS)
    os.system(f'termux-tts-speak "{safe[:2000]}"')

    # Record system audio (fallback mic capture)
    print("🎙️ Recording fallback audio...")

    os.system(f"""
    ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=mono \
    -t 60 -q:a 9 -acodec pcm_s16le "{output}"
    """)

    return output
EOF
