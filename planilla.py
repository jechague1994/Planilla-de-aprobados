import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Planilla de Aprobados", layout="wide")

# Código HTML, CSS y JavaScript
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 p-4 font-sans">
    <div class="max-w-6xl mx-auto">
        <h1 class="text-4xl font-extrabold text-center text-slate-800 mb-8 uppercase tracking-wider border-b-4 border-blue-600 pb-4">
            Planilla de aprobados
        </h1>

        <div class="bg-white p-8 rounded-xl shadow-md mb-8 border border-slate-200">
            <h2 class="text-xl font-semibold mb-6 text-blue-700">Cargar Nuevo Presupuesto</h2>
            <form id="presupuestoForm" class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <label class="block text-sm font-bold text-gray-600">Nombre del Cliente</label>
                    <input type="text" id="cliente" required class="w-full border-gray-300 border rounded-lg p-2 outline-none focus:border-blue-500" placeholder="Empresa o Particular">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-600">Vendedor</label>
                    <input type="text" id="vendedor" required class="w-full border-gray-300 border rounded-lg p-2 outline-none focus:border-blue-500" placeholder="Nombre del vendedor">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-600">N° Presupuesto</label>
                    <input type="text" id="numP" required class="w-full border-gray-300 border rounded-lg p-2 outline-none focus:border-blue-500">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-600">Fecha Creación</label>
                    <input type="date" id="fechaC" required class="w-full border-gray-300 border rounded-lg p-2 outline-none">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-600">Fecha Aprobación</label>
                    <input type="date" id="fechaA" required class="w-full border-gray-300 border rounded-lg p-2 outline-none">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-600">Monto ($)</label>
                    <input type="number" id="monto" step="0.01" required class="w-full border-gray-300 border rounded-lg p-2 outline-none" placeholder="0.00">
                </div>
                <div class="flex items-center">
                    <input type="checkbox" id="esCorp" class="h-4 w-4 text-blue-600">
                    <label for="esCorp" class="ml-2 text-sm font-bold text-gray-700">¿Cliente Corporativo?</label>
                </div>
                <div class="md:col-span-2">
                    <button type="submit" class="w-full bg-blue-600 text-white font-bold py-2 rounded-lg hover:bg-blue-700 shadow transition-all">
                        Registrar en Planilla
                    </button>
                </div>
            </form>
        </div>

        <div class="mb-4 flex justify-end">
            <button onclick="descargarCSV()" class="bg-green-600 text-white px-4 py-2 rounded-lg font-bold hover:bg-green-700 flex items-center shadow">
                <span>📊 Descargar Excel (CSV)</span>
            </button>
        </div>

        <div class="bg-white rounded-xl shadow-xl overflow-hidden border border-slate-200">
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200 text-left">
                    <thead class="bg-slate-800 text-white">
                        <tr>
                            <th class="px-4 py-3 text-xs font-bold uppercase">Cliente</th>
                            <th class="px-4 py-3 text-xs font-bold uppercase">N° Presup.</th>
                            <th class="px-4 py-3 text-xs font-bold uppercase">Vendedor</th>
                            <th class="px-4 py-3 text-xs font-bold uppercase">Aprobado</th>
                            <th class="px-4 py-3 text-xs font-bold uppercase">Monto</th>
                            <th class="px-4 py-3 text-xs font-bold uppercase text-center">Corp.</th>
                            <th class="px-4 py-3 text-xs font-bold uppercase text-center">Acción</th>
                        </tr>
                    </thead>
                    <tbody id="tablaCuerpo" class="divide-y divide-gray-200"></tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('presupuestoForm');
        const tabla = document.getElementById('tablaCuerpo');

        function mostrar() {
            let datos = JSON.parse(localStorage.getItem('presupuestos')) || [];
            tabla.innerHTML = datos.map((item, index) => `
                <tr class="hover:bg-gray-50 text-sm">
                    <td class="px-4 py-3 font-medium text-gray-900">${item.cliente}</td>
                    <td class="px-4 py-3 text-gray-600">${item.numP}</td>
                    <td class="px-4 py-3 text-gray-600">${item.vendedor}</td>
                    <td class="px-4 py-3 text-gray-600">${item.fechaA}</td>
                    <td class="px-4 py-3 font-bold text-green-600">$${parseFloat(item.monto).toLocaleString()}</td>
                    <td class="px-4 py-3 text-center">${item.corp ? '✅' : '❌'}</td>
                    <td class="px-4 py-3 text-center">
                        <button onclick="borrarUno(${index})" class="text-red-500 hover:text-red-700 text-lg" title="Eliminar">🗑️</button>
                    </td>
                </tr>
            `).join('');
        }

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const d = JSON.parse(localStorage.getItem('presupuestos')) || [];
            d.push({
                cliente: document.getElementById('cliente').value,
                vendedor: document.getElementById('vendedor').value,
                numP: document.getElementById('numP').value,
                fechaC: document.getElementById('fechaC').value,
                fechaA: document.getElementById('fechaA').value,
                monto: document.getElementById('monto').value,
                corp: document.getElementById('esCorp').checked
            });
            localStorage.setItem('presupuestos', JSON.stringify(d));
            form.reset();
            mostrar();
        });

        function borrarUno(index) {
            if(confirm('¿Eliminar este registro?')) {
                let d = JSON.parse(localStorage.getItem('presupuestos'));
                d.splice(index, 1);
                localStorage.setItem('presupuestos', JSON.stringify(d));
                mostrar();
            }
        }

        function descargarCSV() {
            let datos = JSON.parse(localStorage.getItem('presupuestos')) || [];
            if(datos.length === 0) return alert('No hay datos para exportar');

            let csvContent = "data:text/csv;charset=utf-8,";
            csvContent += "Cliente,Vendedor,Num Presupuesto,Fecha Creacion,Fecha Aprobacion,Monto,Corporativo\\n";
            
            datos.forEach(item => {
                let fila = ${item.cliente},${item.vendedor},${item.numP},${item.fechaC},${item.fechaA},${item.monto},${item.corp ? 'SI' : 'NO'};
                csvContent += fila + "\\n";
            });

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "planilla_aprobados.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        mostrar();
    </script>
</body>
</html>
"""

# Renderizar en Streamlit
components.html(html_code, height=900, scrolling=True)