from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_data(symbol):
    url = 'http://finance.naver.com/item/sise.nhn?code={}'.format(symbol)
    with urlopen(url) as doc:
        soup = BeautifulSoup(doc, "lxml", from_encoding="euc-kr")
    # id가 _nowval인 <strong>태그를 찾아 cur_price변수에 <strong class="tah p11" id="_nowVal">262,000</strong>태그가 저장된다.
        cur_price = soup.find('strong', id='_nowVal')
    # id가 _rate인 <strong>태그를 찾아 cur_price변수에 <strong id="_rate"><span class="tah p11 nv01">-1.13%</span></strong>태그가 저장된다.
        cur_rate = soup.find('strong', id='_rate')
    # <title> 태그를 찾는다. stock변수에 <title>NAVER : 네이버 금융</title> 태그가 저장된다.
        stock = soup.find('title')
    # <title> 태그에서 콜론 문자를 기준으로 문자열 분리, 종목명을 구한 뒤 문자열 좌우의 공백을 제거
        stock_name = stock.text.split(':')[0].strip()
        return cur_price.text, cur_rate.text.strip(), stock_name


def main_view(request):
    querydict = request.GET.copy()
    mylist = querydict.lists()  # GET방식으로 넘어온 querydict 형태의 url을 리스트 형태로 변환
    rows = []
    total = 0

    for x in mylist:
        # mylist의 종목코드로 get_data 함수를 호출하여 현재가, 등락률, 종목명을 구한다.
        cur_price, cur_rate, stock_name = get_data(x[0])
        price = cur_price.replace(',', '')
        # mylist의 종목수를 int형으로 변환한 뒤 천의 자리마다 쉼표를 포함하는 문자열로 변환
        stock_count = format(int(x[1][0]), ',')
        sum = int(price) * int(x[1][0])
        stock_sum = format(sum, ',')
        # 종목명, 종목코드, 현재가, 주식수, 등락률, 평가금액을 리스트로 생성하여 rows 리스트에 추가
        rows.append([stock_name, x[0], cur_price,
                    stock_count, cur_rate, stock_sum])
        # 평가 금액을 주식수로 곱한 뒤 total 변수에 더한다
        total = total + int(price) * int(x[1][0])

    total_amount = format(total, ',')
    # balance.html 파일에 전달할 값들을 values 딕셔너리에 저장
    values = {'rows': rows, 'total': total_amount}
    # balance.html 파일을 표시하도록 render()함수를 호출하며 인숫값에 해당하는 values 딕셔너리를 넘겨준다.
    return render(request, 'balance.html', values)
