"""webplayground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.registration.url/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages.urls import urls_de_pages

# configurando media files
from django.conf import settings

from profiles.urls import profiles_patterns
from messenger.urls import messenger_patterns

urlpatterns = [
    # importando las urls de la app core
    path('', include('core.urls')),
    # importando las urls de la app pages
    path('pages/', include(urls_de_pages)), # se configura el 'nuevo' urls_patterns de la app pages
    path('admin/', admin.site.urls),
    
    # * Paths de auth:
    # con esto se dan de alta las siguientes rutas: 
    path('accounts/', include('django.contrib.auth.urls')),
    # accounts/ login/ [name='login']
    # accounts/ logout/ [name='logout']
    # accounts/ password_change/ [name='password_change']
    # accounts/ password_change/done/ [name='password_change_done']
    # accounts/ password_reset/ [name='password_reset']
    # accounts/ password_reset/done/ [name='password_reset_done']
    # accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/ reset/done/ [name='password_reset_complete']

    # paths de registro:
    path('accounts/', include('registration.urls')),

    # paths de profiles:
    path('profiles/', include(profiles_patterns)),

    # paths de messenger:
    path('messenger/', include(messenger_patterns)),
]

# configuración para imágenes
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)