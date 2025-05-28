from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.getMain, name="main"),
    path('logIn/', views.logIn, name="logIn"),
    path('logUp/', views.logUp, name="logUp"),
    path('logOut/', views.logOut, name="logOut"),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('shop/', views.shop, name="shop"),
    path('product/<int:id>', views.getProduct, name="product"),
    path('addComent/<int:id>', views.addComent, name="addComent"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
