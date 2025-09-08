# WEACT H750 하드웨어 테스트 스크립트
# 기존 OpenMV 보드에서 핀 매핑만 변경해서 사용

import time
from pyb import Pin, LED, SPI, I2C

print("=== WEACT H750 Custom 하드웨어 테스트 ===")

# LED 테스트 (실제 핀 번호로 수정 필요)
def test_leds():
    print("LED 테스트 시작...")
    try:
        # 실제 핀으로 변경 필요 (예: PA1, PA8, PE2)
        led_pins = ['A1', 'A8', 'E2']  
        leds = []
        
        for pin_name in led_pins:
            try:
                led = Pin(pin_name, Pin.OUT)
                leds.append(led)
                print(f"LED {pin_name}: OK")
            except:
                print(f"LED {pin_name}: 연결 오류")
        
        # LED 순차 점등 테스트
        for i in range(3):
            for led in leds:
                led.high()
                time.sleep(0.2)
                led.low()
                time.sleep(0.1)
        
        print("LED 테스트 완료")
        return True
    except Exception as e:
        print(f"LED 테스트 실패: {e}")
        return False

# I2C 테스트 (카메라 센서 감지)
def test_i2c_camera():
    print("I2C 카메라 테스트 시작...")
    try:
        # I2C2: SCL=H4, SDA=H5 (OV7725용)
        i2c = I2C(2, I2C.CONTROLLER, baudrate=100000)
        
        # I2C 스캔
        devices = i2c.scan()
        print(f"I2C 장치 발견: {[hex(addr) for addr in devices]}")
        
        # OV7725 주소 확인 (일반적으로 0x21 또는 0x42)
        ov7725_addrs = [0x21, 0x42]
        for addr in ov7725_addrs:
            if addr in devices:
                print(f"OV7725 카메라 발견: {hex(addr)}")
                return True
        
        print("OV7725 카메라를 찾을 수 없음")
        return False
        
    except Exception as e:
        print(f"I2C 테스트 실패: {e}")
        return False

# SPI 테스트 (W5500 연결 확인)
def test_spi_w5500():
    print("SPI W5500 테스트 시작...")
    try:
        # SPI3: SCK=C10, MISO=C11, MOSI=C12, CS=A15
        spi = SPI(3, SPI.CONTROLLER, baudrate=1000000, 
                 polarity=0, phase=0, bits=8)
        
        cs_pin = Pin('A15', Pin.OUT)
        rst_pin = Pin('E1', Pin.OUT)
        
        # W5500 리셋
        rst_pin.low()
        time.sleep(0.1)
        rst_pin.high()
        time.sleep(0.1)
        
        # Version Register 읽기 (0x0039)
        cs_pin.low()
        spi.send(bytearray([0x00, 0x39, 0x00]))  # 주소 + 제어
        version = spi.recv(1)[0]
        cs_pin.high()
        
        if version == 0x04:  # W5500 버전
            print(f"W5500 감지됨: 버전 {hex(version)}")
            return True
        else:
            print(f"W5500 감지 실패: 버전 {hex(version)}")
            return False
            
    except Exception as e:
        print(f"SPI 테스트 실패: {e}")
        return False

# USB 연결 테스트
def test_usb_connection():
    print("USB 연결 테스트...")
    try:
        import pyb
        
        # USB VCP 활성화 여부 확인
        if pyb.USB_VCP().connected():
            print("USB VCP 연결됨")
            return True
        else:
            print("USB VCP 연결 안됨")
            return False
            
    except Exception as e:
        print(f"USB 테스트 실패: {e}")
        return False

# 메인 테스트 함수
def main():
    print("하드웨어 테스트를 시작합니다...")
    print("-" * 40)
    
    results = {}
    results['LED'] = test_leds()
    results['Camera_I2C'] = test_i2c_camera()
    results['W5500_SPI'] = test_spi_w5500()
    results['USB'] = test_usb_connection()
    
    print("-" * 40)
    print("테스트 결과 요약:")
    
    for test_name, result in results.items():
        status = "✅ 통과" if result else "❌ 실패"
        print(f"{test_name:15}: {status}")
    
    total_pass = sum(results.values())
    print(f"\n전체: {total_pass}/{len(results)} 테스트 통과")
    
    if total_pass == len(results):
        print("🎉 모든 하드웨어 테스트 통과!")
    else:
        print("⚠️  일부 하드웨어 확인 필요")

if __name__ == "__main__":
    main()
