# 🚀 WEACT H750 Custom OpenMV - GitHub 업로드 가이드

## 📋 완성된 프로젝트 업로드 방법

### 1. GitHub 새 리포지토리 생성
1. https://github.com/new 방문
2. Repository name: `weact-h750-openmv`
3. Description: `STM32H750VBT6 + OV7725 + W5500 custom OpenMV board`
4. Public으로 설정
5. "Create repository" 클릭

### 2. 로컬 리포지토리 연결
```bash
# 현재 디렉토리에서 실행
git remote add origin https://github.com/[YOUR_USERNAME]/weact-h750-openmv.git
git branch -M main
git push -u origin main
```

### 3. 자동 빌드 확인
1. GitHub 리포지토리 → Actions 탭
2. "Build WEACT H750 Custom OpenMV Firmware" 워크플로우 실행 확인
3. 빌드 완료 후 Artifacts에서 펌웨어 다운로드

## 🎯 완성된 커스텀 보드 기능

### ✅ 하드웨어 지원
- **MCU**: STM32H750VBT6 (400MHz, 128KB Flash, 1MB RAM)  
- **카메라**: OV7725 (VGA, RGB565, 30m 비콘 감지)
- **네트워크**: W5500 (SPI3 이더넷)
- **LED**: RGB 3색 상태 표시
- **USB**: High Speed ULPI
- **클럭**: 24MHz HSE

### ✅ 소프트웨어 기능
- **비콘 감지**: 30m 거리 적색 비콘 감지
- **네트워크**: 이더넷 연결 및 데이터 전송
- **상태 표시**: LED를 통한 실시간 상태 확인
- **USB 연결**: OpenMV IDE와 직접 연결
- **하드웨어 테스트**: 자동 하드웨어 검증

### ✅ 개발 도구
- **GitHub Actions**: 자동 펌웨어 빌드
- **OpenMV IDE**: 즉시 사용 가능한 IDE 연동
- **하드웨어 테스트**: 핀 연결 자동 검증
- **완전한 문서**: 설치부터 사용법까지

## 📁 프로젝트 구조

```
weact-h750-openmv/
├── .github/workflows/build.yml           # CI/CD 파이프라인
├── src/
│   ├── omv/boards/WEACT_H750_CUSTOM/     # OpenMV 보드 설정
│   └── micropython/ports/stm32/boards/WEACT_H750_CUSTOM/  # MicroPython 설정
├── beacon_detection_demo.py              # 비콘 감지 데모
├── hardware_test.py                      # 하드웨어 테스트
├── README_WEACT_H750.md                  # 완전한 사용 가이드
└── OpenMV_IDE_Guide.md                   # IDE 사용법
```

## 🔥 즉시 사용 가능!

이 프로젝트는 **완전히 준비된 상태**입니다:

1. **GitHub에 푸시** → 자동으로 펌웨어 빌드됨
2. **펌웨어 다운로드** → DFU로 업로드
3. **OpenMV IDE 연결** → 즉시 코딩 시작
4. **비콘 감지 테스트** → 30m 거리 감지 확인

**🎉 당신의 STM32H750VBT6 + OV7725 + W5500 커스텀 보드가 완전한 OpenMV 시스템으로 변신합니다!**
