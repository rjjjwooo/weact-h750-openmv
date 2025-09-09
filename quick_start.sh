#!/bin/bash
# WEACT H750 Custom OpenMV 빠른 시작 스크립트

echo "🚀 WEACT H750 Custom OpenMV 프로젝트 설정"
echo "========================================"

# 1. GitHub 리포지토리 URL 입력 받기
read -p "GitHub 리포지토리 URL을 입력하세요 (예: https://github.com/username/weact-h750-openmv.git): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ 리포지토리 URL이 필요합니다."
    exit 1
fi

# 2. Git 원격 리포지토리 설정
echo "📡 Git 원격 리포지토리 설정 중..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

# 3. 브랜치 설정
echo "🌿 메인 브랜치 설정 중..."
git branch -M main

# 4. 최종 커밋 및 푸시
echo "📤 GitHub에 업로드 중..."
git add .
git commit -m "Complete WEACT H750 Custom OpenMV project

✅ Ready-to-use custom board configuration
✅ 30m beacon detection capability  
✅ W5500 Ethernet networking
✅ RGB LED status indicators
✅ Hardware test utilities
✅ GitHub Actions CI/CD pipeline
✅ Complete documentation

Hardware: STM32H750VBT6 + OV7725 + W5500
Features: Beacon detection, Ethernet, USB, LEDs"

git push -u origin main

# 5. 성공 메시지
echo ""
echo "🎉 업로드 완료!"
echo ""
echo "다음 단계:"
echo "1. GitHub 리포지토리의 Actions 탭 확인"
echo "2. 자동 빌드 완료 대기 (약 5-10분)"
echo "3. Artifacts에서 펌웨어 다운로드"
echo "4. DFU로 보드에 업로드:"
echo "   dfu-util -a 0 -s 0x08000000:leave -D openmv.bin"
echo ""
echo "🔗 리포지토리 주소: $REPO_URL"
echo "📖 문서: README_WEACT_H750.md 참조"
