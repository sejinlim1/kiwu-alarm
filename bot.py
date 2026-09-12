import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.environ.get('DISCORD_URL')
SITE_URL = "https://www.kiwu.ac.kr/ko/cms/FR_CON/index.do?MENU_ID=310"

# 1. 로봇이 사람(크롬 브라우저)인 척하게 해주는 모자예요! (학교 홈페이지가 막지 않도록)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("1. 학교 홈페이지에 똑똑똑 노크합니다...")
response = requests.get(SITE_URL, headers=headers)
print(f"홈페이지 문 열림 상태: {response.status_code} (200이면 정상!)")

soup = BeautifulSoup(response.text, 'html.parser')
notice_links = soup.select('tbody tr a')

print(f"찾아낸 링크 개수: {len(notice_links)}개")

if len(notice_links) > 0:
    new_title = notice_links[0].text.strip()
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
    print("앗! 글 목록을 못 찾았어요. 홈페이지 구조가 달라서 코드를 수정해야 해요!")
