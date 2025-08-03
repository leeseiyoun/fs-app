# 오픈다트 재무 데이터 시각화 분석 서비스

한국 기업의 재무 데이터를 검색하고 분석할 수 있는 웹 애플리케이션입니다.

## 주요 기능

### 1. 회사 검색
- corp.xml 파일을 데이터베이스로 변환하여 회사명으로 검색
- 실시간 검색 결과 표시
- 회사 코드, 주식 코드, 영문명 등 상세 정보 제공

### 2. 회사 상세 정보
- 선택한 회사의 상세 정보 표시
- 재무 분석, 성과 지표, 업종 비교 탭 제공
- 향후 오픈다트 API 연동 예정

## 설치 및 실행

### 1. 가상환경 생성 및 활성화
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행
```bash
python app.py
```

### 4. 웹 브라우저에서 접속
```
http://localhost:5000
```

## 프로젝트 구조

```
test/
├── app.py                 # Flask 메인 애플리케이션
├── corp.xml              # 기업 정보 XML 파일
├── requirements.txt       # Python 패키지 목록
├── README.md             # 프로젝트 설명서
├── templates/            # HTML 템플릿
│   ├── index.html        # 메인 페이지
│   └── company_detail.html # 회사 상세 페이지
└── corp_database.db      # SQLite 데이터베이스 (자동 생성)
```

## 기술 스택

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Data Source**: corp.xml (오픈다트 기업 정보)

## API 엔드포인트

- `GET /`: 메인 페이지
- `GET /search?q=<검색어>`: 회사 검색 API
- `GET /company/<corp_code>`: 회사 상세 정보 페이지
- `GET /stats`: 통계 정보 API

## 향후 개발 계획

1. **오픈다트 API 연동**
   - 재무제표 데이터 가져오기
   - 실시간 주가 정보 연동
   - 재무 비율 계산 및 시각화

2. **차트 및 시각화**
   - Chart.js 또는 D3.js를 활용한 차트 구현
   - 재무 지표 트렌드 분석
   - 업종 비교 분석

3. **추가 기능**
   - 사용자 인증 시스템
   - 즐겨찾기 기능
   - 데이터 내보내기 기능

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 