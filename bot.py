import requests
from bs4 import BeautifulSoup
import os

# 1. 우체통 주소 (비밀번호처럼 안전하게 숨겨둘 거예요)
WEBHOOK_URL = os.environ.get('DISCORD_URL')

# 2. 경인여대 공지사항 주소
SITE_URL = "https://www.kiwu.ac.kr/ko/cms/FR_CON/index.do?MENU_ID=310"

# 3. 로봇이 학교 홈페이지에 방문합니다.
response = requests.get(SITE_URL)
soup = BeautifulSoup(response.text, 'html.parser')

# 4. 글 목록 모음 안에서 제목 링크들을 찾습니다.
notice_links = soup.select('tbody tr a')

if len(notice_links) > 0:
    # 가장 위에 있는 첫 번째(최신) 글의 제목을 가져옵니다.
    new_title = notice_links[0].text.strip()
    
    # 5. 이전에 로봇이 기억해둔 '마지막 글 제목' 수첩을 열어봅니다.
    try:
        with open("last_notice.txt", "r", encoding="utf-8") as f:
            last_title = f.read().strip()
    except:
        last_title = ""

    # 6. 새로 확인한 글이 로봇이 기억하는 글과 다르다면? (새 공고가 떴다면!)
    if new_title != last_title:
        # 디스코드로 보낼 편지를 씁니다.
        message = {
            "content": f"🚨 **새로운 공지사항이 올라왔어요!**\n\n**제목:** {new_title}\n**확인하러 가기:** {SITE_URL}"
        }
        # 디스코드 우체통에 편지를 쏙 넣습니다.
        requests.post(WEBHOOK_URL, json=message)
        
        # 새로운 글 제목을 로봇의 수첩에 다시 적어둡니다. (다음번엔 중복으로 안 보내게!)
        with open("last_notice.txt", "w", encoding="utf-8") as f:
            f.write(new_title)
