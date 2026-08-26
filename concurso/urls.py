from django.urls import path

from .views import EstadisticasView, EventoFechaView, GanadoresView, InscripcionView

urlpatterns = [
    path('inscripciones/', InscripcionView.as_view(), name='inscripciones'),
    path('ganadores/', GanadoresView.as_view(), name='ganadores'),
    path('estadisticas/', EstadisticasView.as_view(), name='estadisticas'),
    path('evento/<int:pk>/fecha/', EventoFechaView.as_view(), name='evento-fecha'),
]
