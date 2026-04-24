from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# Create your models here.
class Categoria(models.Model):
    codigo=models.CharField(primary_key=True,max_length=6, default='DEF001')
    nombre=models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Productos(models.Model):
    codigo=models.CharField(primary_key=True,max_length=6)
    nombre=models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE , default=1)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    precio = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.01)]  #Precio mínimo 0.01
    )
    def __str__(self):
        return f"{self.nombre} ({self.categoria.nombre})"
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

class Clientes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    codigo = models.CharField(primary_key=True, max_length=6)
    apellidopaterno = models.CharField(max_length=50)
    apellidomaterno = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    correo = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidopaterno} {self.apellidomaterno}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

class Pedidos(models.Model):
    codigo = models.CharField(primary_key=True, max_length=6)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[
        ('Pendiente', 'Pendiente'),
        ('Procesado', 'Procesado'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado')
    ], default='Pendiente')

    def __str__(self):
        return f"Pedido {self.codigo} - {self.cliente.nombre}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"