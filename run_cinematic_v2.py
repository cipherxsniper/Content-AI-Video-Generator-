cat > ~/Omega-Studios-Omega/run_cinematic_v2.py << 'EOF'
import time
import os

from core.script_engine import generate_script
from core.scene_engine_v2 import generate_scenes
from tools.scene_visuals_v2 import create_scene_clip
from tools.scene_editor import merge_scenes
from tools.voice_v2 import generate_voice
from tools.render_v2 import render_final

topic = input("🧠 Topic: ")

print("🧠 Generating script...")
script = generate_script(topic)

print("\n📜 SCRIPT:\n", script)

print("\n🎬 Generating scenes...")
scene_text = generate_scenes(script)

print("\n🎞️ Creating scenes...")

scene_files = []
for i in range(4):
    file = f"media/output/scene_{i}.mp4"
    create_scene_clip(file, duration=8)
    scene_files.append(file)

merged = f"media/output/merged_{int(time.time())}.mp4"
merge_scenes(scene_files, merged)

audio = f"media/output/audio_{int(time.time())}.wav"
generate_voice(script, audio)

final = f"media/output/final_{int(time.time())}.mp4"
render_final(merged, audio, final)

print(f"\n✅ FINAL VIDEO: {final}")

# FORCE copy + open correctly
os.system(f"cp {final} /sdcard/Download/final.mp4")
os.system("am start -a android.intent.action.VIEW -d file:///sdcard/Download/final.mp4 -t video/mp4")
EOF
