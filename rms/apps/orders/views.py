from django.shortcuts import render, redirect
from django.views import generic
from django.db import transaction
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import PurchaseOrder, PurchaseLine
from rms.apps.restaurants.models import Menu


class CheckoutPurchasesView(generic.TemplateView):
    template_name = "order/checkout_detail.html"

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
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
