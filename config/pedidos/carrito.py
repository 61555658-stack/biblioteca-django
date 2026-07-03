# prestamos/carrito.py

class Carrito:

    def __init__(self, request):

        self.request = request
        self.session = request.session

        carrito = self.session.get("carrito")

        if not carrito:
            carrito = self.session["carrito"] = {}

        self.carrito = carrito

    def agregar(self, libro):

        libro_id = str(libro.id)

        if libro_id not in self.carrito:

            self.carrito[libro_id] = {
                "titulo": libro.titulo,
                "autor": libro.autor,
                "cantidad": 1,
            }

        else:

            self.carrito[libro_id]["cantidad"] += 1

        self.guardar()

    def eliminar(self, libro):

        libro_id = str(libro.id)

        if libro_id in self.carrito:

            del self.carrito[libro_id]

            self.guardar()

    def restar(self, libro):

        libro_id = str(libro.id)

        if libro_id in self.carrito:

            self.carrito[libro_id]["cantidad"] -= 1

            if self.carrito[libro_id]["cantidad"] <= 0:
                self.eliminar(libro)

        self.guardar()

    def limpiar(self):

        self.session["carrito"] = {}
        self.session.modified = True

    def guardar(self):

        self.session["carrito"] = self.carrito
        self.session.modified = True