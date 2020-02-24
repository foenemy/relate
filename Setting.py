from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import random
import time,re,os
from datetime import datetime

import win32api
import win32con

import urllib.parse

# import sentry_sdk
# from sentry_sdk import capture_exception
# sentry_sdk.init("https://d794285a418545868f837c97d45570c2@sentry.io/1885204")

########   setting   ##########

def setting():
	###### 브라우저 세팅 준비

	# 현재 파일 경로로 바꾸기
	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	# UA 선택
	UAFile = open('./spoofer.txt', 'rt').readlines()
	randomInt2 = random.randrange(0,len(UAFile))
	UA = UAFile[randomInt2]

	options = webdriver.ChromeOptions()
	# 이거 넣으니 로그인 안 됨.
	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option('useAutomationExtension', False)
	# options.add_argument('headless')
	# options.add_extension('./extension_1_1_0_0.crx')
	# options.add_argument('window-size=360,640')
	# pc size
	options.add_argument('window-size=1920,1080')
	# options.add_argument("disable-gpu")
	# 혹은 options.add_argument("--disable-gpu")
	options.add_argument("user-agent="+UA)

	binary = '../chromedriver.exe'
	browser = webdriver.Chrome(binary,chrome_options=options)		

	# 처음접속할 검색엔진 선택
	domainFile = open('./domain.txt', 'rt').readlines()
	randomInt = random.randrange(0,len(domainFile))
	domain = domainFile[randomInt]

	# browser.delete_all_cookies()
	# time.sleep(5)
	browser.get('http://'+domain)
	# time.sleep(3)
	return browser


def whatismyUA(browser):
	URL = 'https://www.whatismybrowser.com'
	browser.get(URL)
	time.sleep(10)
	return browser

def inputKW(string,keys,browser):

	try:
		# URL = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html'
		# URL = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%8C%80%EA%B5%AC+%EC%B9%A8%EC%82%B0%EB%8F%99+%EB%A7%9B%EC%A7%91&tqi=UNWrPdp0JywssNftUP8ssssstzR-320939'
		URL = 'https://naver.com'
		browser.get(URL)
		time.sleep(2)
		browser.execute_script('document.getElementById("query").focus()')
		keyboard = KeyBoardControl()
		keyboardAltTab(keyboard)
		mouseClickByJS(browser,'document.getElementById("query")')
		time.sleep(1)
		
		keyboardClick2(['hangul'])
		# if clickRandom(2) == 0:
		# 	print("한영키 클릭")
		# 	keyboardClick2(['hangul'])

		#대구 침산동 맛집
		typingKW(string,keys,browser)
		time.sleep(2)
		keyboardClick2(['enter'])
		time.sleep(2)

		# print(browser.find_element_by_css_selector('._related_keyword_ul').text)

	except Exception as e:
		print("def input2")
		print(e)
		# capture_exception(e)
		browser.quit()
	
	return browser	


def inputKW_bottom(string,keys,browser):

	try:
		keyboard = KeyBoardControl()
		# 기존탭으로 전환
		browser.switch_to.window(browser.window_handles[0])

		# 가장 아래 스크롤 내리기
		for i in range(0,4):
			win32api.keybd_event(keyboard.VK_CODE['spacebar'], 0,0,0)
			time.sleep(0.3)
			win32api.keybd_event(keyboard.VK_CODE['spacebar'], 0,win32con.KEYEVENTF_KEYUP,0)
			time.sleep(2)	

		# 아래 상자에 글자 입력
		browser.execute_script('document.getElementById("nx_query_btm").focus()')
		
		keyboardAltTab(keyboard)
		mouseClickByJS(browser,'document.getElementById("nx_query_btm")')

		time.sleep(1)
		# delete all
		for i in range(0,20):
			keyboardClick2(['del'])


		# 한영키 안 누르기
		# if clickRandom(2) == 0:
		# 	print("한영키 클릭")
		# 	keyboardClick2(['hangul'])

		#대구 침산동 맛집
		typingKW_bottom(string,keys,browser)
		time.sleep(2)
		keyboardClick2(['enter'])
		time.sleep(2)

		writeHistory(string)

		# print(browser.find_element_by_css_selector('._related_keyword_ul').text)

	except Exception as e:
		print("def inputKW_bottom")
		print(e)
		# capture_exception(e)
		browser.quit()
	
	return browser



