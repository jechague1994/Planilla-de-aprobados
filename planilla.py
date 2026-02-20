import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página de Streamlit
st.set_page_config(page_title="Planilla de Aprobados", layout="wide")

# Definimos el código HTML/JavaScript
html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 p-4 font-sans">
    <div class="max-w-5xl mx-auto">
        <h1 class="text-4xl font-extrabold text-center text-slate-800 mb-8 uppercase tracking-wider border-b-4 border-blue-600 pb-4">
            Planilla de aprobados
        </h1>

        <div class="bg-white p-8 rounded-xl shadow-md mb-10 border border-slate-200">
            <h2 class="text-xl font-semibold mb-6 text-blue-700 flex items-center">
                Cargar Nuevo Presupuesto
            </h2>
            
            <form id="presupuestoForm" class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                    <label class="block text-sm font-bold text-gray-600 mb-1">Fecha de Creación</label>
                    <input type="date" id="fechaCreacion" required class="w-full border-gray-300 border rounded-lg p-2.5 outline-none">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-600 mb-1">Fecha de Aprobación</label>
                    <input type="date" id="fechaAprobacion" required class="w-full border-gray-300 border rounded-lg p-2.5 outline-none">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-600 mb-1">Número de Presupuesto</label>
                    <input type="text" id="numPresupuesto" required class="w-full border-gray-300 border rounded-lg p-2.5 outline-none" placeholder="Ej: 00452">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-600 mb-1">Monto ($)</label>
                    <input type="number" id="monto" step="0.01" required class="w-full border-gray-300 border rounded-lg p-2.5 outline-none" placeholder="0.00">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-600 mb-1">Nombre del Vendedor</label>
                    <input type="text" id="vendedor" required class="w-full border-gray-300 border rounded-lg p-2.5 outline-none" placeholder="Juan Pérez">
                </div>
                <div class="flex items-center md:pt-6">
                    <input type="checkbox" id="esCorporativo" class="h-4 w-4 text-blue-600 border-gray-300 rounded">
                    <label for="esCorporativo" class="ml-2 block text-sm font-bold text-gray-700">¿Cliente Corporativo?</label>
                </div>
                
                <div class="md:col-span-3">
                    <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-blue-700 shadow-lg transition-all">
                        Registrar en Planilla
                    </button>
                </div>
            </form>
        </div>

        <div class="bg-white rounded-xl shadow-xl overflow-hidden border border-slate-200">
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">N° Presup.</th>
                            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Creado</th>
                            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Aprobado</th>
                            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Monto</th>
                            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Vendedor</th>
                            <th class="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase">Corp.</th>
                        </tr>
                    </thead>
                    <tbody id="tablaCuerpo" class="bg-white divide-y divide-gray-200"></tbody>
                </table>
            </div>
        </div>
        <button onclick="localStorage.removeItem('presupuestos'); location.reload();" class="mt-4 text-xs text-red-500 underline">Borrar todo</button>
    </div>

    <script>
        const form = document.getElementById('presupuestoForm');
        const tabla = document.getElementById('tablaCuerpo');

        function mostrar() {
            let datos = JSON.parse(localStorage.getItem('presupuestos')) || [];
            tabla.innerHTML = datos.map(item => `
                <tr>
                    <td class="px-6 py-4 text-sm font-bold text-gray-900 border-b">${item.numP}</td>
                    <td class="px-6 py-4 text-sm text-gray-600 border-b">${item.fechaC}</td>
                    <td class="px-6 py-4 text-sm text-gray-600 border-b">${item.fechaA}</td>
                    <td class="px-6 py-4 text-sm font-bold text-green-600 border-b">$${item.monto}</td>
                    <td class="px-6 py-4 text-sm text-gray-700 border-b">${item.vendedor}</td>
                    <td class="px-6 py-4 text-center border-b">${item.corp ? '✅' : '❌'}</td>
                </tr>
            `).join('');
        }

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const d = JSON.parse(localStorage.getItem('presupuestos')) || [];
            d.push({
                numP: document.getElementById('numPresupuesto').value,
                fechaC: document.getElementById('fechaCreacion').value,
                fechaA: document.getElementById('fechaAprobacion').value,
                monto: document.getElementById('monto').value,
                vendedor: document.getElementById('vendedor').value,
                corp: document.getElementById('esCorporativo').checked
            });
            localStorage.setItem('presupuestos', JSON.stringify(d));
            form.reset();
            mostrar();
        });
        mostrar();
    </script>
</body>
</html>
"""

# Esta línea es la que hace la magia en Streamlit
components.html(html_code, height=800, scrolling=True)