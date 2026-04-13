from django.urls import path
from . import views

urlpatterns = [
    path('', views.PedidoListCreateAPIView.as_view(), name='pedido_list_create'),
    path('<int:pk>/', views.PedidoRetrieveUpdateDestroyAPIView.as_view(), name='pedido_detail_update_delete'),
]
