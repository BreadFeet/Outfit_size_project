from django.shortcuts import render, redirect

# Create your views here.
from frame.custdb import CustDB
from frame.error import ErrorCode
from frame.linkdb import LinkDB
from teamanalysis.teamanlysis import Analysis


def index(request):
    # print(dir(request.session))
    # print(request.session.keys())         # ['logininfo']
    # print(request.session.values())       # [{'id':'id01', 'name':'김영희'}]
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def loginimpl(request):
    id = request.POST['id']
    pwd = request.POST['pwd']

    try:
        cust = CustDB().selectOne(id)
        if pwd == cust.getPwd():
            request.session['logininfo'] = {'id': cust.getId(), 'name': cust.getName()}
            print(request.session['logininfo'])
            next = 'index.html'
            context = None
        else:
            raise Exception
    except:
        next = 'loginfail.html'
        context = {'msg': ErrorCode.e02}

    return render(request, next, context)

def logout(request):
    if request.session['logininfo'] != None:
        del request.session['logininfo']
    return render(request, 'index.html')


def signup(request):
    return render(request, 'signup.html')

def signupimpl(request):
    id = request.POST['id']
    pwd = request.POST['pwd']
    name = request.POST['name']
    age = int(request.POST['age'])
    height = float(request.POST['ht'])
    weight = int(request.POST['wt'])
    try:
        CustDB().insert(id, pwd, name, age, height, weight)
        return render(request, 'signupsuccess.html')
    except Exception as err:
        print(err)
        context = {'msg': ErrorCode.e01}
        return render(request, 'signupfail.html', context)


def recommend(request):
    id = request.session['logininfo']['id']
    cust = CustDB().selectOne(id)
    age = cust.getAge()
    height = cust.getHt()
    weight = cust.getWt()
    # 분석화면이랑 연결해야 함
    size = Analysis().sizeRecomm(age, height, weight)
    # 해당 사이즈에 맞는 웹사이트 링크 가져오기
    links = LinkDB().selectOne(size)
    context = {
        'size': size,
        'mf': links[0],
        'yoox': links[1]
    }
    return render(request, 'recommend.html', context)
