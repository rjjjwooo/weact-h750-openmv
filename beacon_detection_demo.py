# WEACT H750 Custom Board - OV7725 + W5500 + LED Beacon Detection
# STM32H750VBT6 기반 비콘 감지 시스템

import sensor, image, time, network
from pyb import LED, Pin

# LED 초기화 (비콘 감지 상태 표시용)
led_red = LED(1)    # 감지 실패
led_green = LED(2)  # 감지 성공  
led_blue = LED(3)   # 네트워크 상태

# 카메라 센서 초기화 (OV7725)
sensor.reset()                      # 센서 리셋
sensor.set_pixformat(sensor.RGB565) # RGB565 포맷 (색상 비콘 감지에 적합)
sensor.set_framesize(sensor.QVGA)   # 320x240 해상도 (비콘 감지에 충분)
sensor.skip_frames(time=2000)       # 센서 안정화 대기
sensor.set_auto_gain(False)         # 자동 게인 비활성화 (일관된 색상 감지)
sensor.set_auto_whitebal(False)     # 자동 화이트밸런스 비활성화

# W5500 이더넷 초기화
def init_w5500():
    try:
        # W5500 SPI 설정 (SPI3 사용)
        nic = network.WIZNET5K(spi=3, cs=Pin('A15'), rst=Pin('E1'))
        nic.active(True)
        
        # DHCP로 IP 자동 할당
        nic.ifconfig('dhcp')
        print("W5500 Ethernet 초기화 성공")
        print("IP 주소:", nic.ifconfig()[0])
        led_blue.on()  # 네트워크 연결 성공
        return nic
    except Exception as e:
        print("W5500 초기화 실패:", e)
        led_blue.off()
        return None

# 비콘 색상 임계값 (적색 비콘 기준)
# 30m 거리에서도 감지 가능하도록 임계값 조정
red_threshold = (30, 100, 15, 127, 15, 127)  # LAB 색공간
green_threshold = (30, 100, -64, -8, -32, 32)
blue_threshold = (30, 100, 0, 30, -80, -20)

def find_beacons():
    """비콘 감지 및 위치 반환"""
    img = sensor.snapshot()
    
    # 적색 비콘 찾기
    red_blobs = img.find_blobs([red_threshold], pixels_threshold=20, area_threshold=20, merge=True)
    
    # 감지된 비콘 정보
    beacons = []
    
    for blob in red_blobs:
        # 비콘이 충분히 크고 원형에 가까운지 확인
        if blob.pixels() > 30 and blob.compactness() > 0.5:
            # 비콘 중심 좌표
            cx = blob.cx()
            cy = blob.cy()
            
            # 거리 추정 (픽셀 크기 기반)
            estimated_distance = 10000 / blob.pixels()  # 간단한 거리 추정
            
            beacons.append({
                'x': cx,
                'y': cy, 
                'distance': estimated_distance,
                'size': blob.pixels()
            })
            
            # 비콘에 사각형 그리기
            img.draw_rectangle(blob.rect(), color=(255, 0, 0))
            img.draw_cross(cx, cy, color=(255, 0, 0))
            
            print(f"비콘 감지: 위치({cx}, {cy}), 거리: {estimated_distance:.1f}m")
    
    return img, beacons

def main():
    """메인 실행 함수"""
    print("=== WEACT H750 비콘 감지 시스템 시작 ===")
    
    # W5500 이더넷 초기화
    network_interface = init_w5500()
    
    # LED 초기 상태
    led_red.off()
    led_green.off()
    
    frame_count = 0
    
    while True:
        try:
            # 비콘 감지
            img, beacons = find_beacons()
            
            if beacons:
                led_green.on()   # 비콘 감지 성공
                led_red.off()
                
                # 가장 가까운 비콘 선택
                closest_beacon = min(beacons, key=lambda b: b['distance'])
                print(f"가장 가까운 비콘: {closest_beacon['distance']:.1f}m")
                
                # 네트워크로 데이터 전송 (옵션)
                if network_interface:
                    # 여기에 비콘 정보를 서버로 전송하는 코드 추가 가능
                    pass
                    
            else:
                led_red.on()     # 비콘 감지 실패
                led_green.off()
            
            frame_count += 1
            if frame_count % 30 == 0:  # 30프레임마다 상태 출력
                print(f"프레임: {frame_count}, 감지된 비콘: {len(beacons)}개")
            
            time.sleep_ms(50)  # 20 FPS
            
        except KeyboardInterrupt:
            print("프로그램 종료")
            break
        except Exception as e:
            print(f"오류 발생: {e}")
            led_red.on()
            time.sleep_ms(100)

if __name__ == "__main__":
    main()
