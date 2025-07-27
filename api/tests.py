from django.test import TestCase
from .models import Producto
from decimal import Decimal

class PedidoAPITest(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas de pedidos
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.producto1 = Producto.objects.create(nombre="Ensalada Fit", precio_venta=Decimal('10.50'))
        self.producto2 = Producto.objects.create(nombre="Jugo Verde", precio_venta=Decimal('3.00'))

        self.url = reverse('pedido-list')

    def test_create_pedido(self):
        """
        Asegura que un usuario autenticado puede crear un pedido y el total se calcula correctamente.
        """
        data = {
            "direccion_entrega": "Avenida Siempre Viva 742",
            "detalles_write": [
                {"producto_id": self.producto1.id, "cantidad": 2},
                {"producto_id": self.producto2.id, "cantidad": 1}
            ]
        }
        response = self.client.post(self.url, data, format='json')

        # Verificamos que la respuesta fue exitosa
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verificamos que el total del pedido es correcto
        # (2 * 10.50) + (1 * 3.00) = 21.00 + 3.00 = 24.00
        self.assertEqual(response.data['total'], '24.00')

        # Verificamos que el pedido fue asignado al usuario correcto
        self.assertEqual(response.data['cliente']['username'], self.user.username)
