from django.db import models
from django.contrib.auth.models import User

class ClienteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True)
    direccion_principal = models.TextField(blank=True)
    def __str__(self):
        return self.user.username


class Categoria(models.Model):
    """
    Representa una categoría de producto, como 'Plato Principal', 'Ensalada', etc.
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costo_produccion = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoría") 
    calories = models.IntegerField(null=True, blank=True, verbose_name="Calorías aproximadas")
    imagen_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="URL de la Imagen")
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADOS = [
        ('RECIBIDO', 'Recibido'), ('EN_PREP', 'En preparación'),
        ('EN_CAMINO', 'En camino'), ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='RECIBIDO')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    direccion_entrega = models.TextField()
    notas_cliente = models.TextField(blank=True)
    def __str__(self):
        return f"Pedido #{self.id} de {self.cliente.username}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Pedido #{self.pedido.id}"

class Menu(models.Model):
    """
    Representa un menú semanal o diario que agrupa varios productos.
    """
    name = models.CharField(max_length=100, verbose_name="Nombre del Menú")
    
    # Este es el campo clave. Crea una relación de "muchos a muchos" con el modelo Producto.
    productos = models.ManyToManyField(Producto, verbose_name="Productos en el Menú")

    class Meta:
        verbose_name = "Menú"
        verbose_name_plural = "Menús"

    def __str__(self):
        # El __str__ debe representar al objeto actual, en este caso, el menú.
        return self.name

class Plan(models.Model):
    # --- Campos de Identificación ---
    name = models.CharField(max_length=100, verbose_name="Nombre del Plan")
    description = models.TextField(verbose_name="Descripción")
    
    # --- Campo para la Cantidad de Viandas ---
    cantidad_viandas = models.IntegerField(
        verbose_name="Cantidad de Viandas",
        help_text="Número de viandas incluidas en el plan. Dejar en 0 si la cantidad es personalizada.",
        default=0
    )

    # --- Campo para el Precio ---
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Precio del Plan",
        help_text="Precio total para planes con cantidad fija. Para planes personalizados, puede ser un precio base o 0.",
        null=True,
        blank=True
    )

    # --- La Clave para el Plan Personalizable ---
    permite_cantidad_personalizada = models.BooleanField(
        default=False, 
        verbose_name="¿Permite Cantidad Personalizada?",
        help_text="Marcar si el cliente puede elegir el número de viandas para este plan."
    )

    # --- Campos de Presentación y Control ---
    icon = models.CharField(max_length=50, blank=True, help_text="Nombre del ícono de Lucide (ej: Zap, Leaf, Heart, Beef,Star)")
    color = models.CharField(max_length=50, blank=True, help_text="Color del tema (ej: amarillo, verde, rojo, purpura)")
    is_active = models.BooleanField(default=True, verbose_name="¿Está activo?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Plan de Comida"
        verbose_name_plural = "Planes de Comida"

    def __str__(self):
        return self.name

