from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ClienteProfile, Producto, Pedido, DetallePedido, Plan, Menu
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

# --- Serializers de Registro y Usuario ---
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'telefono', 'direccion_principal')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('clienteprofile', {})
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()

        profile = user.clienteprofile
        profile.telefono = profile_data.get('telefono', '')
        profile.direccion_principal = profile_data.get('direccion_principal', '')
        profile.save()

        return user

class ClienteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteProfile
        fields = ['telefono', 'direccion_principal']

class UserSerializer(serializers.ModelSerializer):
    clienteprofile = ClienteProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'clienteprofile']

# --- Serializers de Productos y Pedidos ---
class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = [
            'id', 
            'nombre', 
            'descripcion', 
            'precio_venta', 
            'categoria',
            'calories',
            'imagen_url',  # <-- El campo de imagen
            'disponible', 
            'fecha_creacion', 
            'fecha_actualizacion'
        ]


class DetallePedidoWriteSerializer(serializers.ModelSerializer):
    producto_id = serializers.IntegerField()
    class Meta:
        model = DetallePedido
        fields = ['producto_id', 'cantidad']

class DetallePedidoReadSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    class Meta:
        model = DetallePedido
        fields = ['id', 'producto', 'cantidad', 'precio_unitario']

class PedidoSerializer(serializers.ModelSerializer):
    # Campo de solo lectura para mostrar los detalles
    detalles = DetallePedidoReadSerializer(many=True, read_only=True)
    # Campo de solo escritura para recibir los detalles al crear
    detalles_write = DetallePedidoWriteSerializer(many=True, write_only=True)
    cliente = UserSerializer(read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'fecha_pedido', 'estado', 'total', 'direccion_entrega', 'notas_cliente', 'detalles', 'detalles_write']
        read_only_fields = ['total', 'estado']

    @transaction.atomic
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles_write')
        pedido = Pedido.objects.create(**validated_data)

        total_pedido = 0
        for detalle_data in detalles_data:
            producto = Producto.objects.get(id=detalle_data['producto_id'])
            precio = producto.precio_venta
            cantidad = detalle_data['cantidad']
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio
            )
            total_pedido += (precio * cantidad)

        pedido.total = total_pedido
        pedido.save()

        return pedido

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        # Asegúrate de que 'icon' y 'color' estén en esta lista
        fields = [
            'id', 
            'name', 
            'description', 
            'cantidad_viandas', 
            'precio', 
            'permite_cantidad_personalizada', 
            'icon',  
            'color'  
        ]


class MenuSerializer(serializers.ModelSerializer):
    categorias = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ('id', 'name', 'categorias')

    def get_categorias(self, menu):
        grouped_products = {}
        
        # --- LÍNEA MODIFICADA ---
        # Añadimos .filter(disponible=True) para obtener solo los productos activos del menú
        productos_del_menu = menu.productos.filter(disponible=True).select_related('categoria').all()

        for producto in productos_del_menu:
            categoria_nombre = producto.categoria.nombre if producto.categoria else "Otros"
            
            if categoria_nombre not in grouped_products:
                grouped_products[categoria_nombre] = []
            
            producto_data = ProductoSerializer(producto, context=self.context).data
            grouped_products[categoria_nombre].append(producto_data)
        
        return grouped_products
