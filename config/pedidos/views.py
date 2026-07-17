# pedidos/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction  # Importación añadida para transacciones seguras
from datetime import date, timedelta

from .carrito import Carrito
from .models import Libro, Prestamo, DetallePrestamo


# ======================================
# BÚSQUEDA Y LISTA DE LIBROS
# ======================================

def lista_libros(request):
    buscar = request.GET.get("buscar", "")

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
# CARRITO DE PRÉSTAMO
# ======================================

def agregar_libro(request, libro_id):
    carrito = Carrito(request)
    libro = get_object_or_404(Libro, id=libro_id)
    carrito.agregar(libro)

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "lista_libros"
        )
    )


def eliminar_libro(request, libro_id):
    carrito = Carrito(request)
    libro = get_object_or_404(Libro, id=libro_id)
    carrito.eliminar(libro)

    return redirect("ver_carrito")


def restar_libro(request, libro_id):
    carrito = Carrito(request)
    libro = get_object_or_404(Libro, id=libro_id)
    carrito.restar(libro)

    return redirect("ver_carrito")


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()

    return redirect("ver_carrito")


# ======================================
# VER SOLICITUD DE PRÉSTAMO
# ======================================

@login_required
def ver_carrito(request):
    carrito = request.session.get("carrito", {})

    estudiantes = User.objects.filter(
        is_staff=False,
        is_superuser=False
    ).order_by("username")

    return render(
        request,
        "carrito.html",
        {
            "carrito": carrito,
            "usuarios": estudiantes
        }
    )


# ======================================
# CONFIRMAR PRÉSTAMO (Optimizado con transacciones)
# ======================================

@login_required
def confirmar_prestamo(request):
    if request.method != "POST":
        return redirect("ver_carrito")

    carrito_sesion = request.session.get("carrito", {})

    if not carrito_sesion:
        messages.error(request, "No existen libros en la solicitud.")
        return redirect("ver_carrito")

    usuario_id = request.POST.get("usuario")

    if not usuario_id:
        messages.error(request, "Debe seleccionar un estudiante.")
        return redirect("ver_carrito")

    usuario = get_object_or_404(User, id=usuario_id)

    # Bloque protegido: Se guarda TODO o NO SE GUARDA NADA si hay un error
    try:
        with transaction.atomic():
            prestamo = Prestamo.objects.create(
                estudiante=usuario,  # <-- CORREGIDO: Guarda al estudiante seleccionado
                fecha_devolucion=date.today() + timedelta(days=7),
                estado="Prestado"
            )

            for key, value in carrito_sesion.items():
                libro = get_object_or_404(Libro, id=key)
                cantidad = value["cantidad"]

                if libro.stock < cantidad:
                    # Cancelará automáticamente toda la transacción del bloque
                    raise ValueError(f"No existe stock para {libro.titulo}")

                DetallePrestamo.objects.create(
                    prestamo=prestamo,
                    libro=libro,
                    cantidad=cantidad
                )

                libro.stock -= cantidad
                libro.save()

    except ValueError as e:
        messages.error(request, str(e))
        return redirect("ver_carrito")

    # Si todo el bloque fue exitoso, se limpia el carrito
    request.session["carrito"] = {}

    messages.success(request, "Préstamo registrado correctamente.")
    return redirect("reporte_prestamos")


# ======================================
# MIS PRÉSTAMOS
# ======================================

@login_required
def mis_prestamos(request):
    # Si el usuario actual es administrador/staff, no debe ver préstamos como suyos
    if request.user.is_staff or request.user.is_superuser:
        prestamos = Prestamo.objects.none()
    else:
        # Si es un estudiante, ve únicamente sus registros asignados
        prestamos = Prestamo.objects.filter(
            estudiante=request.user
        ).order_by("-id")

    return render(
        request,
        "prestamos/mis_prestamos.html",
        {
            "prestamos": prestamos
        }
    )


# ======================================
# DETALLE DEL PRÉSTAMO
# ======================================

@login_required
def detalle_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    detalles = DetallePrestamo.objects.filter(prestamo=prestamo)

    return render(
        request,
        "prestamos/detalle_prestamo.html",
        {
            "prestamo": prestamo,
            "detalles": detalles
        }
    )


# ======================================
# DEVOLVER LIBROS
# ======================================

@login_required
def devolver_libro(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)

    if prestamo.estado == "Devuelto":
        messages.warning(request, "Este préstamo ya fue devuelto.")
        return redirect("reporte_prestamos")

    detalles = DetallePrestamo.objects.filter(prestamo=prestamo)

    for detalle in detalles:
        libro = detalle.libro
        libro.stock += detalle.cantidad
        libro.save()

    prestamo.estado = "Devuelto"
    prestamo.save()

    messages.success(request, "Libro devuelto correctamente.")
    return redirect("reporte_prestamos")


# ======================================
# REPORTE GENERAL
# ======================================

@login_required
def reporte_prestamos(request):
    prestamos = Prestamo.objects.all().order_by("-id")

    cantidad_total = prestamos.count()
    prestados = prestamos.filter(estado="Prestado").count()
    devueltos = prestamos.filter(estado="Devuelto").count()
    retrasados = prestamos.filter(estado="Retrasado").count()

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
# INICIO
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