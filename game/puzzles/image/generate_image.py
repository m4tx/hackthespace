from PIL import Image, ImageFont, ImageDraw


def put_text_on_image(
        source_path: str, dest_path: str, text: str, font_name: str,
        font_size: int):
    img = Image.open(source_path).convert('RGBA')
    txt = Image.new('RGBA', img.size, (0, 0, 0, 0))

    font = ImageFont.truetype(font_name, font_size)
    d = ImageDraw.Draw(txt)

    w, h = d.textsize(text, font=font)
    center_w = (img.size[0] - w) // 2
    center_h = (img.size[1] - h) // 2
    d.text((center_w, center_h), text, fill=(255, 255, 255, 1), font=font)
    combined = Image.alpha_composite(img, txt)

    combined.save(dest_path)
