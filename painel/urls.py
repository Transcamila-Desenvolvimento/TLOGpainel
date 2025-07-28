from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('auth/', include('usuarios.urls')),
    path('core/', include('core.urls')),
    path('', include('usuarios.urls'))
]
