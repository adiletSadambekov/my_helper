from PIL import Image, ImageDraw, ImageFont
import logging

logging.getLogger('App.utill.generate_images.py')

def generate_for_items(num_image: int, text: str, width=400, higth=400, size=98) -> bool:
    logger = logging.getLogger(
        'App.utill.generate_images.get_for_items')

    try:
        img = Image.open('static/images/templates/img%s.jpg' % (str(num_image)))
        font = ImageFont.truetype('static/fonts/Stanberry.ttf', size)
        draw = ImageDraw.Draw(img)
        draw.text((width, higth), text, fill='white', font=font)
        img.save('static/images/done/current_items.jpg')
        return True
    except Exception as e:
        logger.exception(e)
        return False
