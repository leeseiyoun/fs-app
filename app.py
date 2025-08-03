from flask import Flask, render_template, request, jsonify
import xml.etree.ElementTree as ET
import sqlite3
import os
import requests
import json
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)

# 오픈다트 API 설정
OPENDART_API_KEY = os.environ.get("OPENDART_API_KEY", "c4b398c31e803ac7b43b1b4878366911ba84a133")
OPENDART_BASE_URL = "https://opendart.fss.or.kr/api"

# Gemini API 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAl-YCAkml-c8nYW-7RbbqJTI_lOQWIMUk")
genai.configure(api_key=GEMINI_API_KEY)

# 데이터베이스 초기화
def init_database():
    conn = sqlite3.connect('corp_database.db')
    cursor = conn.cursor()
    
    # 회사 정보 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS corporations (
            corp_code TEXT PRIMARY KEY,
            corp_name TEXT NOT NULL,
            corp_eng_name TEXT,
            stock_code TEXT,
            modify_date TEXT
        )
    ''')
    
    # XML 파일에서 데이터 로드
    if os.path.exists('corp.xml'):
        tree = ET.parse('corp.xml')
        root = tree.getroot()
        
        # 기존 데이터 삭제
        cursor.execute('DELETE FROM corporations')
        
        # XML 데이터를 데이터베이스에 삽입
        for corp in root.findall('list'):
            corp_code = corp.find('corp_code').text if corp.find('corp_code') is not None else ''
            corp_name = corp.find('corp_name').text if corp.find('corp_name') is not None else ''
            corp_eng_name = corp.find('corp_eng_name').text if corp.find('corp_eng_name') is not None else ''
            stock_code = corp.find('stock_code').text if corp.find('stock_code') is not None else ''
            modify_date = corp.find('modify_date').text if corp.find('modify_date') is not None else ''
            
            cursor.execute('''
                INSERT OR REPLACE INTO corporations 
                (corp_code, corp_name, corp_eng_name, stock_code, modify_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (corp_code, corp_name, corp_eng_name, stock_code, modify_date))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    
    conn = sqlite3.connect('corp_database.db')
    cursor = conn.cursor()
    
    # 회사명으로 검색 (부분 일치)
    cursor.execute('''
        SELECT corp_code, corp_name, corp_eng_name, stock_code, modify_date
        FROM corporations 
        WHERE corp_name LIKE ? OR corp_eng_name LIKE ?
        ORDER BY corp_name
        LIMIT 20
    ''', (f'%{query}%', f'%{query}%'))
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'corp_code': row[0],
            'corp_name': row[1],
            'corp_eng_name': row[2],
            'stock_code': row[3],
            'modify_date': row[4]
        })
    
    conn.close()
    return jsonify(results)

