from django.db import models


class Plato(models.Model):
    CATEGORIA_CHOICES = [
        ('entrada', 'Entrada'),
        ('fondo', 'Fondo'),
        ('extra', 'Plato Extra'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CHOICES)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['categoria', 'nombre']


class CartaDia(models.Model):
    fecha = models.DateField(unique=True)  # una carta por dia

    def __str__(self):
        return f"Carta del {self.fecha}"

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Carta del dia'
        verbose_name_plural = 'Cartas del dia'


class ItemMenu(models.Model):
    carta = models.ForeignKey(CartaDia, on_delete=models.CASCADE, related_name='items')
    plato = models.ForeignKey(Plato, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def titulo_seccion(self):
        return self.plato.get_categoria_display()

    @property
    def precio(self):
        return self.plato.precio

    def __str__(self):
        return f"{self.cantidad}x {self.plato.nombre} ({self.carta.fecha})"

    class Meta:
        unique_together = ('carta', 'plato')
