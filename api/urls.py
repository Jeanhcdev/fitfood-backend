from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  ProductoViewSet, PlanListView, MenuDetailView, FeaturedMenuView, ResenaListView, ResenaCreateView

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')

urlpatterns = [
    # Usa PlanListView directamente, sin 'views.'
    path('planes/', PlanListView.as_view(), name='plan-list'),
    # '<int:pk>' es un parámetro dinámico que captura el ID del menú (ej: 1)
    path('menus/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),
    path('menus/destacado/', FeaturedMenuView.as_view(), name='menu-destacado'),
    # --- AÑADE ESTA NUEVA RUTA ---
    # Esta única ruta maneja dos acciones diferentes:
    # 1. GET a /reseñas/ -> Llama a ReseñaListView para obtener la lista.
    # 2. POST a /reseñas/ -> Llama a ReseñaCreateView para crear una nueva.
    path('reseñas/', ResenaListView.as_view(), name='reseña-list'),
    path('reseñas/crear/', ResenaCreateView.as_view(), name='reseña-create'),
]

# 2. Añade las URLs del router a urlpatterns
urlpatterns += router.urls
