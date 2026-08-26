from django.urls import include, path

urlpatterns = [
    path('api/', include('concurso.urls')),
]
