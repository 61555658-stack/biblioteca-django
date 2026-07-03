# prestamos/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import date, timedelta

from .carrito import Carrito
from .models import Libro, Prestamo, DetallePrestamo


# ======================================
# BÚSQUEDA Y LISTA DE LIBROS
# ======================================

def lista_libros(request):

    buscar = request.GET.get('buscar', '')

    if buscar:
        libros = Libro.objects.filter(
            titulo__icontains=buscar
        )
    else:
        libros = Libro.objects.all()

    return render(
        request,
        "libros/lista.html",
        {
            "libros": libros,
            "buscar": buscar
        }
    )


# ======================================
# CONTROL DEL CARRITO
# ======================================

def agregar_libro(request, libro_id):

    carrito = Carrito(request)

    libro = Libro.objects.get(id=libro_id)

    carrito.agregar(libro)

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "lista_libros"
        )
    )


def eliminar_libro(request, libro_id):

    carrito = Carrito(request)

    libro = Libro.objects.get(id=libro_id)

    carrito.eliminar(libro)

    return redirect("ver_carrito")


def restar_libro(request, libro_id):

    carrito = Carrito(request)

    libro = Libro.objects.get(id=libro_id)

    carrito.restar(libro)

    return redirect("ver_carrito")


def limpiar_carrito(request):

    carrito = Carrito(request)

    carrito.limpiar()

    return redirect("ver_carrito")


def ver_carrito(request):

    carrito = request.session.get(
        "carrito",
        {}
    )

    return render(
        request,
        "carrito.html",
        {
            "carrito": carrito
        }
    )


# ======================================
# REGISTRAR PRÉSTAMO
# ======================================

@login_required
def confirmar_prestamo(request):

    carrito_sesion = request.session.get("carrito")

    if not carrito_sesion:
        return redirect("lista_libros")

    prestamo = Prestamo.objects.create(
        usuario=request.user,
        fecha_devolucion=date.today() + timedelta(days=7),
        estado="Prestado"
    )

    for key, value in carrito_sesion.items():

        libro = Libro.objects.get(id=key)

        cantidad = value["cantidad"]

        if libro.stock < cantidad:

            messages.error(
                request,
                f"No hay stock disponible para {libro.titulo}"
            )

            prestamo.delete()

            return redirect("ver_carrito")

        DetallePrestamo.objects.create(
            prestamo=prestamo,
            libro=libro,
            cantidad=cantidad
        )

        libro.stock -= cantidad

        libro.save()

    request.session["carrito"] = {}

    return redirect("mis_prestamos")


# ======================================
# HISTORIAL DE PRÉSTAMOS
# ======================================

@login_required
def mis_prestamos(request):

    prestamos = Prestamo.objects.filter(
        usuario=request.user
    ).order_by("-id")

    return render(
        request,
        "prestamos/mis_prestamos.html",
        {
            "prestamos": prestamos
        }
    )


# ======================================
# DEVOLVER LIBRO
# ======================================

@login_required
def devolver_libro(request, prestamo_id):

    prestamo = Prestamo.objects.get(
        id=prestamo_id
    )

    prestamo.estado = "Devuelto"

    prestamo.save()

    return redirect("mis_prestamos")


# ======================================
# REPORTE GENERAL
# ======================================

@login_required
def reporte_prestamos(request):

    prestamos = Prestamo.objects.all().order_by("-id")

    cantidad_total = prestamos.count()

    prestados = prestamos.filter(
        estado="Prestado"
    ).count()

    devueltos = prestamos.filter(
        estado="Devuelto"
    ).count()

    retrasados = prestamos.filter(
        estado="Retrasado"
    ).count()

    return render(
        request,
        "prestamos/reporte_prestamos.html",
        {
            "prestamos": prestamos,
            "cantidad_total": cantidad_total,
            "prestados": prestados,
            "devueltos": devueltos,
            "retrasados": retrasados,
        }
    )


# ======================================
# PÁGINA DE INICIO
# ======================================

@login_required
def inicio(request):

    total_libros = Libro.objects.count()

    total_prestamos = Prestamo.objects.count()

    return render(
        request,
        "inicio.html",
        {
            "total_libros": total_libros,
            "total_prestamos": total_prestamos,
        }
    )
