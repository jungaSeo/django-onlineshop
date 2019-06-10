from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):
    # 장바구니 초기화
    def __init__(self, request):
        self.session = request.session;
        # CART_ID key를 가진 세션이 있는지 체크
        cart = self.session.get(settings.CART_ID)
        login_id = self.session.get(settings.LOGIN_SESSION_ID)
        start = self.session.get(settings.START)
        print('start-value: ', settings.START)
        print('login-id: ', settings.LOGIN_SESSION_ID)

        # 세션이 없으면, 딕셔너리 만들어주어야 함.
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        # 세션이 있으면, 딕셔너리를 가지고 옴.
        self.cart = cart

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
            # yield == return; 없어지지 않고 계속 보유

    # 장바구니 추가
    def add(self, product, quantity=1, is_update = False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price':str(product.price)}

        if is_update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        # self.session[settings.CART_ID] = self.cart
        # self.session.modified = True
        self.save()
        print('장바구니에 추가되었습니다.')

    # 장바구니 내용물 한개씩 삭제
    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del (self.cart[product_id])
            self.save()
        print('장바구니에서 제거되었습니다.')

    # 장바구니 내용물 모두 삭제
    def clear(self):
        self.session[settings.CART_ID] = {}
        self.session.modified = True
        print('장바구니가 모두 삭제되었습니다.')

    # 세션에 장바구니 내역 저장
    def save(self):
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True