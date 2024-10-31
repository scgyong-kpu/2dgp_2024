import re

pat = re.compile(r'\s+<img src="/resources/sheet_icons/(\d+)/(\d+).png[^"]*" alt="([^"]+)"[^>]*>\s*$')
'''
  r'     : Regular Expression 의 시작을 알리는 quote. 그냥 따옴표로 열면 \\ 를 escape 해야 해서 r' 로 여는 것이 편하다
  \\s+   : \\s = space char. + = 1 or more. 앞에 빈칸이 1개 이상 있다.
  ()     : 그룹. 위 패턴에는 모두 3 개의 그룹이 있어 각각 grade, number, name 으로 해석될 예정이다.
  \\d+   : \\d = digit.  + = 1 or more. 슬래시 사이의 숫자들 을 의미한다.
  [^"]*  : 따옴표가 아닌 글자들. * = 0 or more. png 이후 따옴표가 닫힐때까지 글자가 존재할 수도 있다
  [^"]+  : 따옴표가 아닌 글자들. + = 1 or more. alt="..." 에 쿠키 이름이 쓰여 있다.
  [^>]*  : 닫는 > 가 아닌 글자들. alt=".." 부터 > 까지 뭔가 글자가 있을수 있어서 부시하기 위해 쓴다
'''

with open('out/cookierun.html', 'r') as f:
    while True:
        str = f.readline()
        if not str: break

        m = pat.match(str)
        if not m: continue
        grade, number, name = m.groups()
        char = { "id": number, "name": name, "grade": grade }
        print(char)


