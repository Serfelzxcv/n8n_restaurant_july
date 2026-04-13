from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.PlatoListCreateAPIView.as_view(), name='plato_list_create'),
    path('<int:pk>/', views.PlatoRetrieveUpdateDestroyAPIView.as_view(), name='plato_detail_update_delete'),
    path('cartas/', views.CartaListCreateAPIView.as_view(), name='carta_list_create'),
    re_path(r'^cartas/(?P<fecha>\d{4}-\d{2}-\d{2})/$', views.CartaByDateAPIView.as_view(), name='carta_by_date'),
    path('cartas/<int:pk>/', views.CartaRetrieveUpdateDestroyAPIView.as_view(), name='carta_detail_update_delete'),
    path('cartas/<int:carta_pk>/items/', views.ItemMenuListCreateAPIView.as_view(), name='item_menu_list_create'),
    path('cartas/<int:carta_pk>/items/<int:pk>/', views.ItemMenuRetrieveUpdateDestroyAPIView.as_view(), name='item_menu_detail_update_delete'),
    path('<str:categoria>/', views.PlatoPorCategoriaListAPIView.as_view(), name='plato_list_by_categoria'),
]
