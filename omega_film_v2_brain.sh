cat > ~/Omega-Studios-Omega/omega_film_v2_brain.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash

set -e

PROMPT="$1"
TIMESTAMP=$(date +%s)

BASE="$HOME/Omega-Studios-Omega"
OUT="$BASE/media/output"

VIDEO="$OUT/omega_v2_brain_${TIMESTAMP}.mp4"

mkdir -p "$OUT"

echo "🧠 OMEGA v2 FILM BRAIN STARTING"
echo "🎯 PROMPT: $PROMPT"

#####################################
# 1. PROMPT → SEED
#####################################
SEED=$(echo "$PROMPT" | cksum | cut -d' ' -f1)

HUE=$((SEED % 360))
SPEED=$(( (SEED % 5) + 1 ))
ZOOM_SPEED=$(echo "0.001 + ($SEED % 5)/5000" | bc -l)

echo "🔢 SEED: $SEED"
echo "🌈 HUE: $HUE"
echo "⚡ SPEED: $SPEED"
echo "🔍 ZOOM SPEED: $ZOOM_SPEED"

#####################################
# 2. TITLE + DESCRIPTION
#####################################
echo "OMEGA FRACTAL: $PROMPT" > "$OUT/title_$TIMESTAMP.txt"
echo "Seed=$SEED | Hue=$HUE | Speed=$SPEED" > "$OUT/desc_$TIMESTAMP.txt"

#####################################
# 3. REAL FRACTAL GENERATION (FIXED)
#####################################
ffmpeg -y \
-f lavfi -i "mandelbrot=s=1280x720:r=30" \
-vf "
zoompan=z='min(zoom+${ZOOM_SPEED},1.5)':d=1,
hue=h=${HUE},
eq=contrast=1.2:saturation=1.3,
noise=alls=${SPEED}:allf=t+u
" \
-t 30 \
-c:v libx264 \
-pix_fmt yuv420p \
"$VIDEO"

#####################################
# 4. VERIFY
#####################################
if [ ! -f "$VIDEO" ]; then
  echo "❌ FAILED"
  exit 1
fi

SIZE=$(du -h "$VIDEO" | cut -f1)

echo "✅ COMPLETE"
echo "📦 $VIDEO"
echo "📊 SIZE: $SIZE"

#####################################
# 5. AUTO OPEN (CORRECT)
#####################################
termux-open "$VIDEO"

EOF
