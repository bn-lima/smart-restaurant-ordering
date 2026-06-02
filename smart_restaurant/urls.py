from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('device/', include('devices.urls')),
    path('control_panel/', include('control_panel.urls')),
    path('menu/', include('restaurant_menu.urls')),
    path('cart/', include('cart.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)