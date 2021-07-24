from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('checkout/', views.CheckoutPurchasesView.as_view(), name='checkout'),
    # cart url configs     
    path('add/<int:id>/', views.cart_add, name='cart_add'),
    path('clear/<int:id>/', views.item_clear, name='item_clear'),
    path('increment/<int:id>/', views.item_increment, name='item_increment'),
    path('decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('clear/', views.cart_clear, name='cart_clear'),
    path('detail/',views.cart_detail,name='cart_detail'),
]