#! /usr/bin/python3
"""시스템 정보 출력 예제
Author: SungWan Jin(jin.seungwan@hanulsoft.co.kr)

프롬프트 명령을 사용하여 획득한 시스템 정보를 출력합니다.

Portions Copyright (c) 2017 Adafruit Industries
Portions Copyright (c) NVIDIA 2019
Portions copyright (c) JetsonHacks 2019
CopyRight(C) 2020 HanulSoft Inc.
MIT License
"""
import re
import time
import subprocess
import packaging.version

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import __version__ as PIL_VERSION


def get_network_interface_state(interface) -> str:
    """네트워크 인터페이스의 상태를 반환합니다.

    반환 결과는 'up' 또는 'down'입니다.
    """
    return subprocess.check_output("cat /sys/class/net/%s/operstate" % interface, shell=True).decode("ascii")[:-1]


def get_ip_address(interface) -> str:
    """네트워크 인터페이스의 IP 주소를 반환합니다."""
    if get_network_interface_state(interface) == "down":
        # 인터페이스가 비활성화 상태이면 IP 주소를 반환하지 않습니다.
        return None
    cmd = (
        "ifconfig %s | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*'" % interface
        + " | grep -Eo '([0-9]*\.){3}[0-9]*'"
        + " | grep -v '127.0.0.1'"
    )
    return subprocess.check_output(cmd, shell=True).decode("ascii")[:-1]


def get_cpu_usage() -> float:
    """CPU 사용률을 반환합니다.

    mpstat 명령을 사용하여 CPU 사용률을 획득합니다.
    명령 후 1초 대기하고, 1초 동안의 CPU 사용률을 반환합니다.
    """
    result = subprocess.check_output(["mpstat", "1", "1"], universal_newlines=True)
    match = re.search(r"(\d+\.\d+)$", result)
    if match:
        usage = 100 - float(match.group(1))
        return usage / 100.0
    else:
        raise 0.0


def get_gpu_usage() -> float:
    """GPU 사용률을 반환합니다."""
    gpu = 0.0
    with open("/sys/devices/gpu.0/load", encoding="utf-8") as gpu_file:
        gpu_text = gpu_file.readline()
        gpu = int(gpu_text) / 10
    return float(gpu)


def get_mem_usage() -> float:
    """메모리 사용률을 반환합니다."""
    # 이 명령은 메모리 사용량 사용량과 전체 메모리를 MB 단위로 반환합니다.
    cmd = "free -m | awk 'NR==2{printf \"%s|%s\", $3,$2 }'"
    mem = subprocess.check_output(cmd, shell=True).decode("ascii")
    usage, total = map(float, mem.split("|"))
    return usage / total


def get_disk_usage() -> float:
    """디스크 사용률을 반환합니다."""
    # 이 명령은 디스크 사용량 사용량과 전체 메모리를 GB 단위로 반환합니다.
    cmd = 'df -h | awk \'$NF=="/"{printf "%d|%d",$3,$2}\''
    usage, total = map(float, subprocess.check_output(cmd, shell=True).decode("ascii").split("|"))
    return usage / total


def draw_system_stats(draw: ImageDraw, width: int, height: int, font: ImageFont) -> None:
    """시스템 정보를 ImageDraw 객체에 출력합니다."""
    x, y = 0, -2
    margin = -3
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # 네트워크 정보
    eth0_ip = f"Eth0: {get_ip_address('eth0')}"
    draw.text((x, y), eth0_ip, font=font, fill=1)
    if packaging.version.parse(PIL_VERSION) < packaging.version.parse("10.0.0"):
        y += draw.textsize(eth0_ip, font=font)[1] + margin
    else:
        y = font.getbbox(eth0_ip)[3] + margin

    # CPU 사용률
    cpu_usage = f"CPU: {get_cpu_usage() * 100:3.1f}%"
    draw.text((x, y), cpu_usage, font=font, fill=1)
    if packaging.version.parse(PIL_VERSION) < packaging.version.parse("10.0.0"):
        px, py = draw.textsize(cpu_usage, font=font)
    else:
        px, py = font.getbbox(cpu_usage)[2:]
    px += 5
    usage_width = int((width - px) * get_cpu_usage()) + px
    draw.rectangle((px, y + 2, usage_width, y + py - 2), outline=0, fill=1)
    y += py + margin

    # GPU 사용률
    gpu_usage = f"GPU: {get_gpu_usage() * 100:3.1f}%"
    if packaging.version.parse(PIL_VERSION) < packaging.version.parse("10.0.0"):
        px, py = draw.textsize(gpu_usage, font=font)
    else:
        y += 1
        px, py = font.getbbox(gpu_usage)[2:]
    draw.text((x, y), gpu_usage, font=font, fill=1)
    px += 5
    usage_width = int((width - px) * get_gpu_usage()) + px
    draw.rectangle((px, y + 2, usage_width, y + py - 2), outline=0, fill=1)
    y += py + margin

    # 메모리 사용률
    mem_usage = f"Mem: {get_mem_usage() * 100:3.1f}%"
    if packaging.version.parse(PIL_VERSION) < packaging.version.parse("10.0.0"):
        px, py = draw.textsize(mem_usage, font=font)
    else:
        y += 1
        px, py = font.getbbox(mem_usage)[2:]
    draw.text((x, y), mem_usage, font=font, fill=1)
    px += 5
    usage_width = int((width - px) * get_mem_usage()) + px
    draw.rectangle((px, y + 2, usage_width, y + py - 2), outline=0, fill=1)
    y += py + margin


def main() -> None:
    """메인 함수"""
    display = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=7, gpio=1, i2c_address=0x3C)
    display.begin()
    display.clear()
    display.display()
    width, height = display.width, display.height
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    if packaging.version.parse(PIL_VERSION) < packaging.version.parse("10.0.0"):
        font = ImageFont.load_default()
    else:
        font = ImageFont.load_default(9)

    while True:
        draw_system_stats(draw, width, height, font)
        display.image(image)
        display.display()
        time.sleep(1.0 / 4)


if __name__ == "__main__":
    main()
