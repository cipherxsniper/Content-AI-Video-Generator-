cat > ~/Omega-Studios-Omega/tools/scene_visuals_v2.py << 'EOF'
import os
import random

def create_scene_clip(output, mood="dark", duration=8):

    if "dark" in mood:
        source = "mandelbrot"
    elif "tech" in mood:
        source = "life"
    else:
        source = "testsrc"

    effects = [
        "zoompan=z='min(zoom+0.002,1.4)':d=125",
        "tblend=all_mode=average",
        "edgedetect",
        "hue=s=0",
    ]

    effect = random.choice(effects)

    cmd = f"""
    ffmpeg -y \
    -f lavfi -i {source}=size=1080x1920:rate=30 \
    -vf "{effect},scale=1080:1920" \
    -t {duration} \
    -pix_fmt yuv420p \
    -c:v libx264 \
    "{output}"
    """

    os.system(cmd)
    return output
EOF