# 키워드 입력
def typingKW(string,key,browser):

	keyboard = KeyBoardControl()
	#이번 키워드는 자동완성으로 클릭할까 말까 결정하기
	isAutoClick = clickRandom(2)
	print("isAutoClick 0이면 자동 완성 클릭 : "+str(isAutoClick))
	didAutoClick = False

	array_length = len(key)
	for i in range(array_length):
		time.sleep(0.5)
		# spacebar는 할때도 있고 안 할때도 있고...
		if key[i] == 'spacebar':
			randomInt = random.randrange(30,270)	
			if randomInt%3 != 0:
				win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,0,0)
				time.sleep(0.5)
				win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,win32con.KEYEVENTF_KEYUP,0)

		elif key[i] == 'alt':
			win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,0,0)
		else:
			win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,0,0)
			# time.sleep(0.5)
			win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,win32con.KEYEVENTF_KEYUP,0)


			# 이번에 자동완성 하기로 했고...키 입력할 때마다 1/3 확률로 자동완성 클릭
			temp = clickRandom(3)
			# print("temp 0이면 1/3 chance 자동 완성 클릭 : "+str(temp))

			if isAutoClick==0 and temp==0:

				if 'm.naver.com' in browser.current_url:
					autoCompleteLength = browser.execute_script('var a=document.getElementsByClassName("u_atcp_l").length;return a;')
				else:
					autoCompleteLength = browser.execute_script('var a=document.querySelectorAll(".words ul li").length;return a;')

				# print('autoCompleteLength '+str(autoCompleteLength))
				for i in range(0,autoCompleteLength):
					i_str = str(i)
					if 'm.naver.com' in browser.current_url:
						dataQuery = browser.execute_script('var dataQuery=document.getElementsByClassName("u_atcp_l")['+i_str+'].getAttribute("data-query");return dataQuery;')
					else:
						dataQuery = browser.execute_script('var dataQuery=document.querySelectorAll(".words ul li")['+i_str+'].innerText;return dataQuery;')
					# print(string+" : "+dataQuery)
					if string == dataQuery or string.replace(' ', '') == dataQuery:
						
						didAutoClick = True
						time.sleep(1)

						if 'm.naver.com' in browser.current_url:
							mouseClickByJS(browser,'document.getElementsByClassName("u_atcp_a")['+i_str+']')

						else:
							action = ActionChains(browser)
							firstLevelMenu = browser.find_element_by_css_selector(".words ul li:nth-child("+str(i+1)+")")
							# firstLevelMenu = browser.find_element_by_xpath("(//a[@class='keyword'])[1]")
							action.move_to_element(firstLevelMenu).perform()
							
							browser.execute_script('document.querySelectorAll(".words ul li")['+i_str+'].setAttribute("class","atcmp_on")')
							browser.execute_script('document.querySelectorAll(".words ul li")['+i_str+'].click()')

						break

		if didAutoClick == True:
			break


def typingKW_bottom(string,key,browser):

	keyboard = KeyBoardControl()

	array_length = len(key)
	for i in range(array_length):
		time.sleep(0.5)
		# spacebar는 할때도 있고 안 할때도 있고...
		if key[i] == 'spacebar':
			randomInt = random.randrange(30,270)	
			if randomInt%3 != 0:
				win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,0,0)
				time.sleep(0.5)
				win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,win32con.KEYEVENTF_KEYUP,0)

		elif key[i] == 'alt':
			win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,0,0)
		else:
			win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,0,0)
			# time.sleep(0.5)
			win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,win32con.KEYEVENTF_KEYUP,0)


def clickBlog(browser):
	time.sleep(5)
	# 블로그 탭있는 경우
	try:
		if 'm.' in browser.current_url:
			# 바로 플레이스 리스트 버튼 클릭
			mouseClickByJS(browser,'document.querySelector("._1zF_nelpFE a")')
		else:

			mouseClickByJS(browser,'document.querySelector(".sh_blog_title")')
			# mouseClickByJS(browser,'document.querySelector(".thumb_link")')
			
	except Exception as e:
		print("ERROR in search.naver.com page")
		print(e)
		# capture_exception(e)
	
	# 리뷰탭있는 경우
	try:
		if 'm.' in browser.current_url:
			# 바로 플레이스 리스트 버튼 클릭
			mouseClickByJS(browser,'document.querySelector("._1zF_nelpFE a")')
		else:
			mouseClickByJS(browser,'document.querySelector(".thumb_link")')
			
	except Exception as e:
		print("ERROR in search.naver.com page")
		print(e)
		# capture_exception(e)

		
	# 최근탭 활성화
	browser.switch_to.window(browser.window_handles[-1])
	time.sleep(3)
	try:
		browser.execute_script('document.querySelector("iframe").focus();')
	except Exception as e:
		print("no iframe")
		print(e)

	time.sleep(2)
	# 스크롤 작업
	keyboard = KeyBoardControl()
	for i in range(0,4):
		win32api.keybd_event(keyboard.VK_CODE['spacebar'], 0,0,0)
		time.sleep(0.3)
		win32api.keybd_event(keyboard.VK_CODE['spacebar'], 0,win32con.KEYEVENTF_KEYUP,0)
		time.sleep(2)

	time.sleep(60)
	time.sleep(1)	

	##################

	return browser


