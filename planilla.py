import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Planilla de Aprobados", layout="wide")

# Código HTML, CSS y JavaScript con BUSCADOR
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 p-4 font-sans text-slate-900">
    <div class="max-w-6xl mx-auto">
        <h1 class="text-4xl font-extrabold text-center text-slate-800 mb-8 uppercase tracking-wider border-b-4 border-blue-600 pb-4">
            Planilla de aprobados
        </h1>

        <div class="bg-white p-6 rounded-xl shadow-md mb-8 border border-slate-200">
            <h2 class="text-xl font-semibold mb-6 text-blue-700 flex items-center">
                <span class="mr-2">➕</span> Nuevo Registro
            </h2>
            <form id="presupuestoForm" class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <input type="text" id="cliente" required placeholder="Nombre del Cliente" class="border-gray-300 border rounded-lg p-2 outline-none focus:ring-2 focus:ring-blue-500">
                <input type="text" id="vendedor" required placeholder="Vendedor" class="border-gray-300 border rounded-lg p-2 outline-none focus:ring-2 focus:ring-blue-500">
                <input type="text" id="numP" required placeholder="N° Presupuesto" class="border-gray-300 border rounded-lg p-2 outline-none focus:ring-2 focus:ring-blue-500">
                <div class="flex flex-col"><label class="text-[10px] font-bold text-gray-400 ml-1">FECHA CREACIÓN</label><input type="date" id="fechaC" required class="border-gray-300 border rounded-lg p-2"></div>
                <div class="flex flex-col"><label class="text-[10px] font-bold text-gray-400 ml-1">FECHA APROBACIÓN</label><input type="date" id="fechaA" required class="border-gray-300 border rounded-lg p-2"></div>
                <input type="number" id="monto" step="0.01" required placeholder="Monto ($)" class="border-gray-300 border rounded-lg p-2 outline-none focus:ring-2 focus:ring-blue-500">
                <div class="flex items-center md:col-span-1">
                    <input type="checkbox" id="esCorp" class="h-5 w-5 text-blue-600">
                    <label for="esCorp" class="ml-2 text-sm font-bold text-gray-600 cursor-pointer">Cliente Corporativo</label>
                </div>
                <div class="md:col-span-2">
                    <button type="submit" class="w-full bg-blue-600 text-white font-bold py-2 rounded-lg hover:bg-blue-700 shadow-lg active:scale-95 transition-all">
                        Cargar a la Planilla
                    </button>
                </div>
            </form>
        </div>

        <div class="flex flex-col md:flex-row gap-4 mb-4 items-center justify-between bg-blue-50 p-4 rounded-xl border border-blue-100">
            <div class="relative w-full md:w-2/3">
                <span class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-blue-400">🔍</span>
                <input type="text" id="buscador" onkeyup="filtrarTabla()" placeholder="Buscar por cliente, vendedor, número de ppto o fecha..." 
                    class="block w-full pl-10 pr-3 py-3 border border-blue-200 rounded-xl leading-5 bg-white placeholder-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-500 sm:text-sm">
            </div>
            <button onclick="descargarCSV()" class="w-full md:w-auto bg-emerald-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-emerald-700 flex items-center justify-center shadow-md transition-all">
                📥 Descargar CSV
            </button>
        </div>

        <div class="bg-white rounded-xl shadow-xl overflow-hidden border border-slate-200">
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200 text-left" id="miTabla">
                    <thead class="bg-slate-800 text-white">
                        <tr>
                            <th class="px-6 py-4 text-xs font-bold uppercase tracking-wider">Cliente</th>
                            <th class="px-6 py-4 text-xs font-bold uppercase tracking-wider">N° Presup.</th>
                            <th class="px-6 py-4 text-xs font-bold uppercase tracking-wider">Vendedor</th>
                            <th class="px-6 py-4 text-xs font-bold uppercase tracking-wider text-center">Fechas</th>
                            <th class="px-6 py-4 text-xs font-bold uppercase tracking-wider">Monto</th>
                            <th class="px-6 py-4 text-xs font-bold uppercase tracking-wider text-center">Corp.</th>
                            <th class="px-6 py-4 text-xs font-bold uppercase tracking-wider text-center">Acción</th>
                        </tr>
                    </thead>
                    <tbody id="tablaCuerpo" class="divide-y divide-gray-200 bg-white">
                        </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('presupuestoForm');
        const tabla = document.getElementById('tablaCuerpo');
        const inputBuscador = document.getElementById('buscador');

        function mostrarTabla(filtro = "") {
            const datos = JSON.parse(localStorage.getItem('presupuestos')) || [];
            
            // Filtrar los datos según el texto del buscador
            const datosFiltrados = datos.filter(item => {
                const busqueda = filtro.toLowerCase();
                return item.cliente.toLowerCase().includes(busqueda) ||
                       item.vendedor.toLowerCase().includes(busqueda) ||
                       item.numP.toLowerCase().includes(busqueda) ||
                       item.fechaA.includes(busqueda) ||
                       item.fechaC.includes(busqueda);
            });

            if (datosFiltrados.length === 0) {
                tabla.innerHTML = '<tr><td colspan="7" class="px-6 py-10 text-center text-gray-400 italic">No se encontraron registros</td></tr>';
                return;
            }

            tabla.innerHTML = datosFiltrados.map((item, index) => {
                // Buscamos el index original para borrar correctamente si está filtrado
                const indexOriginal = datos.findIndex(d => d.timestamp === item.timestamp);
                
                return `
                <tr class="hover:bg-blue-50/50 transition-colors">
                    <td class="px-6 py-4 text-sm font-semibold text-gray-900">${item.cliente}</td>
                    <td class="px-6 py-4 text-sm text-gray-600">${item.numP}</td>
                    <td class="px-6 py-4 text-sm text-gray-600">${item.vendedor}</td>
                    <td class="px-6 py-4 text-xs text-gray-500 text-center">
                        <div class="font-bold">Aprob: ${item.fechaA}</div>
                        <div class="text-[10px]">Cread: ${item.fechaC}</div>
                    </td>
                    <td class="px-6 py-4 text-sm font-bold text-emerald-600">$${Number(item.monto).toLocaleString('es-AR')}</td>
                    <td class="px-6 py-4 text-center text-lg">${item.corp ? '✅' : '❌'}</td>
                    <td class="px-6 py-4 text-center">
                        <button onclick="borrarUno(${indexOriginal})" class="p-2 hover:bg-red-50 rounded-full text-red-500 transition-colors">
                            🗑️
                        </button>
                    </td>
                </tr>
                `;
            }).join('');
        }

        function filtrarTabla() {
            mostrarTabla(inputBuscador.value);
        }

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const nuevoRegistro = {
                cliente: document.getElementById('cliente').value,
                vendedor: document.getElementById('vendedor').value,
                numP: document.getElementById('numP').value,
                fechaC: document.getElementById('fechaC').value,
                fechaA: document.getElementById('fechaA').value,
                monto: document.getElementById('monto').value,
                corp: document.getElementById('esCorp').checked,
                timestamp: Date.now() // ID único
            };
            const datosActuales = JSON.parse(localStorage.getItem('presupuestos')) || [];
            datosActuales.push(nuevoRegistro);
            localStorage.setItem('presupuestos', JSON.stringify(datosActuales));
            this.reset();
            inputBuscador.value = ""; // Limpiar buscador al cargar nuevo
            mostrarTabla();
        });

        window.borrarUno = function(index) {
            if(confirm('¿Eliminar este registro?')) {
                const datos = JSON.parse(localStorage.getItem('presupuestos')) || [];
                datos.splice(index, 1);
                localStorage.setItem('presupuestos', JSON.stringify(datos));
                mostrarTabla(inputBuscador.value);
            }
        }

        window.descargarCSV = function() {
            const datos = JSON.parse(localStorage.getItem('presupuestos')) || [];
            if(datos.length === 0) return alert('No hay datos');
            let csv = "Cliente,Vendedor,Nro Ppto,Fecha Creacion,Fecha Aprobacion,Monto,Corporativo\\r\\n";
            datos.forEach(d => {
                csv += "${d.cliente}","${d.vendedor}","${d.numP}","${d.fechaC}","${d.fechaA}","${d.monto}","${d.corp?'SI':'NO'}"\\r\\n;
            });
            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.setAttribute("download", "planilla_aprobados.csv");
            link.click();
        }

        mostrarTabla();
    </script>
</body>
</html>
"""

# Renderizar en Streamlit con altura suficiente
components.html(html_code, height=1100, scrolling=True)