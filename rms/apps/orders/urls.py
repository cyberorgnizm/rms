from django.urls import path
from .views import (
    CheckoutPurchasesView, 
    PurchaseOrderListView, 
    PurchaseOrderDetailView,
    PurchaseOrderUpdateView,
    process_order_line,
    cart_add, cart_detail, 
    item_clear, item_increment, 
    item_decrement, cart_clear
)

app_name = "orders"

urlpatterns = [
    path('checkout/', CheckoutPurchasesView.as_view(), name='checkout'),
    path('orders/', PurchaseOrderListView.as_view(), name="purchases"),
    path('orders/<uuid:id>/', PurchaseOrderDetailView.as_view(), name="purchase_detail"),
    path('orders/<uuid:id>/update', PurchaseOrderUpdateView.as_view(), name="purchase_update"),
    path('orders/<uuid:id>/process-line/<int:line_id>', process_order_line, name="process_line"),
    # cart url configs     
    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/clear/', cart_clear, name='cart_clear'),
    path('cart/detail/', cart_detail,name='cart_detail'),
]