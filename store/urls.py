from django.urls import path
from . import views
urlpatterns = [
    path('cart', views.cart, name="cart"),
    path('update_item', views.updateItem, name='update_item'),
    path('checkout', views.checkout, name='checkout'),
    path('processOrder', views.processOrder, name='processOrder'),
    path('paymentSuccess', views.paymentSuccess, name='paymentSuccess'),
    path('paymentError', views.paymentErr, name='paymentError'),
    path('create-checkout-session', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('webhook/stripe', views.my_webhook_view, name='webhook/stripe')

]