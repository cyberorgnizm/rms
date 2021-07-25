import uuid
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views import generic
from django.db import transaction
from django.db.models.expressions import F
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import PurchaseOrder, PurchaseLine
from rms.apps.restaurants.models import Cafeteria, Menu


class CheckoutPurchasesView(generic.TemplateView):
    template_name = "order/checkout_detail.html"

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        try:
            # set of cafeterias orders were place
            cafeteria_set = set()
            # set of orders for cafeterias listed
            order_set = set()
            # set of menu present in cart
            menu_set = set()
            for _, item in request.session.get('cart').items():
                menu = Menu.objects.get(id=item["product_id"])
                menu_set.add(menu)

                cafeteria_name = menu.cafeteria.name
                cafeteria = Cafeteria.objects.get(name=cafeteria_name)

                if not cafeteria in cafeteria_set:
                    order = PurchaseOrder.objects.create(
                        order_id=uuid.uuid4(),
                        cafeteria=cafeteria,
                        student=request.user.student,
                        status='pending',
                        delivery_mode='pickup',
                        delivery_date=timezone.now(),
                        delivery_address=request.user.student.student_address
                    )
                    cafeteria_set.add(cafeteria)
                    order_set.add(order)

            for menu, cart_item in zip(menu_set, request.session.get('cart').items()):
                cart_menu = cart_item[1]
                quantity = int(cart_menu['quantity'])
                # filter order where menu cafeteria matches
                orders = [order for order in order_set if order.cafeteria == menu.cafeteria]
                if orders:
                    PurchaseLine.objects.create(
                        order=orders[0],
                        menu=menu,
                        quantity=quantity,
                        total_price=menu.price * quantity
                    )

        except Exception as exp:
            # TODO: handle exception when performing above computations
            return redirect(request.get_raw_uri())
        else:
            return redirect("orders:cart_detail")

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_cost"] = sum((float(item["price"]) * int(item["quantity"]) for _, item in self.request.session.get('cart').items()))
        return context


class PurchaseOrderDetailView(generic.DetailView):
    pass

class PurchaseOrderUpdateView(generic.UpdateView):
    pass

class PurchaseOrderListView(generic.ListView):
    pass


# ------------------------------------------------------------------------
# Shopping Cart: below section is used for managing items present in cart
# ------------------------------------------------------------------------

@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Menu.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Menu.objects.get(id=id)
    cart.remove(product)
    return redirect("orders:cart_detail")


@login_required(login_url="/accounts/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Menu.objects.get(id=id)
    cart.add(product=product)
    return redirect("orders:cart_detail")


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Menu.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("orders:cart_detail")


@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("orders:cart_detail")


@login_required(login_url="/accounts/login")
def cart_detail(request):
    item_count = len(request.session.get('cart'))
    quantity_sum = sum((int(item["quantity"]) for _, item in request.session.get('cart').items()))
    price_sum = sum((float(item["price"]) for _, item in request.session.get('cart').items()))
    total_price = sum((float(item["price"]) * int(item["quantity"]) for _, item in request.session.get('cart').items()))
    context = {"item_count": item_count, 'total_price': total_price, "price_sum": price_sum, "quantity_sum": quantity_sum}
    return render(request, 'cart/cart_detail.html', context=context)
