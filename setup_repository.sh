#!/bin/bash
# GitHub 리포지토리 연결 스크립트

echo "🔧 WEACT H750 OpenMV 리포지토리 설정"
echo "====================================="

# 사용자로부터 리포지토리 URL 입력받기
echo "GitHub에서 새 리포지토리를 생성한 후, 아래 명령어를 실행하세요:"
echo ""
echo "1. GitHub 리포지토리 URL을 복사하세요"
echo "2. 아래 명령어의 URL 부분을 바꾸고 실행하세요:"
echo ""
echo "git remote add origin https://github.com/YOUR_USERNAME/weact-h750-openmv.git"
echo "git push -u origin main"
echo ""
echo "예시:"
echo "git remote add origin https://github.com/johndoe/weact-h750-openmv.git"
echo "git push -u origin main"
echo ""
echo "🎉 업로드 완료 후 GitHub Actions에서 자동 빌드가 시작됩니다!"
