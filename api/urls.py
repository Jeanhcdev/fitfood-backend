from django.urls import path, include
from rest_framework.routers import DefaultRouter
# 1. Importa PlanListView junto con las otras vistas
from .views import RegisterView, MeView, ClienteViewSet, ProductoViewSet, PedidoViewSet, PlanListView, MenuDetailView

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
    # Usa PlanListView directamente, sin 'views.'
    path('planes/', PlanListView.as_view(), name='plan-list'),
    # --- AÑADE ESTA NUEVA RUTA ---
    # '<int:pk>' es un parámetro dinámico que captura el ID del menú (ej: 1)
    path('menus/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),
    path('register/', RegisterView.as_view(), name='register'), # <-- AÑADE ESTA LÍNEA
    
    # Aquí puedes añadir otras rutas que no usen el router
    # path('register/', RegisterView.as_view(), name='register'),
    # path('me/', MeView.as_view(), name='me'),
]

# 2. Añade las URLs del router a urlpatterns
urlpatterns += router.urls