@app.route('/company/<corp_code>')
def company_detail(corp_code):
    conn = sqlite3.connect('corp_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT corp_code, corp_name, corp_eng_name, stock_code, modify_date
        FROM corporations 
        WHERE corp_code = ?
    ''', (corp_code,))
    
    company = cursor.fetchone()
    conn.close()
    
    if company:
        company_data = {
            'corp_code': company[0],
            'corp_name': company[1],
            'corp_eng_name': company[2],
            'stock_code': company[3],
            'modify_date': company[4]
        }
        return render_template('company_detail.html', company=company_data)
    else:
        return "회사를 찾을 수 없습니다.", 404

@app.route('/stats')
def stats():
    conn = sqlite3.connect('corp_database.db')
    cursor = conn.cursor()
    
    # 전체 회사 수
    cursor.execute('SELECT COUNT(*) FROM corporations')
    total_companies = cursor.fetchone()[0]
    
    # 오늘 날짜의 검색 수 (간단한 예시)
    today_searches = 0  # 실제로는 검색 로그 테이블에서 계산
    
    # 데이터 업데이트 날짜 (가장 최근 수정일)
    cursor.execute('SELECT MAX(modify_date) FROM corporations')
    latest_date = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_companies': total_companies,
        'today_searches': today_searches,
        'data_updated': latest_date
    })

def get_financial_data(corp_code, year="2023", report_code="11011"):
    """오픈다트 API에서 재무 데이터 가져오기"""
    try:
        url = f"{OPENDART_BASE_URL}/fnlttSinglAcnt.json"
        params = {
            'crtfc_key': OPENDART_API_KEY,
            'corp_code': corp_code,
            'bsns_year': year,
            'reprt_code': report_code
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') == '000':
            return data.get('list', [])
        else:
            print(f"API 오류: {data.get('message', '알 수 없는 오류')}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"API 요청 오류: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        return []

def format_amount(amount_str):
    """금액 문자열을 숫자로 변환"""
    if not amount_str or amount_str == '':
        return 0
    try:
        # 쉼표 제거 후 숫자로 변환
        return int(amount_str.replace(',', ''))
    except ValueError:
        return 0

@app.route('/api/financial/<corp_code>')
def api_financial_data(corp_code):
    """재무 데이터 API 엔드포인트"""
    year = request.args.get('year', '2023')
    report_code = request.args.get('report_code', '11011')
    
    financial_data = get_financial_data(corp_code, year, report_code)
    
    if not financial_data:
        return jsonify({'error': '재무 데이터를 가져올 수 없습니다.'}), 404
    
    # 주요 재무 지표 추출
    key_metrics = {}
    
    for item in financial_data:
        account_name = item.get('account_nm', '')
        fs_div = item.get('fs_div', '')  # OFS: 개별, CFS: 연결
        
        # 연결재무제표 기준으로 주요 지표 추출
        if fs_div == 'CFS':
            if '자산총계' in account_name:
                key_metrics['total_assets'] = format_amount(item.get('thstrm_amount', '0'))
            elif '부채총계' in account_name:
                key_metrics['total_liabilities'] = format_amount(item.get('thstrm_amount', '0'))
            elif '자본총계' in account_name:
                key_metrics['total_equity'] = format_amount(item.get('thstrm_amount', '0'))
            elif '매출액' in account_name:
                key_metrics['revenue'] = format_amount(item.get('thstrm_amount', '0'))
            elif '영업이익' in account_name:
                key_metrics['operating_income'] = format_amount(item.get('thstrm_amount', '0'))
            elif '당기순이익' in account_name:
                key_metrics['net_income'] = format_amount(item.get('thstrm_amount', '0'))
    
    return jsonify({
        'financial_data': financial_data,
        'key_metrics': key_metrics,
        'year': year,
        'report_code': report_code
    })

def analyze_financial_data_with_ai(financial_data, company_name):
    """Gemini AI를 사용하여 재무 데이터를 쉽게 분석"""
    try:
        # 주요 재무 지표 추출
        key_metrics = {}
        for item in financial_data:
            account_name = item.get('account_nm', '')
            fs_div = item.get('fs_div', '')
            
            if fs_div == 'CFS':  # 연결재무제표 기준
                if '자산총계' in account_name:
                    key_metrics['total_assets'] = format_amount(item.get('thstrm_amount', '0'))
                elif '부채총계' in account_name:
                    key_metrics['total_liabilities'] = format_amount(item.get('thstrm_amount', '0'))
                elif '자본총계' in account_name:
                    key_metrics['total_equity'] = format_amount(item.get('thstrm_amount', '0'))
                elif '매출액' in account_name:
                    key_metrics['revenue'] = format_amount(item.get('thstrm_amount', '0'))
                elif '영업이익' in account_name:
                    key_metrics['operating_income'] = format_amount(item.get('thstrm_amount', '0'))
                elif '당기순이익' in account_name:
                    key_metrics['net_income'] = format_amount(item.get('thstrm_amount', '0'))
        
        # AI 분석을 위한 프롬프트 생성
        prompt = f"""
        다음은 {company_name}의 2023년 재무 데이터입니다. 
        이 데이터를 바탕으로 일반인이 이해하기 쉽게 분석해주세요.

        주요 재무 지표:
        - 자산총계: {key_metrics.get('total_assets', 0):,}원
        - 부채총계: {key_metrics.get('total_liabilities', 0):,}원
        - 자본총계: {key_metrics.get('total_equity', 0):,}원
        - 매출액: {key_metrics.get('revenue', 0):,}원
        - 영업이익: {key_metrics.get('operating_income', 0):,}원
        - 당기순이익: {key_metrics.get('net_income', 0):,}원

        다음 형식으로 분석해주세요:

        1. **재무 건전성 분석**
        - 부채비율 계산 및 평가
        - 자본구조 분석

        2. **수익성 분석**
        - 매출 대비 영업이익률
        - 매출 대비 순이익률
        - 수익성 평가

        3. **투자 관점 분석**
        - 이 기업에 투자할 때 고려사항
        - 장단점 분석

        4. **일반인을 위한 요약**
        - 핵심 포인트 3가지
        - 투자 추천도 (매우 좋음/좋음/보통/주의/위험)

        한국어로 친근하고 이해하기 쉽게 설명해주세요.
        """
        
        # Gemini AI 모델 사용
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        print(f"AI 분석 오류: {e}")
        return "AI 분석 중 오류가 발생했습니다."

@app.route('/api/ai-analysis/<corp_code>')
def ai_analysis(corp_code):
    """AI 재무 분석 API 엔드포인트"""
    year = request.args.get('year', '2023')
    report_code = request.args.get('report_code', '11011')
    
    # 회사 정보 가져오기
    conn = sqlite3.connect('corp_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT corp_name FROM corporations WHERE corp_code = ?', (corp_code,))
    company_result = cursor.fetchone()
    conn.close()
    
    if not company_result:
        return jsonify({'error': '회사 정보를 찾을 수 없습니다.'}), 404
    
    company_name = company_result[0]
    
    # 재무 데이터 가져오기
    financial_data = get_financial_data(corp_code, year, report_code)
    
    if not financial_data:
        return jsonify({'error': '재무 데이터를 가져올 수 없습니다.'}), 404
    
    # AI 분석 수행
    analysis_result = analyze_financial_data_with_ai(financial_data, company_name)
    
    return jsonify({
        'company_name': company_name,
        'analysis': analysis_result,
        'year': year
    })

if __name__ == '__main__':
    init_database()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 