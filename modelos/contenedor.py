class Contenedor:

    def __init__(self, id_contenedor, nombre, imagen, cpu_porcentaje, ram_mb, puerto):
        self.id = id_contenedor
        self.nombre = nombre
        self.imagen = imagen

        self.cpu_porcentaje = cpu_porcentaje
        self.ram_mb = ram_mb
        self.puerto = puerto

        self.estado = "Activo"

    def mostrar_informacion(self):
        print(f"\nID: {self.id}")
        print(f"Nombre: {self.nombre}")
        print(f"Imagen: {self.imagen}")
        print(f"CPU (%): {self.cpu_porcentaje}")
        print(f"RAM (MB): {self.ram_mb}")
        print(f"Puerto: {self.puerto}")
        print(f"Estado: {self.estado}")

    def __str__(self):
        return f"Contenedor[{self.id}] - {self.nombre} ({self.estado})"

    def pausar(self):
        if self.estado == "Activo":
            self.estado = "Pausado"
            return True, "Contenedor pausado"
        return False, "No se puede pausar el contenedor en su estado actual"

    def reiniciar(self):
        if self.estado in ["Activo", "Pausado"]:
            self.estado = "Reiniciando"
            self.estado = "Activo"
            return True, "Contenedor reiniciado"
        return False, "No se puede reiniciar el contenedor"

    def detener(self):
        if self.estado != "Detenido":
            self.estado = "Detenido"
            return True, "Contenedor detenido"
        return False, "El contenedor ya está detenido"

    def activar(self):
        if self.estado == "Detenido":
            self.estado = "Activo"
            return True, "Contenedor activado"
        return False, "El contenedor no puede activarse"

    def obtener_cpu_porcentaje(self):
        return self.cpu_porcentaje

    def obtener_ram_mb(self):
        return self.ram_mb
