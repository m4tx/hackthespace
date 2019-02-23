from PIL import Image

from game.utils.images import put_text_on_image


def generate_image(
        source_path: str, dest_path: str, text: str, font_name: str,
        font_size: int, fill):
    img = Image.open(source_path).convert('RGBA')
    txt = Image.new('RGBA', img.size, (0, 0, 0, 0))

    put_text_on_image(txt, text, font_name, font_size, fill)
    combined = Image.alpha_composite(img, txt)

    combined.save(dest_path)
