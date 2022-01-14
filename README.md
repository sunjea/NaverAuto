# naver_autoprogram

# 기능 설명
1. 네이버 카페 댓글을 빨리 다는 기능
2. 네이버 카페 자동 출석 체크 기능

## 동작 방식
1. 카페 댓글 기능
 - 기본 동작은 주기적인 스케쥴 동작으로 해당 카페 ID 와 특정 API 주소로 대상이 새글을 작성했는지 체크.
 - 해당 대상이 새글 등록 시 자동 댓글 등록 API 실행 ( 이때 등록되는 ID 는 'n_aut', 'n_ses' 등록된 네이버 로그인 고유 세션키로 등록 )

2. 출석 체크 기능
 - 등록된 카페 ID 의 URL 로 30분 주기 새로고침을 통해 자동 출석횟수 증가 ( 여기서도 증가시킬 회원정보는 'n_aut', 'n_ses' 키의 네이버 ID 기준 )

# 사용 방법
## 필수 설치 
1) python 3.9.x ,pyqt5 , requests

## 설치 방법
- python 생략 ( 개발환경에 맞게 설치 )
- pip install pyqt5
- pip install requests

# INI 파일 만들기
- 실행하기 위해서는 ini 파일이 필요함.
- main.py 와 같은 디렉토리에 auto.ini 파일 생성
- 아래와 같이 파일 작성
( ID 는 여러개 설정으로 등록해서 사용 가능, AUTH, SESS 가져오는 방법은 값은 글 하단부분 참고 )


```
[COMMON]

ACCOUNT_CNT = 1

ID_0 = 
PASSSWD_0 = 

[COMMENTER]
## test
CAFFEID = 11887565 
## Kann 
#CAFFEID = 29118241

## test
CHECKER_URI = https://apis.naver.com/cafe-web/cafe-mobile/CafeMemberNetworkArticleList?search.cafeId=11887565&search.memberKey=xHvQQfnay_QW_GQTv9Ziow&search.perPage=40&search.page=1&requestFrom=B

## Kann KapUchiNo -- THIS USE
#CHECKER_URI = https://apis.naver.com/cafe-web/cafe-mobile/CafeMemberNetworkArticleList?search.cafeId=29118241&search.memberKey=uclL7CZV-8neohJyN6dIAw&search.perPage=40&search.page=1&requestFrom=B

## Kann_manager
# CHECKER_URI = https://apis.naver.com/cafe-web/cafe-mobile/CafeMemberNetworkArticleList?search.cafeId=29118241&search.memberKey=AeTNY4uU7_53EX6k23ujeA&search.perPage=40&search.page=1&requestFrom=B
## Kann_kaki
# CHECKER_URI = https://apis.naver.com/cafe-web/cafe-mobile/CafeMemberNetworkArticleList?search.cafeId=29118241&search.memberKey=AkE9kKRptSgOX7_OkHAC6Q&search.perPage=40&search.page=1&requestFrom=B

COMMENT_TEXT_0 = a

[CHECKER]

API_URI = https://apis.naver.com/cafe-web/cafe-mobile/CafeMemberLevelInfo?cafeId=29118241
```


