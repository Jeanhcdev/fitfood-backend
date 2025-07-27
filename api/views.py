from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Producto, Pedido, DetallePedido, Plan, Menu
from .serializers import RegisterSerializer, UserSerializer, ProductoSerializer, PedidoSerializer, PlanSerializer, MenuSerializer

class MenuDetailView(generics.RetrieveAPIView):
    """
    Vista para obtener los detalles de un único menú por su ID.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [AllowAny] # Permite que cualquiera vea el menú


class RegisterView(generics.CreateAPIView):
    """
    Vista para registrar nuevos usuarios.
    Accesible por cualquiera (AllowAny).
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class ClienteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('-fecha_creacion')
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Pedido.objects.all().order_by('-fecha_pedido')
        return Pedido.objects.filter(cliente=self.request.user).order_by('-fecha_pedido')

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

class PlanListView(generics.ListAPIView):
    # Ahora solo obtenemos los planes donde is_active es verdadero
    queryset = Plan.objects.filter(is_active=True) 
    serializer_class = PlanSerializer
    permission_classes = [AllowAny]


class MenuListView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [AllowAny]

# El DetallePedido ahora se gestiona a través del PedidoViewSet, por lo que no necesita su propio ViewSet.
