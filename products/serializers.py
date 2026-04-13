from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from .models import CartaDia, ItemMenu, Plato


class PlatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plato
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Crear carta del dia',
            value={
                'fecha': '2026-04-07',
                'items': [
                    {
                        'plato_id': 1,
                        'cantidad': 1,
                    },
                    {
                        'plato_id': 3,
                        'cantidad': 2,
                    },
                ],
            },
            request_only=True,
        )
    ]
)
class ItemMenuSerializer(serializers.ModelSerializer):
    titulo_seccion = serializers.CharField(read_only=True)
    precio = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    plato_id = serializers.PrimaryKeyRelatedField(queryset=Plato.objects.all(), source='plato')

    class Meta:
        model = ItemMenu
        fields = ['id', 'carta', 'plato_id', 'cantidad', 'precio', 'titulo_seccion']
        extra_kwargs = {
            'carta': {'read_only': True},
        }


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Carta del dia con platos',
            value={
                'fecha': '2026-04-07',
                'items': [
                    {
                        'plato_id': 1,
                        'cantidad': 1,
                    },
                    {
                        'plato_id': 3,
                        'cantidad': 2,
                    },
                ],
            },
            request_only=True,
        )
    ]
)
class CartaDiaSerializer(serializers.ModelSerializer):
    items = ItemMenuSerializer(many=True)

    class Meta:
        model = CartaDia
        fields = ['id', 'fecha', 'items']
        read_only_fields = ['id']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError('La carta del dia debe incluir al menos un plato.')

        platos = set()
        for item in value:
            plato = item['plato']
            if plato.id in platos:
                raise serializers.ValidationError('No puedes repetir el mismo plato en la carta del dia.')
            platos.add(plato.id)
        return value

    def validate(self, attrs):
        fecha = attrs.get('fecha')
        existing = CartaDia.objects.filter(fecha=fecha).first() if fecha else None

        if self.instance is None and existing:
            raise serializers.ValidationError(
                {'non_field_errors': [f'Ya existe una carta para la fecha {fecha}']}
            )
        return attrs

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        fecha = validated_data['fecha']
        carta = CartaDia.objects.filter(fecha=fecha).first()

        if carta is None:
            carta = CartaDia.objects.create(**validated_data)
        else:
            for attr, value in validated_data.items():
                setattr(carta, attr, value)
            carta.save()
            carta.items.all().delete()

        for item_data in items_data:
            ItemMenu.objects.create(carta=carta, **item_data)

        return carta

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                ItemMenu.objects.create(carta=instance, **item_data)

        return instance
