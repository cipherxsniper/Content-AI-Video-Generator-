cat > ~/Omega-Studios-Omega/run_omega.py << 'EOF'
import os
import time
import math
import random
import hashlib
from pathlib import Path
import subprocess

BASE = Path.home() / "Omega-Studios-Omega"
OUT = BASE / "media/output"
FRAMES = OUT / "frames"
OUT.mkdir(parents=True, exist_ok=True)
FRAMES.mkdir(parents=True, exist_ok=True)

FPS = 30
DURATION = 30
TOTAL_FRAMES = FPS * DURATION

def seed(prompt):
    return int(hashlib.sha256(prompt.encode()).hexdigest(), 16) % 10**8

def math_field(x, t, s):
    # procedural visual math field (this drives animation)
    return (
        math.sin(x * 0.1 + t * 0.05 + s) +
        math.cos(x * 0.07 - t * 0.03) +
        math.sin((x + t) * 0.02)
    )

def generate_frames(prompt, s):
    print("🎬 Generating frames...")

    for t in range(TOTAL_FRAMES):
        frame_path = FRAMES / f"frame_{t:04d}.ppm"

        width, height = 320, 320

        with open(frame_path, "w") as f:
            f.write("P3\n{} {}\n255\n".format(width, height))

            for y in range(height):
                for x in range(width):
                    v = math_field(x, t, s)

                    r = int((math.sin(v + t*0.02) + 1) * 127)
                    g = int((math.cos(v + x*0.01) + 1) * 127)
                    b = int((math.sin(v * 0.5) + 1) * 127)

                    f.write(f"{r} {g} {b} ")

        if t % 30 == 0:
            print(f"frame {t}/{TOTAL_FRAMES}")

def render_video(s):
    output = OUT / f"final_{s}.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES / "frame_%04d.ppm"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-t", str(DURATION),
        str(output)
    ]

    print("🎥 Encoding video...")
    subprocess.run(cmd)

    return output

def open_video(path):
    subprocess.run(["termux-open", str(path)])

def main(prompt):
    s = seed(prompt)
    print("🧠 Seed:", s)

    generate_frames(prompt, s)
    video = render_video(s)

    print("✅ DONE:", video)
    open_video(video)

if __name__ == "__main__":
    import sys
    main(" ".join(sys.argv[1:]))
EOF
