# OpenMV IDE를 통한 WEACT H750 사용 가이드

## 1. OpenMV IDE 다운로드 및 설치
1. https://openmv.io/pages/download 에서 최신 버전 다운로드
2. 설치 후 실행

## 2. 기존 보드로 초기 테스트
- OPENMV4와 유사한 H7 보드 선택
- 카메라 연결 확인
- 기본 예제 실행

## 3. 커스텀 보드 설정
1. IDE에서 Tools > Options > General > Board 설정
2. Custom Board 선택
3. STM32H750 설정 적용

## 4. 비콘 감지 코드 실행
beacon_detection_demo.py 파일을 OpenMV IDE에서 실행

## 5. 하드웨어 검증
- 각 핀 연결 상태 확인
- LED 동작 테스트
- 카메라 이미지 확인
- W5500 네트워크 연결 테스트
