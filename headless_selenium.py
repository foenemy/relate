#네이버 연관작업 먼저 PC
# 셀레니움 사용

from selenium import webdriver
import time,re,os,subprocess
import Setting
# import sentry_sdk
# from sentry_sdk import capture_exceptio n
# sentry_sdk.init("https://d794285a418545868f837c97d45570c2@sentry.io/1885204")

keywordList = [
['모시모시','부산대 맛집',['q', 'n', 't', 'k', 's', 'e', 'o', 'spacebar', 'a', 'k', 't', 'w', 'l', 'q'],['a', 'h', 't', 'l', 'a', 'h', 't', 'l']],
['이안헤어3호점','서면여자커트',['t', 'j', 'a', 'u', 's', 'd', 'u', 'w', 'k', 'z', 'j', 'x', 'm'],['d', 'l', 'd', 'k', 's', 'g', 'p', 'd', 'j', '3', 'g', 'h', 'w', 'j', 'a']],
['티앤북스 남포점','남포동 카페',['s', 'k', 'a', 'v', 'h', 'e', 'h', 'd', 'spacebar', 'z', 'k', 'v', 'p'],['x', 'l', 'd', 'o', 's', 'q', 'n', 'r', 't', 'm', 'spacebar', 's', 'k', 'a', 'v', 'h', 'w', 'j', 'a']],
['부산대 토모','부산대 술집',['q', 'n', 't', 'k', 's', 'e', 'o', 'spacebar', 't', 'n', 'f', 'w', 'l', 'q'],['q', 'n', 't', 'k', 's', 'e', 'o', 'spacebar', 'x', 'h', 'a', 'h']],
# ['다깡','부산 중앙동 맛집',['q', 'n', 't', 'k', 's', 'spacebar', 'w', 'n', 'd', 'd', 'k', 'd', 'e', 'h', 'd', 'spacebar', 'a', 'k', 't', 'w', 'l', 'q']],
]


for j in range(10000):
	i = j%len(keywordList) 


	try:
		# 키워드 갯수에 따라 아이피 변경 e
		print(i)
		if i == 0:
			os.chdir("C:\Program Files (x86)\OneClickTethering\OneClickThthering")
			subprocess.call("adb start-server")
			time.sleep(2)
			subprocess.call("adb shell svc data disable")
			time.sleep(2)
			subprocess.call("adb shell svc data enable")
			time.sleep(3)
		browser = Setting.setting()
		time.sleep(5)
		# browser = Setting.whatismyUA(browser)
		# 뉴스 등 탐색
		browser = Setting.inputKW(keywordList[i][1],keywordList[i][2],browser)
		# time.sleep(500)
		browser = Setting.clickBlog(browser)

		browser = Setting.inputKW_bottom(keywordList[i][0],keywordList[i][3],browser)

		browser = Setting.clickBlog(browser)
		# # 플레이스 안에서 스크롤하기
		# # browser.implicitly_wait(3)
		time.sleep(2)
		browser = Setting.closeTab(browser)
		browser.quit()
	except Exception as e:
		print(e)
		# capture_exception(e)
		browser.quit()

	time.sleep(1200)