def closeTab(browser):
	
	time.sleep(1)
	browser.switch_to.window(browser.window_handles[-1])
	time.sleep(1)
	randomInt = random.randrange(20,60)
	try:
		mouseClickByJS(browser,'document.querySelectorAll("a")['+str(randomInt)+']')
	except Exception as e:
		pass
	time.sleep(2)
	browser.close()
	browser.switch_to.window(browser.window_handles[-1])
	time.sleep(1)
	randomInt = random.randrange(20,60)
	try:
		mouseClickByJS(browser,'document.querySelectorAll("a")['+str(randomInt)+']')
	except Exception as e:
		pass	
	time.sleep(2)
	browser.close()
	browser.switch_to.window(browser.window_handles[-1])
	time.sleep(3)

	return browser

# 191119 몇 번에 한 번 클릭할까 정하는 함수
def clickRandom(num):
	randomInt = random.randrange(1,num+1)
	isAutoClick = randomInt%num	
	return isAutoClick

# 191119 history파일에 글 쓰기
def writeHistory(data):
	f=open('history.txt','a')
	f.write(data+" / "+str(datetime.now())+'\n')
	f.close()


##########마우스 매크로 등 관련 메소드 ##############################


# 키보드 클릭
def keyboardClick2(key):
	keyboard = KeyBoardControl()
	array_length = len(key)
	for i in range(array_length):
		time.sleep(0.5)
		# spacebar는 할때도 있고 안 할때도 있고...
		if key[i] == 'spacebar':
			randomInt = random.randrange(30,270)	
			if randomInt%3 != 0:
				win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,0,0)
				time.sleep(0.5)
				win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,win32con.KEYEVENTF_KEYUP,0)

		elif key[i] == 'alt':
			win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,0,0)
				
		else:
			win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,0,0)
			time.sleep(0.5)
			win32api.keybd_event(keyboard.VK_CODE[key[i]], 0,win32con.KEYEVENTF_KEYUP,0)
	

def keyboardAltTab(keyboard):
	time.sleep(1)
	win32api.keybd_event(keyboard.VK_CODE['alt'], 0,0,0)
	win32api.keybd_event(keyboard.VK_CODE['tab'], 0,0,0)
	time.sleep(.05)
	win32api.keybd_event(keyboard.VK_CODE['tab'], 0,win32con.KEYEVENTF_KEYUP,0)
	win32api.keybd_event(keyboard.VK_CODE['alt'], 0,win32con.KEYEVENTF_KEYUP,0)
	time.sleep(2)
	win32api.keybd_event(keyboard.VK_CODE['alt'], 0,0,0)
	win32api.keybd_event(keyboard.VK_CODE['tab'], 0,0,0)
	time.sleep(.05)
	win32api.keybd_event(keyboard.VK_CODE['tab'], 0,win32con.KEYEVENTF_KEYUP,0)
	win32api.keybd_event(keyboard.VK_CODE['alt'], 0,win32con.KEYEVENTF_KEYUP,0)
	time.sleep(2)

# 무료 vpn으로 아이피 바꾸는 메소드	
def mouseMacro(self) :
	time.sleep(1)
	# 폰 잠금 해제
	self.mouseDbClick(1429,504)
	time.sleep(10)
	# 테더링 끄기 
	self.mouseClick(1306,307)
	time.sleep(7)
	# 테더링 켜기 
	self.mouseClick(1306,308)
	time.sleep(10)

def mouseClick(self,x,y) :
    x = int(x)
    y = int(y)
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def mouseDbClick(self,x,y) :
	self.mouseClick(x,y)
	time.sleep(0.1)
	self.mouseClick(x,y)

def addToClipBoard(self,text):
	command = 'echo ' + text.strip() + '| clip'
	os.system(command)  

def mouseClickByJS(browser,el):
	browser.execute_script('function mouseEvent(type, sx, sy, cx, cy) { var evt; var e = {bubbles: true,cancelable: (type != "mousemove"),view: window, detail: 0,    screenX: sx,     screenY: sy,    clientX: cx,     clientY: cy,    ctrlKey: false,    altKey: false,    shiftKey: false,    metaKey: false,    button: 0,    relatedTarget: undefined  };  if (typeof( document.createEvent ) == "function") {    evt = document.createEvent("MouseEvents");    evt.initMouseEvent(type,       e.bubbles, e.cancelable, e.view, e.detail,      e.screenX, e.screenY, e.clientX, e.clientY,      e.ctrlKey, e.altKey, e.shiftKey, e.metaKey,      e.button, document.body.parentNode);  } else if (document.createEventObject) {    evt = document.createEventObject();    for (prop in e) {    evt[prop] = e[prop];  }    evt.button = { 0:1, 1:4, 2:2 }[evt.button] || evt.button;  }  return evt;}function dispatchEvent (el, evt) {  if (el.dispatchEvent) {    el.dispatchEvent(evt);  } else if (el.fireEvent) {    el.fireEvent("on" + type, evt);  }  return evt;} var test = '+el+'; var evt = mouseEvent("click", 100, 600, 100, 600); dispatchEvent(test, evt);')	




