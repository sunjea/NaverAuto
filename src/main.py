import time 
import sys 
from PyQt5.QtWidgets import * 
from PyQt5 import uic 
from PyQt5.QtCore import *
from login import naver_session

import configparser
import requests 

#UI파일 연결 #단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다. 
form_class = uic.loadUiType("ui/main.ui")[0] 
 
config = configparser.ConfigParser()
config.read('./auto.ini')

account_cnt = config['COMMON']['ACCOUNT_CNT']

n_aut = []
n_sess = []
commentText = []

for conf in range(0, int(account_cnt)) :
    a_str = 'AUTH_' + str(conf)
    s_str = 'SESS_' + str(conf)
    c_str = 'COMMENT_TEXT_' + str(conf)
  
    try :
        n_aut.append(config['COMMON'][a_str])
        n_sess.append(config['COMMON'][s_str])
        commentText.append(config['COMMENTER'][c_str])
    except :
        pass

url_api = config['CHECKER']['API_URI']
caffeId = config['COMMENTER']['CAFFEID']
apiReqUrI = config['COMMENTER']['CHECKER_URI']

class CommentThread(QThread): 
    def __init__(self, parent): 
        super().__init__(parent) 
        self.parent = parent 
    
    def run(self): 
        loop = True
        find = True

        user_agent = 'Mozilla/5.0 1.2.1'
        header = {'User-Agent': user_agent, 'cookie' : 'NID_AUT='+n_aut[0]+' NID_SES='+n_sess[0] } 
        req = requests.get(apiReqUrI, headers = header).json() 
        
        result = req['message']['status']                       # 결과
        totalCnt = req['message']['result']['totalCount']       # 전체 Count
        oldtotalCnt = totalCnt   
      
        while loop :
            find = True

            secs = time.time()
            tm = time.localtime(secs)
            nowtime = time.strftime('%Y-%m-%d %I:%M:%S %p', tm)
            self.parent.txtLog.append(nowtime + ' ID 찾는중 ..')
            while find :
                
                header = {'User-Agent': user_agent, 'cookie' : 'NID_AUT='+n_aut[0]+' NID_SES='+n_sess[0] } 
                req = requests.get(apiReqUrI, headers = header).json() 
                # req = requests.get(apiReqUrI).json()
                result = req['message']['status']                       # 결과
                totalCnt = req['message']['result']['totalCount']       # 전체 Count 
                
                if totalCnt !=  oldtotalCnt :
                    articleid = req['message']['result']['articleList'][0]['articleid']
                    # oldtotalCnt = totalCnt
                    find = False
                    break
               
                time.sleep(0.2)
        
            url = ''
            url += 'https://m.cafe.naver.com/ca-fe/web/cafes/'+ caffeId + '/articles/'
            url += str(articleid)
            url += '/comments?search.clubid='+caffeId+'&search.articleid='
            url += str(articleid)
            timeout = 5
            
            for conf in range(0, int(account_cnt)) :    
                jsondata = {'cafeId':caffeId, 'articleId': articleid, 'content':commentText[conf], 'requestFrom' : 'B'}
                user_agent = 'Mozilla/5.0 1.2.' + str(conf)
                headers = {'User-Agent': user_agent, 'cookie' : 'NID_AUT='+n_aut[conf]+' NID_SES='+n_sess[conf] } 
                rsp = requests.post('https://apis.naver.com/cafe-web/cafe-mobile/CommentPost.json', data=jsondata, headers=headers, timeout=timeout)
 
                if rsp.status_code == 200 :
                    self.parent.txtLog.append(nowtime + ' 댓글 작성완료')
                    loop = False
                else : 
                    self.parent.txtLog.append(nowtime + ' 댓글 작성실패')
                    oldtotalCnt -= oldtotalCnt
                    loop = False
 

class CheckThread(QThread): 
    def __init__(self, parent): 
        super().__init__(parent) 
        self.parent = parent
        self.working = True 
    
    def run(self): 
        
        sec = 1800
        while self.working :    
            secs = time.time()
            tm = time.localtime(secs)
            string = time.strftime('%Y-%m-%d %I:%M:%S %p', tm)
                
            if sec == 0 or sec == 1800 :
                self.parent.txtLog.append("체크 시간 : " + string )
                timeout = 5
                for conf in range(0, int(account_cnt)) :
                    user_agent = 'Mozilla/5.0 1.2.' + str(conf)
                    header = {'User-Agent': user_agent, 'cookie' : 'NID_AUT='+n_aut[conf]+' NID_SES='+n_sess[conf] } 
                    req = requests.get(url_api, headers = header).json() 
                    self.parent.txtLog.append("카페 멤버 상태 : {0} ".format(req['message']['result']['isCafeMember'] == True and "맴버" or "비회원"))

                    if req['message']['result']['isCafeMember'] == True :
                        self.parent.txtLog.append('닉네임 : ' + req['message']['result']['clubMember']['nickname'] + '  출석 횟수 : ' + str(req['message']['result']['clubMember']['cafeMemberActivity']['cafeVisit'] ) )
                    time.sleep(1)
                    sec = 1800 - int(account_cnt)
            
            sec -= 1
            self.parent.lcdNumber_2.display(sec)
            time.sleep(1) 
  
            
class WindowClass(QMainWindow, form_class) : 
    def __init__(self) : 
        super().__init__() 
        self.setupUi(self) 
        
        #각 버튼에 대한 함수 연결 
        self.btn_comment.clicked.connect(self.func_comment)
        self.btn_check.clicked.connect(self.func_check_start) 
    
        self.commentThr = CommentThread(parent=self)
        self.checkThr = CheckThread(parent=self)

    def func_comment(self) :
        self.txtLog.clear()        
        self.commentThr.start()

    def func_check_start(self) :
        self.txtLog.clear()

        if self.btn_check.text() == '자동 출책 정지' :
            self.btn_check.setText('자동 출책 시작') 
            self.checkThr.working = False
        else :
            self.checkThr.start()
            self.checkThr.working = True
            self.btn_check.setText('자동 출책 정지')

if __name__ == "__main__" : 
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show() 
    app.exec_()
 