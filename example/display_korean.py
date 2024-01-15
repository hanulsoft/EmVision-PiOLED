#! /usr/bin/python3
"""한글 출력 예제
Author: SungWan Jin(jin.seungwan@hanulsoft.co.kr)

한글을 출력하고 간단한 애니메이션을 보여줍니다.

CopyRight(C) 2020 HanulSoft Inc.
MIT License
"""
import os
import time

import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

KOREAN_TEXT = "안녕하세요\nEmVision입니다"
KOREAN_FONT = ImageFont.truetype("NotoSansCJK-Regular.ttc", 12)
IMAGE_VEL = 4


def main():
    diplay = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=7, gpio=1, i2c_address=0x3C)
    diplay.begin()
    diplay.clear()
    diplay.display()

    width = diplay.width
    height = diplay.height
    image = Image.new("1", (width, height))
    diplay_image = Image.new("1", (width, height))
    iamge_draw = ImageDraw.Draw(image)
    iamge_draw.rectangle((0, 0, width, height), outline=0, fill=0)

    x = 0
    while True:
        y = 0
        iamge_draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # 각 라인을 출력합니다.
        for text in KOREAN_TEXT.split("\n"):
            iamge_draw.text((0, y), text, font=KOREAN_FONT, fill=255)
            text_width, text_height = iamge_draw.textsize(text, font=KOREAN_FONT)
            y += text_height
        if x >= width:
            x = 0

        # 이미지를 스크롤하는 애니메이션을 보여줍니다.
        x += IMAGE_VEL
        image_part_1 = image.crop((x, 0, width, height))
        image_part_2 = image.crop((0, 0, x, height))
        diplay_image.paste(image_part_1, (0, 0))
        diplay_image.paste(image_part_2, (width - x, 0))

        diplay.image(diplay_image)
        diplay.display()
        time.sleep(1.0 / 4)


if __name__ == "__main__":
    main()