class KeyBoardControl:

	VK_CODE = {'backspace':0x08,
	'tab':0x09,
	'clear':0x0C,
	'enter':0x0D,
	'shift':0x10,
	'ctrl':0x11,
	'alt':0x12,
	'pause':0x13,
	'caps_lock':0x14,
	'hangul':0x15,
	'esc':0x1B,
	'spacebar':0x20,
	'page_up':0x21,
	'page_down':0x22,
	'end':0x23,
	'home':0x24,
	'left_arrow':0x25,
	'up_arrow':0x26,
	'right_arrow':0x27,
	'down_arrow':0x28,
	'select':0x29,
	'print':0x2A,
	'execute':0x2B,
	'print_screen':0x2C,
	'ins':0x2D,
	'del':0x2E,
	'help':0x2F,
	'0':0x30,
	'1':0x31,
	'2':0x32,
	'3':0x33,
	'4':0x34,
	'5':0x35,
	'6':0x36,
	'7':0x37,
	'8':0x38,
	'9':0x39,
	'a':0x41,
	'b':0x42,
	'c':0x43,
	'd':0x44,
	'e':0x45,
	'f':0x46,
	'g':0x47,
	'h':0x48,
	'i':0x49,
	'j':0x4A,
	'k':0x4B,
	'l':0x4C,
	'm':0x4D,
	'n':0x4E,
	'o':0x4F,
	'p':0x50,
	'q':0x51,
	'r':0x52,
	's':0x53,
	't':0x54,
	'u':0x55,
	'v':0x56,
	'w':0x57,
	'x':0x58,
	'y':0x59,
	'z':0x5A,
	'numpad_0':0x60,
	'numpad_1':0x61,
	'numpad_2':0x62,
	'numpad_3':0x63,
	'numpad_4':0x64,
	'numpad_5':0x65,
	'numpad_6':0x66,
	'numpad_7':0x67,
	'numpad_8':0x68,
	'numpad_9':0x69,
	'multiply_key':0x6A,
	'add_key':0x6B,
	'separator_key':0x6C,
	'subtract_key':0x6D,
	'decimal_key':0x6E,
	'divide_key':0x6F,
	'F1':0x70,
	'F2':0x71,
	'F3':0x72,
	'F4':0x73,
	'F5':0x74,
	'F6':0x75,
	'F7':0x76,
	'F8':0x77,
	'F9':0x78,
	'F10':0x79,
	'F11':0x7A,
	'F12':0x7B,
	'F13':0x7C,
	'F14':0x7D,
	'F15':0x7E,
	'F16':0x7F,
	'F17':0x80,
	'F18':0x81,
	'F19':0x82,
	'F20':0x83,
	'F21':0x84,
	'F22':0x85,
	'F23':0x86,
	'F24':0x87,
	'num_lock':0x90,
	'scroll_lock':0x91,
	'left_shift':0xA0,
	'right_shift ':0xA1,
	'left_control':0xA2,
	'right_control':0xA3,
	'left_menu':0xA4,
	'right_menu':0xA5,
	'browser_back':0xA6,
	'browser_forward':0xA7,
	'browser_refresh':0xA8,
	'browser_stop':0xA9,
	'browser_search':0xAA,
	'browser_favorites':0xAB,
	'browser_start_and_home':0xAC,
	'volume_mute':0xAD,
	'volume_Down':0xAE,
	'volume_up':0xAF,
	'next_track':0xB0,
	'previous_track':0xB1,
	'stop_media':0xB2,
	'play/pause_media':0xB3,
	'start_mail':0xB4,
	'select_media':0xB5,
	'start_application_1':0xB6,
	'start_application_2':0xB7,
	'attn_key':0xF6,
	'crsel_key':0xF7,
	'exsel_key':0xF8,
	'play_key':0xFA,
	'zoom_key':0xFB,
	'clear_key':0xFE,
	'+':0xBB,
	',':0xBC,
	'-':0xBD,
	'.':0xBE,
	'/':0xBF,
	'`':0xC0,
	';':0xBA,
	'[':0xDB,
	'\\':0xDC,
	']':0xDD,
	"'":0xDE,
	'`':0xC0}

	def keyboardClick(self):
		pass