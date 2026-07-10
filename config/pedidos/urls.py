# prestamos/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # Página principal
    path("", views.inicio, name="inicio"),

    # Libros
    path("libros/", views.lista_libros, name="lista_libros"),

    # Historial de préstamos
    path("mis-prestamos/", views.mis_prestamos, name="mis_prestamos"),

    # Carrito (Selección de libros)
    path("carrito/", views.ver_carrito, name="ver_carrito"),

    path(
        "agregar/<int:libro_id>/",
        views.agregar_libro,
        name="agregar"
    ),

    path(
        "eliminar/<int:libro_id>/",
        views.eliminar_libro,
        name="eliminar"
    ),

    path(
        "restar/<int:libro_id>/",
        views.restar_libro,
        name="restar"
    ),

    path(
        "limpiar/",
        views.limpiar_carrito,
        name="limpiar"
    ),

    path(
        "confirmar/",
        views.confirmar_prestamo,
        name="confirmar_prestamo"
    ),

    # Devolución de libros
    path(
        "devolver/<int:prestamo_id>/",
        views.devolver_libro,
        name="devolver_libro"
    ),

    # Login
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    # Reportes
    path(
        "reporte-prestamos/",
        views.reporte_prestamos,
        name="reporte_prestamos"
    ),  
]