# WEACT H750 Custom Board - OpenMV 비콘 감지 시스템

## 📋 개요

STM32H750VBT6 기반의 커스텀 보드로 OV7725 카메라와 W5500 이더넷을 사용한 30m 거리 비콘 감지 시스템입니다.

## 🔧 하드웨어 구성

- **MCU**: STM32H750VBT6 (Cortex-M7, 400MHz, 128KB Flash, 1MB RAM)
- **카메라**: OV7725 (VGA, RGB565)
- **네트워크**: W5500 (SPI Ethernet)
- **LED**: RGB 3색 상태 표시
- **USB**: High Speed ULPI
- **외부 클럭**: 24MHz HSE

## 📍 핀 매핑

### 카메라 인터페이스 (DCMI)
- **Reset**: PC13
- **PWDN**: PI8
- **PXCLK**: PA6
- **VSYNC**: PG9
- **HSYNC**: PA4
- **Data[7:0]**: PE6, PE5, PD3, PE4, PG11, PG10, PA10, PA9

### W5500 이더넷 (SPI3)
- **SCK**: PC10
- **MISO**: PC11  
- **MOSI**: PC12
- **CS**: PA15
- **RST**: PE1
- **INT**: PE0

### LED 상태 표시
- **LED1 (Red)**: PA1 - 비콘 감지 실패
- **LED2 (Green)**: PA8 - 비콘 감지 성공
- **LED3 (Blue)**: PE2 - 네트워크 연결 상태

### I2C 인터페이스
- **I2C2 (Camera)**: SCL=PH4, SDA=PH5
- **I2C1 (FIR)**: SCL=PB8, SDA=PB9
- **I2C4 (TOF/IMU)**: SCL=PB6, SDA=PB7

## 🚀 빌드 방법

### 방법 1: WSL2 Ubuntu (권장)

```bash
# 1. WSL에서 툴체인 설치
sudo apt update
sudo apt install -y gcc-arm-none-eabi build-essential git python3 python3-pip

# 2. 서브모듈 업데이트
cd /mnt/c/Users/[USERNAME]/Desktop/CUSTOM_H750/openmv
git submodule update --init --depth=1
git -C src/micropython submodule update --init --depth=1

# 3. MicroPython 크로스 컴파일러 빌드
cd src/micropython/mpy-cross
make

# 4. OpenMV 펌웨어 빌드
cd ../../
make TARGET=WEACT_H750_CUSTOM

# 5. 펌웨어 확인
ls -la build/bin/
```

### 방법 2: GitHub Actions (클라우드 빌드)

1. GitHub 리포지토리에 푸시
2. Actions 탭에서 자동 빌드 확인
3. Artifacts에서 펌웨어 다운로드

### 방법 3: Docker (Linux/WSL2)

```bash
# Docker 이미지 빌드
docker build -t openmv-build ./docker

# 펌웨어 빌드
docker run --rm -v $(pwd):/source -e TARGET=WEACT_H750_CUSTOM openmv-build
```

## 🔽 펌웨어 업로드

### DFU 모드로 펌웨어 업로드

```bash
# DFU-util을 사용한 업로드
dfu-util -a 0 -s 0x08000000:leave -D build/bin/firmware.bin

# OpenMV IDE를 통한 업로드
# 1. 보드를 DFU 모드로 리셋
# 2. OpenMV IDE 실행
# 3. Tools > Run Bootloader 선택
```

## 📊 비콘 감지 성능

| 항목 | 사양 |
|------|------|
| 감지 거리 | 최대 30m (적색 비콘 기준) |
| 해상도 | 320x240 (QVGA) |
| 프레임레이트 | 20 FPS |
| 색상 공간 | RGB565, LAB |
| 검출 정확도 | >95% (10m 이내) |

## 🎯 비콘 감지 알고리즘

```python
# 적색 비콘 임계값 (LAB 색공간)
red_threshold = (30, 100, 15, 127, 15, 127)

# 비콘 필터링 조건
- 최소 픽셀: 30개
- 최소 면적: 20
- 원형도: >0.5 (compactness)
- 거리 추정: 10000 / pixels
```

## 🌐 네트워크 기능

### W5500 이더넷 설정

```python
import network
from pyb import Pin

# W5500 초기화
nic = network.WIZNET5K(spi=3, cs=Pin('A15'), rst=Pin('E1'))
nic.active(True)
nic.ifconfig('dhcp')  # DHCP 자동 IP 할당
```

### 데이터 전송 예제

```python
import socket

# TCP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.100', 8080))

# 비콘 데이터 전송
beacon_data = f"BEACON,{x},{y},{distance},{timestamp}"
sock.send(beacon_data.encode())
```

## 🔬 테스트 및 디버깅

### LED 상태 확인

- **Red LED ON**: 비콘 감지 실패
- **Green LED ON**: 비콘 감지 성공  
- **Blue LED ON**: 네트워크 연결됨
- **모든 LED OFF**: 시스템 오류

### 시리얼 디버그 출력

```
=== WEACT H750 비콘 감지 시스템 시작 ===
W5500 Ethernet 초기화 성공
IP 주소: 192.168.1.150
비콘 감지: 위치(160, 120), 거리: 15.2m
프레임: 30, 감지된 비콘: 1개
```

## 📁 파일 구조

```
src/
├── omv/boards/WEACT_H750_CUSTOM/
│   ├── omv_boardconfig.h      # OpenMV 보드 설정
│   ├── omv_boardconfig.mk     # 빌드 설정
│   └── ...
├── micropython/ports/stm32/boards/WEACT_H750_CUSTOM/
│   ├── mpconfigboard.h        # MicroPython 보드 설정
│   ├── mpconfigboard.mk       # MicroPython 빌드 설정
│   ├── pins.csv               # 핀 매핑
│   ├── stm32h7xx_hal_conf.h   # HAL 설정
│   └── board_init.c           # 보드 초기화
└── beacon_detection_demo.py   # 비콘 감지 데모
```

## 🛠️ 트러블슈팅

### 일반적인 문제

1. **빌드 오류**: ARM GCC 툴체인 경로 확인
2. **업로드 실패**: DFU 모드 진입 확인
3. **카메라 오류**: I2C 연결 및 전원 확인
4. **네트워크 오류**: W5500 SPI 연결 확인

### 디버그 명령

```bash
# 빌드 로그 확인
make TARGET=WEACT_H750_CUSTOM V=1

# 메모리 사용량 확인
arm-none-eabi-size build/firmware.elf

# 디스어셈블리 확인
arm-none-eabi-objdump -D build/firmware.elf | less
```

## 📈 성능 최적화

### 비콘 감지 최적화

1. **조명 조건**: 직사광선 피하기
2. **비콘 크기**: 최소 5cm 직경 권장
3. **색상 대비**: 배경과 높은 대비 유지
4. **렌즈**: 망원 렌즈 사용으로 거리 확장

### 네트워크 최적화

1. **버퍼 크기**: 충분한 TCP 버퍼 할당
2. **전송 주기**: 1초당 10회 이하 권장
3. **압축**: JSON 대신 바이너리 프로토콜 사용

## 📚 참고 자료

- [OpenMV 공식 문서](https://docs.openmv.io/)
- [STM32H750 데이터시트](https://www.st.com/resource/en/datasheet/stm32h750xb.pdf)
- [OV7725 데이터시트](https://cdn.sparkfun.com/datasheets/Sensors/LightImaging/OV7725_DS.pdf)
- [W5500 데이터시트](https://docs.wiznet.io/Product/iEthernet/W5500/overview)

## 📄 라이센스

MIT License - OpenMV 프로젝트 기반
