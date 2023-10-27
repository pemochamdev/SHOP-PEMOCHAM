from django.urls import path

from core import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove-single-item-from-cart/<slug>/', views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
]
