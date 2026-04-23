from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Categoria, Productos, Clientes, Pedidos


# ==============================
# EST DE CATEGORIA
# ==============================

class CategoriaTest(TestCase):

    def test_creacion_categoria(self):
        categoria = Categoria.objects.create(
            codigo="CAT001",
            nombre="Joyas"
        )
        self.assertEqual(categoria.nombre, "Joyas")


# ==============================
# TEST DE PRODUCTO
# ==============================

class ProductoTest(TestCase):

    def test_creacion_producto_valido(self):
        categoria = Categoria.objects.create(
            codigo="CAT001",
            nombre="Joyas"
        )

        producto = Productos.objects.create(
            codigo="PROD01",
            nombre="Anillo",
            precio=100,
            categoria=categoria
        )

        self.assertEqual(producto.nombre, "Anillo")
        self.assertEqual(producto.categoria.nombre, "Joyas")


# ==============================
# 👤 TEST DE CLIENTE
# ==============================

class ClienteTest(TestCase):

    def test_creacion_cliente(self):
        user = User.objects.create_user(
            username="valeria",
            password="12345"
        )

        cliente = Clientes.objects.create(
            codigo="CLI001",
            nombre="Valeria",
            apellidopaterno="Sosa",
            apellidomaterno="Lopez",
            correo="val@test.com",
            user=user
        )

        self.assertEqual(cliente.nombre, "Valeria")



# TEST DE USUARIO


class UsuarioTest(TestCase):

    def test_password_encriptado(self):
        user = User.objects.create_user(
            username="valeria",
            password="12345"
        )

        self.assertNotEqual(user.password, "12345")
        self.assertTrue(user.check_password("12345"))



# TEST DE PEDIDO
class PedidoTest(TestCase):

    def test_creacion_pedido(self):
        user = User.objects.create_user(
            username="val",
            password="123"
        )

        cliente = Clientes.objects.create(
            codigo="CLI001",
            nombre="Val",
            apellidopaterno="Test",
            apellidomaterno="User",
            correo="val@test.com",
            user=user
        )

        pedido = Pedidos.objects.create(
            codigo="PED001",
            cliente=cliente
        )

        self.assertEqual(pedido.cliente.nombre, "Val")


#TEST DE PAGO (LOGIN REQUIRED)
class PagoTest(TestCase):

    def test_usuario_no_logueado_no_puede_pagar(self):
        response = self.client.post(reverse('pagar_carrito'))
        self.assertEqual(response.status_code, 302)