from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.getMain, name="main"),
    path('logIn/', views.logIn, name="logIn"),
    path('logUp/', views.logUp, name="logUp"),
    path('logOut/', views.logOut, name="logOut"),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('shop/<int:page>', views.shop, name="shop"),
    path('product/<int:id>', views.getProduct, name="product"),
    path('addComent/<int:id>', views.addComent, name="addComent"),
    path('profile/<int:id>/', views.getProfile, name="profile"),
    path('profile/<int:id>/edit', views.editProfile, name="edit"),
    path('user/basket/<int:id>', views.getBasket, name="userBasket"),
    path('product/<int:id>/addToBasket/', views.addToBasket, name="addToBasket"),
    path('user/basket/<int:basketId>/delete/<int:productId>', views.deleteProductBasket, name="deleteProductBasket"),
    path('user/basket/<int:basketId>/pay/', views.pay, name="pay"),

    # Password Reset path
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
