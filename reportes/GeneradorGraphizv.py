class GeneradorGraphviz:
    """Genera reportes con Graphviz"""
    
    def __init__(self, g_centros, g_vms):
        self.g_centros = g_centros
        self.g_vms = g_vms
    
    def reporte_centros(self, ruta="reportes/centros.dot"):
        try:
            dot = []
            dot.append("digraph CentrosDatos {")
            dot.append('  rankdir=TB;')
            dot.append('  node [shape=box, style="rounded,filled", fillcolor=lightblue];')
            dot.append('  graph [bgcolor=white];')
            dot.append('')
            dot.append('  titulo [label="CENTROS DE DATOS\\nCloudSync", shape=note, fillcolor=gold, fontsize=16];')
            dot.append('')
            
            temp = self.g_centros.centros.cabeza
            while temp is not None:
                centro = temp.dato
                label = f"{centro.id}\\n{centro.nombre}\\n"
                label += f"CPU: {centro.cpu_disp}/{centro.cpu_total}\\n"
                label += f"RAM: {centro.ram_disp}/{centro.ram_total} GB\\n"
                label += f"VMs: {centro.vms.obtener_tamanio()}"
                
                dot.append(f'  {centro.id} [label="{label}"];')
                dot.append(f'  titulo -> {centro.id};')
                
                temp = temp.siguiente
            
            dot.append("}")
            
            with open(ruta, 'w') as f:
                f.write('\n'.join(dot))
            
            return True, f"Reporte: {ruta}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def reporte_vms_centro(self, id_centro, ruta="reportes/vms_centro.dot"):
        try:
            centro = self.g_centros.obtener_centro(id_centro)
            if centro is None:
                return False, f"Centro {id_centro} no existe"
            
            dot = []
            dot.append("digraph VMsCentro {")
            dot.append('  rankdir=TB;')
            dot.append('  node [shape=box, style="rounded,filled"];')
            dot.append('')
            
            dot.append(f'  centro [label="{centro.id}\\n{centro.nombre}", fillcolor=lightblue, fontsize=14];')
            dot.append('')
            
            temp_vm = centro.vms.cabeza
            while temp_vm is not None:
                vm = temp_vm.dato
                label = f"{vm.id}\\n{vm.nombre}\\n{vm.so}\\n"
                label += f"CPU: {vm.cpu_disponible:.1f}/{vm.cpu_asig}\\n"
                label += f"RAM: {vm.ram_disponible:.1f}/{vm.ram_asig} GB"
                
                dot.append(f'  {vm.id} [label="{label}", fillcolor=lightgreen];')
                dot.append(f'  centro -> {vm.id};')
                
                temp_vm = temp_vm.siguiente
            
            dot.append("}")
            
            with open(ruta, 'w') as f:
                f.write('\n'.join(dot))
            
            return True, f"Reporte: {ruta}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def reporte_contenedores_vm(self, id_vm, ruta="reportes/contenedores_vm.dot"):
        try:
            vm = self.g_vms.obtener_vm(id_vm)
            if vm is None:
                return False, f"VM {id_vm} no existe"
            
            dot = []
            dot.append("digraph ContenedoresVM {")
            dot.append('  rankdir=TB;')
            dot.append('  node [shape=box, style="rounded,filled"];')
            dot.append('')
            
            dot.append(f'  vm [label="{vm.id}\\n{vm.nombre}", fillcolor=lightgreen, fontsize=14];')
            dot.append('')
            
            temp_cont = vm.contenedores.cabeza
            while temp_cont is not None:
                cont = temp_cont.dato
                label = f"{cont.id}\\n{cont.nombre}\\n{cont.imagen}\\n"
                label += f"CPU: {cont.cpu_pct}%\\nRAM: {cont.ram_mb} MB\\n"
                label += f"Estado: {cont.estado}"
                
                color = "lightyellow"
                if cont.estado == "Activo":
                    color = "lightgreen"
                elif cont.estado == "Pausado":
                    color = "orange"
                elif cont.estado == "Detenido":
                    color = "lightcoral"
                
                dot.append(f'  {cont.id} [label="{label}", fillcolor={color}];')
                dot.append(f'  vm -> {cont.id};')
                
                temp_cont = temp_cont.siguiente
            
            dot.append("}")
            
            with open(ruta, 'w') as f:
                f.write('\n'.join(dot))
            
            return True, f"Reporte: {ruta}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def reporte_cola_solicitudes(self, cola, ruta="reportes/cola_solicitudes.dot"):
        try:
            dot = []
            dot.append("digraph ColaSolicitudes {")
            dot.append('  rankdir=LR;')
            dot.append('  node [shape=box, style="rounded,filled"];')
            dot.append('')
            dot.append('  inicio [label="COLA", shape=ellipse, fillcolor=gold];')
            dot.append('')
            
            temp = cola.frente
            anterior = "inicio"
            contador = 1
            
            while temp is not None:
                sol = temp.dato
                label = f"#{contador}\\n{sol.id}\\n{sol.cliente}\\n"
                label += f"Tipo: {sol.tipo}\\nPrioridad: {sol.prioridad}"
                
                color = "lightgreen"
                if sol.prioridad >= 8:
                    color = "red"
                elif sol.prioridad >= 5:
                    color = "orange"
                
                dot.append(f'  sol{contador} [label="{label}", fillcolor={color}];')
                dot.append(f'  {anterior} -> sol{contador};')
                
                anterior = f"sol{contador}"
                temp = temp.siguiente
                contador += 1
            
            if cola.vacia():
                dot.append('  vacio [label="(vacia)", shape=plaintext];')
                dot.append('  inicio -> vacio;')
            
            dot.append("}")
            
            with open(ruta, 'w') as f:
                f.write('\n'.join(dot))
            
            return True, f"Reporte: {ruta}"
        except Exception as e:
            return False, f"Error: {str(e)}"
