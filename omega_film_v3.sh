cat > ~/Omega-Studios-Omega/omega_film_v3.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash

set -e

PROMPT="$1"
TIMESTAMP=$(date +%s)

BASE="$HOME/Omega-Studios-Omega"
OUT="$BASE/media/output"
SCENES="$OUT/v3_scenes_$TIMESTAMP"
LIST="$OUT/list_$TIMESTAMP.txt"
FINAL="$OUT/omega_v3_${TIMESTAMP}.mp4"

mkdir -p "$OUT"
mkdir -p "$SCENES"

echo "🧠 OMEGA v3 HYBRID FILM BRAIN"
echo "🎯 PROMPT: $PROMPT"

#####################################
# 1. BASE SEED
#####################################
BASE_SEED=$(echo "$PROMPT" | cksum | cut -d' ' -f1)
echo "🔢 BASE SEED: $BASE_SEED"

#####################################
# 2. TITLE + DESCRIPTION
#####################################
echo "OMEGA v3 FILM: $PROMPT" > "$OUT/title_$TIMESTAMP.txt"
echo "Hybrid fractal film system | Seed=$BASE_SEED | 4 scenes" > "$OUT/desc_$TIMESTAMP.txt"

#####################################
# 3. GENERATE SCENES
#####################################
> "$LIST"

for i in 0 1 2 3
do
  SEED=$((BASE_SEED + i*777))

  HUE=$((SEED % 360))
  SPEED=$(( (SEED % 5) + 1 ))

  ZOOM_SPEED=$(echo "0.001 + ($SEED % 5)/5000" | bc -l)

  SCENE_FILE="$SCENES/scene_${i}.mp4"

  echo "🎬 Scene $i | HUE=$HUE SPEED=$SPEED"

  ffmpeg -y \
  -f lavfi -i "mandelbrot=s=1280x720:r=30" \
  -vf "
  zoompan=z='min(zoom+${ZOOM_SPEED},1.5)':d=1,
  hue=h=${HUE},
  eq=contrast=1.2:saturation=1.3,
  noise=alls=${SPEED}:allf=t+u
  " \
  -t 7.5 \
  -c:v libx264 \
  -pix_fmt yuv420p \
  "$SCENE_FILE"

  echo "file '$SCENE_FILE'" >> "$LIST"
done

#####################################
# 4. CONCAT SCENES (REAL CUT SYSTEM)
#####################################
ffmpeg -y \
-f concat -safe 0 -i "$LIST" \
-c copy \
"$FINAL"

#####################################
# 5. VALIDATION
#####################################
if [ ! -f "$FINAL" ]; then
  echo "❌ FINAL VIDEO FAILED"
  exit 1
fi

SIZE=$(du -h "$FINAL" | cut -f1)

echo "✅ OMEGA v3 COMPLETE"
echo "📦 $FINAL"
echo "📊 SIZE: $SIZE"

#####################################
# 6. AUTO OPEN
#####################################
termux-open "$FINAL"

EOF
