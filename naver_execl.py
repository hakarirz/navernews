from bs4 import BeautifulSoup
import requests
import openpyxl

fpath = r'C:\vspy\TEST2\tenline.xlsx'

base_url = "https://search.naver.com/search.naver?where=view&sm=tab_jum&query="
print("검색하는 키워드에 맞춰 뉴스가 검색됩니다.")
keyword = input("검색어를 입력하세요: ")

search_url = base_url + keyword

r = requests.get(search_url)

soup = BeautifulSoup(r.text, "html.parser")

items = soup.select(".title_link._cross_trigger")

# 엑셀 파일 생성 또는 열기
wb = openpyxl.Workbook()
ws = wb.active

# 열 제목 추가
ws.append(['뉴스 번호', '뉴스 제목', '뉴스 링크'])

# 각 열의 최대 길이를 저장할 딕셔너리
max_lengths = {'A': len('뉴스 번호'), 'B': len('뉴스 제목'), 'C': len('뉴스 링크')}

for e, item in enumerate(items, 1):
    # 링크 가져오기
    news_link = item.get('href') if item.get('href') else '링크 없음'

    # 엑셀에 데이터 추가
    ws.append([e, item.text, news_link])

    # 데이터의 길이를 확인하여 각 열의 최대 길이 업데이트
    max_lengths['A'] = max(max_lengths['A'], len(str(e)))
    max_lengths['B'] = max(max_lengths['B'], len(item.text))
    max_lengths['C'] = max(max_lengths['C'], len(news_link))

# 각 열의 최대 길이를 기준으로 열의 너비를 동적으로 조절
for column, max_length in max_lengths.items():
    adjusted_width = max_length + 30  # 여유 공간을 두기 위해 +2
    ws.column_dimensions[column].width = adjusted_width

# 엑셀 파일 저장
wb.save(fpath)

print(f"데이터가 {fpath}에 저장되었습니다.")
print("다시 검색시 엑셀 파일은 초기화 됩니다.")
