"""
URL configuration for starprinting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.views.static import serve as serve_media

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('star_admin.urls')),
    path('pricing/', include('pricing.urls')),
    # Serves downloaded WhatsApp images/PDFs (whitenoise only serves STATIC_ROOT,
    # not MEDIA_ROOT). Fine for a small admin tool; move to S3/Cloudinary if the
    # host's disk is wiped on every deploy.
    path('media/<path:path>', serve_media, {'document_root': settings.MEDIA_ROOT}),
]
