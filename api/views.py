from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Producto, Plan, Menu, Resena
from .serializers import ProductoSerializer,PlanSerializer, MenuSerializer, ResenaSerializer

class MenuDetailView(generics.RetrieveAPIView):
    """
    Vista para obtener los detalles de un único menú por su ID.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [AllowAny] # Permite que cualquiera vea el menú

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('-fecha_creacion')
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PlanListView(generics.ListAPIView):
    # Ahora solo obtenemos los planes donde is_active es verdadero
    queryset = Plan.objects.filter(is_active=True) 
    serializer_class = PlanSerializer
    permission_classes = [AllowAny]

class MenuListView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [AllowAny]

class FeaturedMenuView(APIView):
    """
    Devuelve el único menú que está marcado como 'es_destacado'.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            # Intenta encontrar el primer menú que sea destacado
            menu_destacado = Menu.objects.get(es_destacado=True)
            # Usa el serializador que ya creamos
            serializer = MenuSerializer(menu_destacado, context={'request': request})
            return Response(serializer.data)
        except Menu.DoesNotExist:
            # Si no se encuentra ningún menú destacado
            return Response(
                {"error": "No hay un menú destacado configurado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Menu.MultipleObjectsReturned:
            # Si accidentalmente se marcaron varios menús como destacados
            return Response(
                {"error": "Hay múltiples menús destacados configurados. Solo debe haber uno."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ResenaListView(generics.ListAPIView):
    """
    Vista para LISTAR solo las reseñas que han sido aprobadas.
    El frontend usará esta vista para mostrar los testimonios.
    """
    # El queryset solo incluye reseñas donde el campo 'aprobado' es True.
    queryset = Resena.objects.filter(aprobado=True)
    serializer_class = ResenaSerializer
    permission_classes = [AllowAny] # Cualquiera puede ver las reseñas aprobadas.

class ResenaCreateView(generics.CreateAPIView):
    """
    Vista para que CUALQUIER usuario pueda CREAR una nueva reseña.
    La reseña se guardará como 'aprobado=False' por defecto.
    """
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer
    permission_classes = [AllowAny] # Cualquiera puede enviar una reseña.
