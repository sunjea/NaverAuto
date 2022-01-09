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

AUTH_0 = OueJc2e24WcGxZRgNFyX...
SESS_0 = AAABqMf6G8ePcPIH4UJ4WuLwDOuCSJLf...

[COMMENTER] 

## Kann 
CAFFEID = 29118241

## Kann
CHECKER_URI = https://apis.naver.com/cafe-web/cafe-mobile/CafeMemberNetworkArticleList?search.cafeId=29118241&search.memberKey=uclL7CZV-8neohJyN6dIAw&search.perPage=40&search.page=1&requestFrom=B

COMMENT_TEXT = a

[CHECKER]

API_URI = https://apis.naver.com/cafe-web/cafe-mobile/CafeMemberLevelInfo?cafeId=29118241

```

# 네이버 세션 키 등록 하기 
해당 프로그램을 사용하기 위해선 로그인 정보가 필요함. ( 'n_aut', 'n_ses' 키 부분임 )
확인 방법은
1) 네이버에 로그인 후 "F12 개발자 모드" 로 network 부분 클릭
2) 네이버 페이지 새로 고침
3) www.naver.com 요청 부분 찾기
4) Request 부분에 cookie 값 확인 
예)
cookie: NNB=4RDPYNED2VSGC; NM_THEME_EDIT=; ASID=dd95af010000017c722aeecb00000059; PM_MY_NOTICE_TOOLTIP=Y; NID_AUT=89U1PNkPF/CUF4+yrG1tWNMqXI0BZ01cuV8G3lDH+qxPva+GQAeZYSPdTLNVmRXo; NID_JKL=NWdfmrfIoC8d0s9Y2mX0cfwZb4b3V0lwiqzgMdzJd3Y=; NV_WETR_LAST_ACCESS_RGN_M="MDk1OTAxMDc="; NV_WETR_LOCATION_RGN_M="MDk1OTAxMDc="; nx_ssl=2; NM_THEME_LAST_FIXED=CARGAME; NDARK=N; page_uid=hieQksprvTossP5VaEZssssst70-218397; _naver_usersession_=H2HgQ53jgx48FmHFos52qA==; PM_CK_loc=dbb76f46a236a564f445f25761a317ebe251f1cd5c9026abb61a0f126b922b70; NID_SES=AAABrai6wGVKCOTNgbwnwBqqUeqssXctRUujAVJhl...

5) 위처럼 나온 쿠기에서 NID_AUT 값 , NID_SES 값 만 복사 해서 넣기.
예)
NID_AUT = 89U1PNkPF/CUF4+yrG1tWNMqXI0BZ01cuV8G3lDH+qxPva+...;
NID_SES = AAABrai6wGVKCOTNgbwnwBqqUeqssXctRUujAVJhl...

# 실행하기
1) 위에서 설정한 바로가기 버튼으로 리모트 디버그 크롬 실행.
2) python main.py  실행 후 UI 에서 원하는 기능 버튼 클릭.

