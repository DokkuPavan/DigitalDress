"""
URL configuration for DigitalDress project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from app.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('', user_login, name='login'),
    path("signup/", user_signup, name="signup"),
    path('shop/', shop, name="shop"),
    path('checkout/', check_out, name='checkout'),
    path('contact/', contact, name='contact'),
    path('product_details/', product_details, name='product_details'),
    path('trial/', trail, name='trial'),
    path('trail_res/', trail_res, name='trail_res'),
    path('trial1/<str:image_id>/', trail1, name='trial1'),
    path('store_image_url/', store_image_url, name='store_image_url'),
    path('profile/', profile, name='profile'),

]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)