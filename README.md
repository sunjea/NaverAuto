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
1) python 3.9.x ,pyqt5 , requests, selenium

## 설치 방법
- python 생략 ( 개발환경에 맞게 설치 )
- pip install pyqt5
- pip install selenium
- pip install requests

## 사용환경 구성하기
- 해당 매크로에서 사용하는 크롬 드라이버는 95.0.4638.69(공식 빌드)(64비트) 버전을 기준으로 사용하고 있음
- 하여 사용하려는 장비의 크롬 버전이 맞지 않다면 드라이버를 별도 다운받아야 함.
( 드라이버 다운 링크 : https://chromedriver.chromium.org/downloads )

## 디버그로 사용할 크롬을 기본 크롬으로 셋팅 하기
** 이는 소스상 " options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  " 해당 부분 때문에 설정하는 것으로 
   해당 방법을 사용하지 않고 디버그 크롬을 사용해도 된다.
1. 사용하고 있는 크롬 브라우저의 바로가기 새로 만들기
2. 바로가기 우클릭-> 속성에서 "대상(T)" 부분을 아래와 같이 추가 해준다.
** 주의 : 하기 임시 크롬의 파일들 경로는 별도 생성해주는것이 좋음 ( 크롬 실행시 이력이나 기타 파일들이 많이생성됨.. )

"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="D:\ChormeTemp"

1) C:\Program Files (x86)\Google\Chrome\Application\chrome.exe : 기본 크롬 실행파일 위치
2) --remote-debugging-port=9222 : 임시 리모트 포트 설정
3) --user-data-dir="D:\ChormeTemp" : 임시 크롬의 파일 생성 

## 네이버 세션 키 등록 하기 ( 추후 자동화 예정 )
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

## 실행하기
1) 위에서 설정한 바로가기 버튼으로 리모트 디버그 크롬 실행.
2) python main.py  실행 후 UI 에서 원하는 기능 버튼 클릭.

