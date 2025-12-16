#generador_xml.py
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

class GeneradorXML:

    def __init__(self, controlador_centros):
        self.controlador_centros = controlador_centros

    def generar_salida(self, ruta_salida):
        # genera el archivo xml con las estadisticas
        try:
            # creo el elemento raiz
            root = ET.Element("resultadoCloudSync")

            # pongo el timestamp
            timestamp = ET.SubElement(root, "timestamp")
            tiempo_actual = datetime.now().isoformat()
            timestamp.text = tiempo_actual

            # agrego estado de los centros
            self._agregar_estado_centros(root)

            # agrego las estadisticas generales
            self._agregar_estadisticas(root)

            # formateo el xml para que se vea bonito
            xml_str = minidom.parseString(ET.tostring(root, encoding="unicode")).toprettyxml(indent="  ")
            
            # guardo en el archivo
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                f.write(xml_str)
                
            return True, "Archivo XML generado exitosamente"
        except Exception as e:
            mensaje_error = f"Error al generar XML: {str(e)}"
            return False, mensaje_error

    def _agregar_estado_centros(self, root):
        # agrego la informacion de cada centro
        estado_centros = ET.SubElement(root, "estadoCentros")
        
        # obtengo la lista de centros
        centros = self.controlador_centros.listar_todos()
        actual = centros.primero
        
        # recorro todos los centros
        while actual is not None:
            # creo el elemento del centro
            centro_elem = ET.SubElement(estado_centros, "centro", id=actual.id)
            
            # agrego el nombre
            nombre = ET.SubElement(centro_elem, "nombre")
            nombre.text = actual.nombre

            # agrego recursos
            recursos = ET.SubElement(centro_elem, "recursos")

            # informacion de cpu
            cpu_total = ET.SubElement(recursos, "cpuTotal")
            cpu_total.text = str(actual.cpu_total)
            
            cpu_disp = ET.SubElement(recursos, "cpuDisponible")
            cpu_disp.text = str(actual.cpu_disponible)
            
            cpu_util = ET.SubElement(recursos, "cpuUtilizacion")
            utilizacion_cpu = actual.calcular_utilizacion_cpu()
            cpu_util.text = f"{utilizacion_cpu:.2f}%"

            # informacion de ram
            ram_total = ET.SubElement(recursos, "ramTotal")
            ram_total.text = str(actual.ram_total)
            
            ram_disp = ET.SubElement(recursos, "ramDisponible")
            ram_disp.text = str(actual.ram_disponible)
            
            ram_util = ET.SubElement(recursos, "ramUtilizacion")
            utilizacion_ram = actual.calcular_utilizacion_ram()
            ram_util.text = f"{utilizacion_ram:.2f}%"

            # cantidad de vms
            cant_vms = ET.SubElement(centro_elem, "cantidadVms")
            cant_vms.text = str(actual.vms.tamanio)

            # ahora cuento los contenedores
            total_contenedores = 0
            vm_actual = actual.vms.primero
            while vm_actual is not None:
                num_contenedores = vm_actual.dato.contenedores.tamanio
                total_contenedores += num_contenedores
                vm_actual = vm_actual.siguiente

            cant_cont = ET.SubElement(centro_elem, "cantidadContenedores")
            cant_cont.text = str(total_contenedores)

            # paso al siguiente centro
            actual = actual.siguiente

    def _agregar_estadisticas(self, root):
        # agrego estadisticas totales del sistema
        estadisticas = ET.SubElement(root, "estadisticas")
        
        # inicializo contadores
        total_vms = 0
        total_contenedores = 0
        
        # obtengo centros
        centros = self.controlador_centros.listar_todos()
        actual = centros.primero
        
        # recorro para contar
        while actual is not None:
            # sumo las vms de este centro
            total_vms += actual.vms.tamanio
            
            # ahora cuento contenedores de cada vm
            vm_actual = actual.vms.primero
            while vm_actual is not None:
                num_cont = vm_actual.dato.contenedores.tamanio
                total_contenedores += num_cont
                vm_actual = vm_actual.siguiente
                
            # siguiente centro
            actual = actual.siguiente

        # agrego el total de vms
        total_vms_elem = ET.SubElement(estadisticas, "vmsTotales")
        total_vms_elem.text = str(total_vms)

        # agrego el total de contenedores
        total_contenedores_elem = ET.SubElement(estadisticas, "contenedoresTotales")
        total_contenedores_elem.text = str(total_contenedores)