import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

class GeneradorXML:
    """Genera archivos XML de salida con estadísticas"""

    def __init__(self, controlador_centros):
        self.controlador_centros = controlador_centros

    def generar_salida(self, ruta_salida):
        """Genera el archivo XML de salida"""
        try:
            root = ET.Element("resultadoCloudSync")

            # Timestamp
            timestamp = ET.SubElement(root, "timestamp")
            timestamp.text = datetime.now().isoformat()

            # Estado de centros
            self._agregar_estado_centros(root)

            # Estadísticas generales
            self._agregar_estadisticas(root)

            # Formatear y guardar
            xml_str = minidom.parseString(ET.tostring(root, encoding="unicode")).toprettyxml(indent="  ")
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                f.write(xml_str)
            return True, "Archivo XML generado exitosamente"
        except Exception as e:
            return False, f"Error al generar XML: {str(e)}"

    def _agregar_estado_centros(self, root):
        """Agrega información de estado de los centros"""
        estado_centros = ET.SubElement(root, "estadoCentros")
        centros = self.controlador_centros.listar_todos()
        actual = centros.primero
        while actual is not None:
            centro_elem = ET.SubElement(estado_centros, "centro", id=actual.id)
            nombre = ET.SubElement(centro_elem, "nombre")
            nombre.text = actual.nombre

            recursos = ET.SubElement(centro_elem, "recursos")

            cpu_total = ET.SubElement(recursos, "cpuTotal")
            cpu_total.text = str(actual.cpu_total)
            cpu_disp = ET.SubElement(recursos, "cpuDisponible")
            cpu_disp.text = str(actual.cpu_disponible)
            cpu_util = ET.SubElement(recursos, "cpuUtilizacion")
            cpu_util.text = f"{actual.calcular_utilizacion_cpu():.2f}%"

            ram_total = ET.SubElement(recursos, "ramTotal")
            ram_total.text = str(actual.ram_total)
            ram_disp = ET.SubElement(recursos, "ramDisponible")
            ram_disp.text = str(actual.ram_disponible)
            ram_util = ET.SubElement(recursos, "ramUtilizacion")
            ram_util.text = f"{actual.calcular_utilizacion_ram():.2f}%"

            cant_vms = ET.SubElement(centro_elem, "cantidadVms")
            cant_vms.text = str(actual.vms.tamanio)

            # Contar contenedores
            total_contenedores = 0
            vm_actual = actual.vms.primero
            while vm_actual is not None:
                total_contenedores += vm_actual.dato.contenedores.tamanio
                vm_actual = vm_actual.siguiente

            cant_cont = ET.SubElement(centro_elem, "cantidadContenedores")
            cant_cont.text = str(total_contenedores)

            actual = actual.siguiente

    def _agregar_estadisticas(self, root):
        """Agrega estadísticas generales"""
        estadisticas = ET.SubElement(root, "estadisticas")
        total_vms = 0
        total_contenedores = 0
        centros = self.controlador_centros.listar_todos()
        actual = centros.primero
        while actual is not None:
            total_vms += actual.vms.tamanio
            vm_actual = actual.vms.primero
            while vm_actual is not None:
                total_contenedores += vm_actual.dato.contenedores.tamanio
                vm_actual = vm_actual.siguiente
            actual = actual.siguiente

        total_vms_elem = ET.SubElement(estadisticas, "vmsTotales")
        total_vms_elem.text = str(total_vms)

        total_contenedores_elem = ET.SubElement(estadisticas, "contenedoresTotales")
        total_contenedores_elem.text = str(total_contenedores)
