import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.environ.get('DISCORD_URL')
SITE_URL = "https://www.kiwu.ac.kr/ko/cms/FR_CON/index.do?MENU_ID=310"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("1. 학교 홈페이지에 똑똑똑 노크합니다...")
response = requests.get(SITE_URL, headers=headers)
print(f"홈페이지 문 열림 상태: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')

# '표(table)' 안에 있는 모든 링크(a 태그)를 찾습니다. (구조가 달라도 다 잡을 수 있어요!)
notice_links = soup.select('table a')

real_notices = []
for link in notice_links:
    title = link.text.strip()
    # 3글자 이상이고, 파일 다운로드 링크가 아닌 경우만 '진짜 제목'으로 인정합니다.
    if len(title) > 3 and "첨부파일" not in title:
        real_notices.append(title)

print(f"찾아낸 진짜 제목 개수: {len(real_notices)}개")

if len(real_notices) > 0:
    new_title = real_notices[0]
    print(f"2. 홈페이지 최신 글 제목: {new_title}")
    
    try:
        with open("last_notice.txt", "r", encoding="utf-8") as f:
            last_title = f.read().strip()
    except:
        last_title = ""
        
    print(f"3. 로봇 수첩에 적힌 글 제목: {last_title}")

    if new_title != last_title:
        print("4. 새로운 글 발견! 디스코드로 편지를 보냅니다.")
        message = {
            "content": f"🚨 **새로운 공지사항이 올라왔어요!**\n\n**제목:** {new_title}\n**확인하러 가기:** {SITE_URL}"
        }
        res = requests.post(WEBHOOK_URL, json=message)
        print(f"디스코드 우체통 전송 결과: {res.status_code} (204면 대성공!)")
        
        with open("last_notice.txt", "w", encoding="utf-8") as f:
            f.write(new_title)
    else:
        print("4. 에구, 아직 새로운 글이 안 올라왔네요. (그래서 알림 안 보냄!)")
else:
    print("앗! 홈페이지에서 아무 글자도 못 찾았어요. 홈페이지 주소나 구조 확인이 필요해요!")
