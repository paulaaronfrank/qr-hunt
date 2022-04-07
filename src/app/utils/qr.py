# import modules
import qrcode
from PIL import Image
from . import Config
import requests


def create_qr_code(qr_id):
    if Config.IMG_URL:
        icon = Image.open(requests.get(Config.IMG_URL, stream=True).raw)
    else:
        icon = Image.open('app/assets/icon.jpg')
    h_size = int((float(icon.size[1]) * float((100 / float(icon.size[0])))))
    icon = icon.resize((100, h_size), Image.ANTIALIAS)

    qr_code = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    url = Config.BASE_URL + qr_id

    qr_code.add_data(url)
    qr_code.make()
    qr_color = Config.COLOR
    qr_img = qr_code.make_image(fill_color=qr_color, back_color="white").convert('RGB')
    pos = ((qr_img.size[0] - icon.size[0]) // 2,
           (qr_img.size[1] - icon.size[1]) // 2)
    qr_img.paste(icon, pos)
    qr_img.save(f'app/codes/{qr_id}.png')
    return qr_img
