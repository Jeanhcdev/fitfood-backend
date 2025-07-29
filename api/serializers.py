from rest_framework import serializers
from .models import Producto, Plan, Menu, Resena


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
            'imagen_url', 
            'disponible', 
            'fecha_creacion', 
            'fecha_actualizacion'
        ]


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
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
        
        productos_del_menu = menu.productos.filter(disponible=True).select_related('categoria').all()

        for producto in productos_del_menu:
            categoria_nombre = producto.categoria.nombre if producto.categoria else "Otros"
            
            if categoria_nombre not in grouped_products:
                grouped_products[categoria_nombre] = []
            
            producto_data = ProductoSerializer(producto, context=self.context).data
            grouped_products[categoria_nombre].append(producto_data)
        
        return grouped_products

class ResenaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Reseña.
    Convierte los objetos Reseña a formato JSON.
    """
    class Meta:
        model = Resena
        # Especificamos los campos que el frontend podrá ver y enviar.
        # Notar que no incluimos el campo 'aprobado', ya que eso se maneja internamente.
        fields = ['id', 'nombre', 'instagram', 'comentario', 'calificacion', 'fecha_creacion']
