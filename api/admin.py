from django.contrib import admin
from .models import Plan , Producto, Menu, Categoria 



# --- Personalización para el modelo Producto (Opcional pero recomendado) ---
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_venta',"costo_produccion", "calories", 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre', 'descripcion')


# --- Personalización para el modelo Menu ---
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    # Esta es la línea mágica que cambia la interfaz
    filter_horizontal = ('productos',)
    list_display = ('name',)
    search_fields = ('name',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Este método personaliza el queryset para el campo de selección de productos.
        """
        # Comprobamos si el campo que se está renderizando es 'productos'
        if db_field.name == "productos":
        # Modificamos el queryset para que solo incluya productos disponibles
            kwargs["queryset"] = Producto.objects.filter(disponible=True)
        
        # Devolvemos el campo con el queryset modificado
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# --- Registra los otros modelos de forma simple si no necesitan personalización ---
admin.site.register(Plan)
admin.site.register(Categoria)
# admin.site.register(Producto) 