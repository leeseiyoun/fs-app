# 오픈다트 재무 데이터 분석 서비스 배포 가이드

## 🚀 배포 옵션

### 1. Render (추천 - 무료)

#### 단계별 배포 방법:

1. **GitHub에 코드 업로드**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/opendart-financial-analysis.git
   git push -u origin main
   ```

2. **Render 계정 생성**
   - [Render.com](https://render.com)에서 계정 생성
   - GitHub 계정 연결

3. **새 Web Service 생성**
   - "New +" → "Web Service" 클릭
   - GitHub 저장소 연결
   - 다음 설정으로 구성:
     - **Name**: opendart-financial-analysis
     - **Environment**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`

4. **환경 변수 설정**
   - Environment Variables 섹션에서 다음 변수 추가:
     ```
     OPENDART_API_KEY = c4b398c31e803ac7b43b1b4878366911ba84a133
     GEMINI_API_KEY = AIzaSyAl-YCAkml-c8nYW-7RbbqJTI_lOQWIMUk
     ```

5. **배포 완료**
   - "Create Web Service" 클릭
   - 배포 완료 후 제공되는 URL로 접속

### 2. Heroku (무료 티어 종료됨)

#### 배포 방법:

1. **Heroku CLI 설치**
   ```bash
   # Windows
   https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Heroku 앱 생성**
   ```bash
   heroku login
   heroku create opendart-financial-analysis
   ```

3. **환경 변수 설정**
   ```bash
   heroku config:set OPENDART_API_KEY="c4b398c31e803ac7b43b1b4878366911ba84a133"
   heroku config:set GEMINI_API_KEY="AIzaSyAl-YCAkml-c8nYW-7RbbqJTI_lOQWIMUk"
   ```

4. **배포**
   ```bash
   git push heroku main
   ```

### 3. Railway (무료)

#### 배포 방법:

1. **Railway 계정 생성**
   - [Railway.app](https://railway.app)에서 계정 생성
   - GitHub 계정 연결

2. **새 프로젝트 생성**
   - "New Project" → "Deploy from GitHub repo"
   - 저장소 선택

3. **환경 변수 설정**
   - Variables 탭에서 환경 변수 추가:
     ```
     OPENDART_API_KEY = c4b398c31e803ac7b43b1b4878366911ba84a133
     GEMINI_API_KEY = AIzaSyAl-YCAkml-c8nYW-7RbbqJTI_lOQWIMUk
     ```

4. **배포 완료**
   - 자동으로 배포되며 제공되는 URL로 접속

## 📁 배포 파일 구조

```
opendart-financial-analysis/
├── app.py                 # 메인 애플리케이션
├── requirements.txt       # Python 패키지 목록
├── render.yaml           # Render 배포 설정
├── Procfile             # Heroku 배포 설정
├── runtime.txt          # Python 버전
├── corp.xml            # 기업 정보 데이터
├── templates/           # HTML 템플릿
│   ├── index.html
│   └── company_detail.html
└── README.md           # 프로젝트 설명서
```

## 🔧 환경 변수

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `OPENDART_API_KEY` | 오픈다트 API 키 | c4b398c31e803ac7b43b1b4878366911ba84a133 |
| `GEMINI_API_KEY` | Gemini AI API 키 | AIzaSyAl-YCAkml-c8nYW-7RbbqJTI_lOQWIMUk |
| `PORT` | 서버 포트 | 5000 |

## 🌐 배포 후 확인사항

1. **메인 페이지 접속**: `https://your-app-name.onrender.com`
2. **회사 검색 테스트**: "삼성전자" 검색
3. **재무 데이터 확인**: 회사 선택 후 재무 분석 탭
4. **AI 분석 테스트**: AI 분석 탭 클릭

## 🐛 문제 해결

### 일반적인 문제:

1. **모듈 설치 오류**
   - `requirements.txt`에 모든 패키지가 포함되어 있는지 확인
   - Python 버전이 3.11 이상인지 확인

2. **API 키 오류**
   - 환경 변수가 올바르게 설정되었는지 확인
   - API 키가 유효한지 확인

3. **데이터베이스 오류**
   - `corp.xml` 파일이 프로젝트에 포함되어 있는지 확인
   - 배포 시 데이터베이스가 자동으로 초기화됨

## 📞 지원

배포 중 문제가 발생하면:
1. 로그 확인 (Render/Railway/Heroku 대시보드)
2. 환경 변수 설정 확인
3. API 키 유효성 확인

## 🎯 추천 배포 플랫폼

**Render**를 추천합니다:
- ✅ 무료 플랜 제공
- ✅ 쉬운 배포 과정
- ✅ 자동 HTTPS
- ✅ GitHub 연동
- ✅ 환경 변수 관리
- ✅ 로그 확인 가능 