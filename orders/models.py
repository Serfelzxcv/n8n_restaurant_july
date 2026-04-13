from django.db import models


class Pedido(models.Model):
    numero_persona = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"Pedido #{self.id} - Persona {self.numero_persona}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    plato = models.ForeignKey('products.Plato', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    detalle = models.CharField(max_length=500, blank=True, null=True)

    @property
    def subtotal(self):
        return self.plato.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad}x {self.plato.nombre}"
