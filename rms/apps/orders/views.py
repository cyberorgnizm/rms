import os
import uuid
import json
import requests
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.cart import Cart
from rms.apps.accounts.models import Student, Worker
from rms.apps.restaurants.models import Cafeteria, Menu
from .models import PurchaseOrder, PurchaseLine, Invoice


class CheckoutPurchasesView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy("accounts:login")
    redirect_field_name = "redirect_to"
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
                        delivery_address=request.user.student.student_address
                    )
                    # verify transaction
                    if request.is_ajax():
                        body = json.loads(request.body)
                        response = requests.get(f"https://api.paystack.co/transaction/verify/{body['reference']}", headers={
                            "Authorization": f"Bearer {os.environ['PAYSTACK_SECRET']}"
                        }).json()

                        if response['message'] == "Verification successful":
                            Invoice.objects.create(
                                invoice_id=uuid.uuid4(),
                                order=order,
                                payment_reference=int(body['reference']),
                                cafeteria=order.cafeteria,
                                student=order.student,
                                due_date=timezone.now()
                            )
                    cafeteria_set.add(cafeteria)
                    order_set.add(order)

            for menu, cart_item in zip(menu_set, request.session.get('cart').items()):
                cart_menu = cart_item[1]
                quantity = int(cart_menu['quantity'])
                # filter order where menu cafeteria matches
                orders = [order for order in order_set if order.cafeteria == menu.cafeteria]
                if orders:
                    purchase_order = orders[0]
                    line = PurchaseLine.objects.create(
                        order=purchase_order,
                        menu=menu,
                        quantity=quantity,
                        total_price=menu.price * quantity
                    )
                    # update total price for order after total price for line item is calculated
                    purchase_order.total_price += float(line.total_price)
                    purchase_order.save()
        except Exception as exp:
            print(exp)
            # TODO: handle exception when performing above computations
            return redirect(request.get_raw_uri())
        else:
            cart = Cart(request)
            cart.clear()
            return redirect("orders:cart_detail")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_cost"] = sum((float(item["price"]) * int(item["quantity"]) for _, item in self.request.session.get('cart').items()))
        return context


class PurchaseOrderListView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy("accounts:login")
    redirect_field_name = "redirect_to"
    model = PurchaseOrder
    template_name = "order/purchases_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_student:
            student = Student.objects.get(user=self.request.user)
            queryset = queryset.filter(student=student)
            return queryset
        elif self.request.user.is_worker:
            worker = Worker.objects.get(user=self.request.user)
            queryset = queryset.filter(cafeteria=worker.cafeteria)
            return queryset
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pending_orders"] = self.get_queryset().filter(status='pending')
        context["cancelled_orders"] = self.get_queryset().filter(status='cancelled')
        context["completed_orders"] = self.get_queryset().filter(status='completed')
        return context


class PurchaseOrderDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = reverse_lazy("accounts:login")
    redirect_field_name = "redirect_to"
    model = PurchaseOrder
    slug_field = "order_id"
    slug_url_kwarg = "id"
    template_name = "order/purchase_detail.html"
    context_object_name = "order"
    

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_student:
            student = Student.objects.get(user=self.request.user)
            queryset = queryset.filter(student=student)
            return queryset
        elif self.request.user.is_worker:
            return queryset
        return queryset

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if request.user.is_worker:
            worker = Worker.objects.get(user=request.user)
            order = self.get_object()
            if request.POST.get('approve', None) == 'on':
                    for line in order.lines.all():
                        line.is_ready = True
                        line.save()
                    order.status = 'completed'
                    order.approved_by_worker = worker
                    order.save()
                    # create an invoice on approval
                    Invoice.objects.create(
                        invoice_id=uuid.uuid4(),
                        order=order,
                        cafeteria=order.cafeteria,
                        student=order.student,
                        due_date=timezone.now()
                    )
            elif request.POST.get('reject', None) == 'on':
                    for line in order.lines.all():
                        line.is_ready = False
                        line.save()
                    order.status = 'cancelled'
                    order.approved_by_worker = worker
                    order.save()
            return redirect("purchases")
            
        return redirect("purchase_detail", id=str(kwargs["id"]))


class PurchaseOrderUpdateView(generic.UpdateView):
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
