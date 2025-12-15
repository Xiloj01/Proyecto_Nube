#centros_datos.py
from estructuras.listasimple import ListaSimple

class CentroDatos:
    
    def __init__(self, identificador, nombre_centro, pais, ciudad, cpu, ram, almacenamiento):
        self.id = identificador
        self.nombre = nombre_centro
        self.pais = pais
        self.ciudad = ciudad
        
        # guardo los recursos totales del centro
        self.cpu_total = int(cpu)
        self.ram_total = int(ram)
        self.almacenamiento_total = int(almacenamiento)
        
        # al principio todo esta disponible
        self.cpu_disp = int(cpu)
        self.ram_disp = int(ram)
        self.almacen_disp = int(almacenamiento)
        
        # lista donde guardo las vms de este centro
        self.vms = ListaSimple()
        self.siguiente = None  #para cuando este en una lista enlazada
    
    def uso_cpu_porcentaje(self):
        # calculo cuanto cpu se esta usando en porcentaje
        if self.cpu_total == 0:
            return 0.0
        
        usado = self.cpu_total - self.cpu_disp
        porcentaje = (usado * 100.0) / self.cpu_total
        return porcentaje
    
    def uso_ram_porcentaje(self):
        # lo mismo pero para ram
        if self.ram_total == 0:
            return 0.0
        
        usado = self.ram_total - self.ram_disp
        porcentaje = (usado * 100.0) / self.ram_total
        return porcentaje
    
    def hay_recursos_suficientes(self, cpu_req, ram_req, almac_req):
        # verifico si tengo suficientes recursos para lo que me piden
        tiene_cpu = self.cpu_disp >= cpu_req
        tiene_ram = self.ram_disp >= ram_req
        tiene_almacen = self.almacen_disp >= almac_req
        
        # si tengo todo retorno true
        if tiene_cpu and tiene_ram and tiene_almacen:
            return True
        else:
            return False
    
    def usar_recursos(self, cpu, ram, almac):
        # cuando creo una vm resto los recursos
        self.cpu_disp -= cpu
        self.ram_disp -= ram
        self.almacen_disp -= almac
    
    def devolver_recursos(self, cpu, ram, almac):
        # cuando elimino una vm devuelvo los recursos
        self.cpu_disp += cpu
        self.ram_disp += ram
        self.almacen_disp += almac
    
    def mostrar(self):
        # muestro toda la info del centro
        print(f"\n{'='*65}")
        print(f"ID Centro: {self.id}")
        print(f"Nombre: {self.nombre}")
        print(f"Ubicacion: {self.ciudad}, {self.pais}")
        
        print(f"\nRECURSOS:")
        
        # calculo y muestro cpu
        pct_cpu = self.uso_cpu_porcentaje()
        print(f"  CPU: {self.cpu_disp}/{self.cpu_total} disponibles ({pct_cpu:.2f}% usado)")
        
        # calculo y muestro ram
        pct_ram = self.uso_ram_porcentaje()
        print(f"  RAM: {self.ram_disp}/{self.ram_total} GB disponibles ({pct_ram:.2f}% usado)")
        
        # almacenamiento
        print(f"  Almacenamiento: {self.almacen_disp}/{self.almacenamiento_total} GB")
        
        # cuento cuantas vms tiene
        num_vms = self.vms.obtener_tamanio()
        print(f"VMs activas: {num_vms}")
        print(f"{'='*65}")