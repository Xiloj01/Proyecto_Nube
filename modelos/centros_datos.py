from estructuras.listasimple import ListaSimple

class CentroDatos:
    """Modelo de centro de datos"""
    
    def __init__(self, identificador, nombre_centro, pais, ciudad, cpu, ram, almacenamiento):
        self.id = identificador
        self.nombre = nombre_centro
        self.pais = pais
        self.ciudad = ciudad
        # totales
        self.cpu_total = int(cpu)
        self.ram_total = int(ram)
        self.almacenamiento_total = int(almacenamiento)
        # disponibles
        self.cpu_disp = int(cpu)
        self.ram_disp = int(ram)
        self.almacen_disp = int(almacenamiento)
        # VMs
        self.vms = ListaSimple()
        self.siguiente = None
    
    def uso_cpu_porcentaje(self):
        if self.cpu_total == 0:
            return 0.0
        usado = self.cpu_total - self.cpu_disp
        return (usado * 100.0) / self.cpu_total
    
    def uso_ram_porcentaje(self):
        if self.ram_total == 0:
            return 0.0
        usado = self.ram_total - self.ram_disp
        return (usado * 100.0) / self.ram_total
    
    def hay_recursos_suficientes(self, cpu_req, ram_req, almac_req):
        return (self.cpu_disp >= cpu_req and 
                self.ram_disp >= ram_req and 
                self.almacen_disp >= almac_req)
    
    def usar_recursos(self, cpu, ram, almac):
        self.cpu_disp -= cpu
        self.ram_disp -= ram
        self.almacen_disp -= almac
    
    def devolver_recursos(self, cpu, ram, almac):
        self.cpu_disp += cpu
        self.ram_disp += ram
        self.almacen_disp += almac
    
    def mostrar(self):
        print(f"\n{'='*65}")
        print(f"ID Centro: {self.id}")
        print(f"Nombre: {self.nombre}")
        print(f"Ubicacion: {self.ciudad}, {self.pais}")
        print(f"\nRECURSOS:")
        print(f"  CPU: {self.cpu_disp}/{self.cpu_total} disponibles ({self.uso_cpu_porcentaje():.2f}% usado)")
        print(f"  RAM: {self.ram_disp}/{self.ram_total} GB disponibles ({self.uso_ram_porcentaje():.2f}% usado)")
        print(f"  Almacenamiento: {self.almacen_disp}/{self.almacenamiento_total} GB")
        print(f"VMs activas: {self.vms.obtener_tamanio()}")
        print(f"{'='*65}")

