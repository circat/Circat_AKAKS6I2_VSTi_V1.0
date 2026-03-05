import os
from PIL import Image

# Pfad zu deinen hochgeladenen Bildern
IMAGE_DIR = r"C:\Users\erich\.gemini\antigravity\brain\128d5d06-9ace-438c-85d0-97b83d50d913"
# Zielordner für die ausgeschnittenen Assets
ASSETS_DIR = r"f:\S612VSTi\Assets"

os.makedirs(ASSETS_DIR, exist_ok=True)

# Finde das erste JPG-Bild im Ordner als Basis
image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")]

if not image_files:
    print("Keine Bilder gefunden.")
    exit(1)

# Wir nehmen das erste hochauflösende Bild
source_image_path = os.path.join(IMAGE_DIR, image_files[0])
print(f"Lade Basisbild: {source_image_path}")

try:
    img = Image.open(source_image_path)
    width, height = img.size
    print(f"Bildgröße: {width}x{height}")
    
    # HINWEIS: Diese Koordinaten (left, upper, right, lower) sind Schätzungen!
    # Da ich das Bild nicht visuell sehen kann, müssen diese Werte eventuell von dir 
    # feinjustiert werden. Das Skript schneidet dir die Teile als Basis aus.
    
    # Beispiel-Koordinaten (prozentual oder geschätzt)
    regions = {
        "knob_rec.png": (width * 0.15, height * 0.4, width * 0.25, height * 0.6),
        "knob_monitor.png": (width * 0.25, height * 0.4, width * 0.32, height * 0.6),
        "fader_start.png": (width * 0.5, height * 0.3, width * 0.55, height * 0.7),
        "display_7seg.png": (width * 0.4, height * 0.3, width * 0.48, height * 0.45),
        "btn_new.png": (width * 0.25, height * 0.65, width * 0.32, height * 0.75),
        "panel_section.png": (width * 0.1, height * 0.2, width * 0.9, height * 0.8)
    }

    print("Schneide Assets aus...")
    
    for name, box in regions.items():
        # Stelle sicher, dass die Box im Bild liegt
        box = (
            max(0, int(box[0])),
            max(0, int(box[1])),
            min(width, int(box[2])),
            min(height, int(box[3]))
        )
        
        cropped_img = img.crop(box)
        output_path = os.path.join(ASSETS_DIR, name)
        cropped_img.save(output_path)
        print(f"Gespeichert: {name} ({box[2]-box[0]}x{box[3]-box[1]} px)")

    print("Fertig! Alle Bilder liegen im Ordner f:\\S612VSTi\\Assets")

except Exception as e:
    print(f"Fehler beim Verarbeiten des Bildes: {e}")
