#centros_datos.py
from estructuras.Lista_enlazada import ListaSimple

class CentroDatos:
    
    def __init__(self, identificador, nombre_centro, pais, ciudad, cpu, ram, almacenamiento):
        self.id = identificador
        self.nombre = nombre_centro
        self.pais = pais
        self.ciudad = ciudad
        
        self.cpu_total = int(cpu)
        self.ram_total = int(ram)
        self.almacenamiento_total = int(almacenamiento)
        
        self.cpu_disp = int(cpu)
        self.ram_disp = int(ram)
        self.almacen_disp = int(almacenamiento)
        
        self.cpu_disponible = int(cpu)
        self.ram_disponible = int(ram)
        
        self.vms = ListaSimple()
        self.siguiente = None
    
    def uso_cpu_porcentaje(self):
        if self.cpu_total == 0:
            return 0.0
        
        usado = self.cpu_total - self.cpu_disp
        porcentaje = (usado * 100.0) / self.cpu_total
        return porcentaje
    
    def calcular_utilizacion_cpu(self):
        return self.uso_cpu_porcentaje()
    
    def uso_ram_porcentaje(self):
        if self.ram_total == 0:
            return 0.0
        
        usado = self.ram_total - self.ram_disp
        porcentaje = (usado * 100.0) / self.ram_total
        return porcentaje
    
    def calcular_utilizacion_ram(self):
        return self.uso_ram_porcentaje()
    
    def hay_recursos_suficientes(self, cpu_req, ram_req, almac_req):
        tiene_cpu = self.cpu_disp >= cpu_req
        tiene_ram = self.ram_disp >= ram_req
        tiene_almacen = self.almacen_disp >= almac_req
        
        if tiene_cpu and tiene_ram and tiene_almacen:
            return True
        else:
            return False
    
    def usar_recursos(self, cpu, ram, almac):
        self.cpu_disp -= cpu
        self.ram_disp -= ram
        self.almacen_disp -= almac
        
        self.cpu_disponible = self.cpu_disp
        self.ram_disponible = self.ram_disp
    
    def devolver_recursos(self, cpu, ram, almac):
        self.cpu_disp += cpu
        self.ram_disp += ram
        self.almacen_disp += almac
        
        self.cpu_disponible = self.cpu_disp
        self.ram_disponible = self.ram_disp
    
    def mostrar(self):
        separador = "=" * 65
        print("")
        print(separador)
        texto_id = "ID Centro: " + self.id
        print(texto_id)
        texto_nombre = "Nombre: " + self.nombre
        print(texto_nombre)
        texto_ubicacion = "Ubicacion: " + self.ciudad + ", " + self.pais
        print(texto_ubicacion)
        
        print("\nRECURSOS:")
        
        pct_cpu = self.uso_cpu_porcentaje()
        cpu_disp_str = str(self.cpu_disp)
        cpu_total_str = str(self.cpu_total)
        pct_cpu_str = f"{pct_cpu:.2f}"
        texto_cpu = "  CPU: " + cpu_disp_str + "/" + cpu_total_str + " disponibles (" + pct_cpu_str + "% usado)"
        print(texto_cpu)
        
        pct_ram = self.uso_ram_porcentaje()
        ram_disp_str = str(self.ram_disp)
        ram_total_str = str(self.ram_total)
        pct_ram_str = f"{pct_ram:.2f}"
        texto_ram = "  RAM: " + ram_disp_str + "/" + ram_total_str + " GB disponibles (" + pct_ram_str + "% usado)"
        print(texto_ram)
        
        almacen_disp_str = str(self.almacen_disp)
        almacen_total_str = str(self.almacenamiento_total)
        texto_almacen = "  Almacenamiento: " + almacen_disp_str + "/" + almacen_total_str + " GB"
        print(texto_almacen)
        
        num_vms = self.vms.obtener_tamanio()
        num_vms_str = str(num_vms)
        texto_vms = "VMs activas: " + num_vms_str
        print(texto_vms)
        print(separador)