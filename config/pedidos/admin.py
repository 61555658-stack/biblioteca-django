from django.contrib import admin
from .models import Categoria, Libro, Prestamo, DetallePrestamo

admin.site.register(Categoria)
admin.site.register(Libro)
admin.site.register(Prestamo)
admin.site.register(DetallePrestamo)


