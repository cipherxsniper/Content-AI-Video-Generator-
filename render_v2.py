cat > ~/Omega-Studios-Omega/tools/render_v2.py << 'EOF'
import os

def render_final(video, audio, output):

    if not os.path.exists(video):
        raise Exception("VIDEO MISSING")

    if not os.path.exists(audio):
        print("⚠️ Missing audio, injecting silent track...")
        os.system(f"""
        ffmpeg -y -i "{video}" \
        -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
        -shortest -c:v copy -c:a aac "{output}"
        """)
        return output

    os.system(f"""
    ffmpeg -y -i "{video}" -i "{audio}" \
    -c:v libx264 -pix_fmt yuv420p \
    -c:a aac -shortest \
    -movflags +faststart \
    "{output}"
    """)

    return output
EOF
