# prestamos/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [


    # ======================================
    # PÁGINA PRINCIPAL
    # ======================================

    path(
        "",
        views.inicio,
        name="inicio"
    ),



    # ======================================
    # LIBROS
    # ======================================

    path(
        "libros/",
        views.lista_libros,
        name="lista_libros"
    ),



    # ======================================
    # PRÉSTAMOS DEL USUARIO
    # ======================================

    path(
        "mis-prestamos/",
        views.mis_prestamos,
        name="mis_prestamos"
    ),



    # ======================================
    # DETALLE DEL PRÉSTAMO
    # ======================================

    path(
        "detalle-prestamo/<int:prestamo_id>/",
        views.detalle_prestamo,
        name="detalle_prestamo"
    ),



    # ======================================
    # CARRITO / SOLICITUD DE PRÉSTAMO
    # ======================================

    path(
        "carrito/",
        views.ver_carrito,
        name="ver_carrito"
    ),



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



    # ======================================
    # DEVOLUCIÓN
    # ======================================

    path(
        "devolver/<int:prestamo_id>/",
        views.devolver_libro,
        name="devolver_libro"
    ),



    # ======================================
    # REPORTE GENERAL
    # ======================================

    path(
        "reporte-prestamos/",
        views.reporte_prestamos,
        name="reporte_prestamos"
    ),



    # ======================================
    # AUTENTICACIÓN
    # ======================================

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

]