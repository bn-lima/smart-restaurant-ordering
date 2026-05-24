from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('device/', include('devices.urls')),
    path('control_panel/', include('control_panel.urls'))
]
