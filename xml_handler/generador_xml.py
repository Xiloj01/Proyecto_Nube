# generador_xml.py
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

class GeneradorXML:
    def __init__(self, controlador_centros):
        self.controlador_centros = controlador_centros

    def generar_salida(self, ruta_salida):
        try:
            root = ET.Element("resultadoCloudSync")
            timestamp = ET.SubElement(root, "timestamp")
            tiempo_actual = datetime.now().isoformat()
            timestamp.text = tiempo_actual

            self._agregar_estado_centros(root)
            self._agregar_estadisticas(root)

            xml_str = minidom.parseString(ET.tostring(root, encoding="unicode")).toprettyxml(indent="  ")
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                f.write(xml_str)
            return True, "Archivo XML generado exitosamente"
        except Exception as e:
            mensaje_error = f"Error al generar XML: {str(e)}"
            return False, mensaje_error

    def _agregar_estado_centros(self, root):
        estado_centros = ET.SubElement(root, "estadoCentros")
        centros = self.controlador_centros.listar_todos()
        actual = centros.cabeza  # ← Usa 'cabeza', no 'primero'
        while actual is not None:
            centro = actual.dato  # ← El objeto real está en .dato

            centro_elem = ET.SubElement(estado_centros, "centro", id=centro.id)
            nombre = ET.SubElement(centro_elem, "nombre")
            nombre.text = centro.nombre

            recursos = ET.SubElement(centro_elem, "recursos")

            cpu_total = ET.SubElement(recursos, "cpuTotal")
            cpu_total.text = str(centro.cpu_total)
            cpu_disp = ET.SubElement(recursos, "cpuDisponible")
            cpu_disp.text = str(centro.cpu_disponible)
            cpu_util = ET.SubElement(recursos, "cpuUtilizacion")
            utilizacion_cpu = centro.calcular_utilizacion_cpu()
            cpu_util.text = f"{utilizacion_cpu:.2f}%"

            ram_total = ET.SubElement(recursos, "ramTotal")
            ram_total.text = str(centro.ram_total)
            ram_disp = ET.SubElement(recursos, "ramDisponible")
            ram_disp.text = str(centro.ram_disponible)
            ram_util = ET.SubElement(recursos, "ramUtilizacion")
            utilizacion_ram = centro.calcular_utilizacion_ram()
            ram_util.text = f"{utilizacion_ram:.2f}%"

            cant_vms = ET.SubElement(centro_elem, "cantidadVms")
            cant_vms.text = str(centro.vms.obtener_tamanio())

            # Contar contenedores en todas las VMs de este centro
            total_contenedores = 0
            vm_actual = centro.vms.cabeza
            while vm_actual is not None:
                total_contenedores += vm_actual.dato.contenedores.obtener_tamanio()
                vm_actual = vm_actual.siguiente

            cant_cont = ET.SubElement(centro_elem, "cantidadContenedores")
            cant_cont.text = str(total_contenedores)

            actual = actual.siguiente

    def _agregar_estadisticas(self, root):
        estadisticas = ET.SubElement(root, "estadisticas")
        total_vms = 0
        total_contenedores = 0

        centros = self.controlador_centros.listar_todos()
        actual = centros.cabeza
        while actual is not None:
            centro = actual.dato
            total_vms += centro.vms.obtener_tamanio()

            vm_actual = centro.vms.cabeza
            while vm_actual is not None:
                total_contenedores += vm_actual.dato.contenedores.obtener_tamanio()
                vm_actual = vm_actual.siguiente

            actual = actual.siguiente

        vms_elem = ET.SubElement(estadisticas, "vmsTotales")
        vms_elem.text = str(total_vms)

        cont_elem = ET.SubElement(estadisticas, "contenedoresTotales")
        cont_elem.text = str(total_contenedores)