from rest_framework import generics

from .models import Pedido
from .serializers import PedidoSerializer


class PedidoListCreateAPIView(generics.ListCreateAPIView):#sirve para trabajar con la lista de pedidos y crear nuevos pedidos
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


class PedidoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):#sirve para trabajar con un pedido específico: obtener detalles, actualizar o eliminar
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
