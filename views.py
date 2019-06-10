from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.views.decorators.http import require_POST
from cart.forms import AddProductForm
from .cart import *

@require_POST # if문 역할 대신함. 자바에선 annotation. 파이썬에서는 decorator
def add(request, product_id):
    # request.session['login_id'] = 'kgjava'
    # print('장바구니에 넣는 제품id: ', product_id)
    cart = Cart(request) # 객체생성, 초기화
    product = get_object_or_404(Product, id=product_id) # db 서치
    # 유효한 값이 들어가 있는지 체크
    # input에 들어간 values를 가지고 옴.
    form = AddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        # input data 처리
        # db, form, hidden값 add
        cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])
    return redirect('cart:detail')
    # redirect : 페이지 넘김. 다른 함수 호출.
def remove(request):
    pass

def detail(request):
    cart = Cart(request)
    for product in cart:
        product['quantity_form'] = AddProductForm(initial={'quantity':product['quantity'], 'is_update':True})
    return render(request, 'cart/detail.html', {'cart':cart})