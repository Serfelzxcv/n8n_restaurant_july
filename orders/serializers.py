from decimal import Decimal

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, extend_schema_field, extend_schema_serializer
from rest_framework import serializers

from .models import ItemPedido, Pedido
from products.models import Plato


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Pedido con items',
            value={
                'numero_persona': 4,
                'items': [
                    {
                        'plato_id': 1,
                        'cantidad': 2,
                        'detalle': 'sin cebolla',
                    },
                    {
                        'plato_id': 3,
                        'cantidad': 1,
                        'detalle': 'bien caliente',
                    },
                ],
            },
            request_only=True,
        )
    ]
)
class ItemPedidoSerializer(serializers.ModelSerializer):
    plato_id = serializers.PrimaryKeyRelatedField(queryset=Plato.objects.all(), source='plato')
    subtotal = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ItemPedido
        fields = ['id', 'plato_id', 'cantidad', 'detalle', 'subtotal']
        read_only_fields = ['id', 'subtotal']

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_subtotal(self, obj) -> Decimal:
        return obj.subtotal


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Crear pedido',
            value={
                'numero_persona': 4,
                'items': [
                    {
                        'plato_id': 1,
                        'cantidad': 2,
                        'detalle': 'sin cebolla',
                    },
                    {
                        'plato_id': 3,
                        'cantidad': 1,
                        'detalle': 'bien caliente',
                    },
                ],
            },
            request_only=True,
        )
    ]
)
class PedidoSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    items = ItemPedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ['id', 'numero_persona', 'fecha', 'total', 'items']
        read_only_fields = ['id', 'fecha', 'total']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError('El pedido debe incluir al menos un plato.')
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        pedido = Pedido.objects.create(**validated_data)

        for item_data in items_data:
            ItemPedido.objects.create(pedido=pedido, **item_data)

        return pedido

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                ItemPedido.objects.create(pedido=instance, **item_data)

        return instance

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_total(self, obj) -> Decimal:
        return obj.total
