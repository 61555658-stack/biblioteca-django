from django.db import models
from django.contrib.auth.models import User



# ======================================
# CATEGORÍA
# ======================================

class Categoria(models.Model):

    nombre = models.CharField(
        max_length=100
    )


    def __str__(self):
        return self.nombre



# ======================================
# LIBRO
# ======================================

class Libro(models.Model):

    titulo = models.CharField(
        max_length=100
    )

    autor = models.CharField(
        max_length=100
    )

    stock = models.IntegerField(
        default=0
    )

    activo = models.BooleanField(
        default=True
    )


    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    def __str__(self):

        return self.titulo



# ======================================
# PRÉSTAMO
# ======================================

class Prestamo(models.Model):


    ESTADOS = [

        ('Prestado','Prestado'),

        ('Devuelto','Devuelto'),

        ('Retrasado','Retrasado'),

    ]


    # Estudiante que recibe el préstamo

    estudiante = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    libros = models.ManyToManyField(
        Libro,
        through='DetallePrestamo'
    )


    fecha_prestamo = models.DateField(
        auto_now_add=True
    )


    fecha_devolucion = models.DateField()



    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="Prestado"
    )


    def __str__(self):

        return f"{self.estudiante.username} - {self.fecha_prestamo}"




# ======================================
# DETALLE DEL PRÉSTAMO
# ======================================

class DetallePrestamo(models.Model):


    prestamo = models.ForeignKey(
        Prestamo,
        on_delete=models.CASCADE
    )


    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE
    )


    cantidad = models.IntegerField(
        default=1
    )


    def __str__(self):

        return f"{self.libro.titulo} x {self.cantidad}"