class Contenedor:
    
    def __init__(self, identificador, nombre_cont, imagen_docker, cpu_porcentaje, ram_megabytes, puerto_red):
        self.id = identificador
        self.nombre = nombre_cont
        self.imagen = imagen_docker
        self.cpu_pct = int(cpu_porcentaje)
        self.ram_mb = int(ram_megabytes)
        self.puerto = int(puerto_red)
        self.estado = "Activo"  
        # incia activo
        self.siguiente = None
    
    def modificar_estado(self, estado_nuevo):
        # lista de estados
        estados_permitidos = ["Activo", "Pausado", "Detenido", "Reiniciando"]
        
        # verifico si el estado es valido
        if estado_nuevo in estados_permitidos:
            self.estado = estado_nuevo
            return True
        else:
            return False
    
    def mostrar(self):
        print(f"\n{'='*60}")
        print(f"ID Contenedor: {self.id}")
        print(f"Nombre: {self.nombre}")
        print(f"Imagen: {self.imagen}")
        print(f"Estado: {self.estado}")
        print(f"Recursos:")
        print(f"  CPU: {self.cpu_pct}%")
        print(f"  RAM: {self.ram_mb} MB")
        print(f"Puerto: {self.puerto}")
        print(f"{'='*60}")