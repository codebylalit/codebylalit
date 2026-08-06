import sys
import os
from PIL import Image, ImageEnhance

def prep_photo(input_path: str, output_path: str = "source-prepped.png"):
    if not os.path.exists(input_path):
        print(f"Error: Input photo '{input_path}' not found.")
        sys.exit(1)

    print(f"Processing '{input_path}'...")

    try:
        from rembg import remove
        input_img = Image.open(input_path)
        nobg_img = remove(input_img)
        img_rgba = nobg_img.convert("RGBA")
    except Exception as e:
        print(f"Note: rembg background removal fallback ({e})...")
        img_rgba = Image.open(input_path).convert("RGBA")

    gray = img_rgba.convert("L")
    enhancer = ImageEnhance.Contrast(gray)
    enhanced = enhancer.enhance(1.8)

    white_bg = Image.new("L", gray.size, 255)
    alpha = img_rgba.split()[3]
    final_img = Image.composite(enhanced, white_bg, alpha)

    final_img.save(output_path)
    print(f"Prepped photo saved to '{output_path}'.")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    out = sys.argv[2] if len(sys.argv) > 2 else "source-prepped.png"
    prep_photo(src, out)
