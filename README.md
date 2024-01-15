# LED Display Control Sample Code

![EmVision LCD](assets\EmVision_LCD.png)

## 소개

이 샘플 코드는 하늘소프트의 EmVision에 탑재되어 있는 LED 디스플레이를 제어하는 예시 코드를 제공합니다.

## 설치 방법

설치와 실행을 위해서는 EmVision에서 직접 작업하거나 원격 접속으로 터미널을 실행해야 합니다.

1. 이 저장소를 복제합니다:

   ```bash
   git clone https://github.com/hanulsoft/EmVision-PiOLED
   ```

2. I2C 접근 권한을 획득하고 인터페이스 드라이버를 설치합니다:

   ```bash
   ./installEmVisionOLED.sh
   ```

## 의존성

- Python 3.6 이상
- [Adafruit-SSD1306](https://github.com/adafruit/Adafruit_Python_SSD1306/)
- [Pillow](https://python-pillow.org/)

### 예제 의존성

- [Jetson Stats](https://github.com/rbonghi/jetson_stats)

## 사용 방법

> **실행 시 주의사항**: 하늘소프트에서는 자동 실행 서비스로 현재 시스템 모니터링 정보를 LED 패널에 출력하고 있습니다. 이 기능을 수행하는 서비스를 정지한 후 예제를 실행해야 올바른 출력 결과를 얻을 수 있습니다.
> ```bash
> # 서비스 중단
> sudo systemctl stop pioled_stats.service
> # 서비스 시작
> sudo systemctl start pioled_stats.service
> ```

```bash
python example/{예제 파일 이름}.py
```

EmVision의 터미널에서 위와 같은 명령으로 예제를 실행할 수 있습니다.

## 예제 목록

- `display_korean.py`: 한글을 출력하고 스크롤 애니메이션을 수행합니다.
- `display_stats.py`: 현재 시스템의 모니터링 정보를 출력합니다.

첫 시작에는 가장 단순한 코드를 가진 `display_korean.py`을 추천합니다.


## 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

