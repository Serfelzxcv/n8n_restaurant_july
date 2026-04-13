from drf_spectacular.utils import extend_schema, extend_schema_view
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import CartaDia, ItemMenu, Plato
from .serializers import CartaDiaSerializer, ItemMenuSerializer, PlatoSerializer


@extend_schema_view(
    get=extend_schema(operation_id='products_list_all'),
)
class PlatoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Plato.objects.all()
    serializer_class = PlatoSerializer


class PlatoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plato.objects.all()
    serializer_class = PlatoSerializer


@extend_schema_view(
    get=extend_schema(operation_id='products_list_by_categoria'),
)
class PlatoPorCategoriaListAPIView(generics.ListAPIView):
    serializer_class = PlatoSerializer

    def get_queryset(self):
        categoria = self.kwargs['categoria'].lower()
        if categoria == 'entrada':
            return Plato.objects.filter(categoria='entrada')
        if categoria == 'extra':
            return Plato.objects.filter(categoria='extra')
        if categoria in {'fondo', 'menu'}:
            return Plato.objects.filter(Q(categoria='fondo') | Q(categoria='menu'))

        if categoria not in {'entrada', 'extra', 'fondo', 'menu'}:
            raise NotFound('Categoria no valida. Usa entrada, fondo o extra.')

        return Plato.objects.none()


class CartaListCreateAPIView(generics.ListCreateAPIView):
    queryset = CartaDia.objects.all()
    serializer_class = CartaDiaSerializer

    def create(self, request, *args, **kwargs):
        fecha = request.data.get('fecha')
        existing = CartaDia.objects.filter(fecha=fecha).exists()
        
        if existing:
            return Response(
                {'error': f'Ya existe una carta para la fecha {fecha}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CartaByDateAPIView(generics.RetrieveAPIView):
    queryset = CartaDia.objects.all()
    serializer_class = CartaDiaSerializer
    lookup_field = 'fecha'
    lookup_url_kwarg = 'fecha'


class CartaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartaDia.objects.all()
    serializer_class = CartaDiaSerializer


class ItemMenuListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ItemMenuSerializer

    def get_queryset(self):
        return ItemMenu.objects.filter(carta_id=self.kwargs['carta_pk'])

    def perform_create(self, serializer):
        carta = get_object_or_404(CartaDia, pk=self.kwargs['carta_pk'])
        serializer.save(carta=carta)


class ItemMenuRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemMenuSerializer

    def get_queryset(self):
        return ItemMenu.objects.filter(carta_id=self.kwargs['carta_pk'])
