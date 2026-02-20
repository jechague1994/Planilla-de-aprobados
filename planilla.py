<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Planilla de aprobados</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 p-4 md:p-10 font-sans">

    <div class="max-w-5xl mx-auto">
        <h1 class="text-4xl font-extrabold text-center text-slate-800 mb-8 uppercase tracking-wider border-b-4 border-blue-600 pb-4">
            Planilla de aprobados
        </h1>

        <div class="bg-white p-8 rounded-xl shadow-md mb-10 border border-slate-200">
            <h2 class="text-xl font-semibold mb-6 text-blue-700 flex items-center">
                <span class="mr-2">📝</span> Cargar Nuevo Presupuesto
            </h2>
            
            <form id="presupuestoForm" class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                    <label class="block text-sm font-bold text-gray-600 mb-1">Fecha de Creación</label>
                    <input type="date" id="fechaCreacion" required class="w-full border-gray-300 border rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-600 mb-1">Fecha de Aprobación</label>
                    <input type="date" id="fechaAprobacion" required class="w-full border-gray-300 border rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-600 mb-1">Número de Presupuesto</label>
                    <input type="text" id="numPresupuesto" required class="w-full border-gray-300 border rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Ej: 00452">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-600 mb-1">Monto ($)</label>
                    <input type="number" id="monto" step="0.01" required class="w-full border-gray-300 border rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="0.00">
                </div>
                <div>
                    <label class="block text-sm font-bold text-gray-600 mb-1">Nombre del Vendedor</label>
                    <input type="text" id="vendedor" required class="w-full border-gray-300 border rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Juan Pérez">
                </div>
                <div class="flex items-center md:pt-6">
                    <label class="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" id="esCorporativo" class="sr-only peer">
                        <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        <span class="ml-3 text-sm font-bold text-gray-700">¿Cliente Corporativo?</span>
                    </label>
                </div>
                
                <div class="md:col-span-3">
                    <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-blue-700 shadow-lg transform active:scale-[0.98] transition-all">
                        Registrar en Planilla
                    </button>
                </div>
            </form>
        </div>

        <div class="bg-white rounded-xl shadow-xl overflow-hidden border border-slate-200">
            <div class="bg-slate-800 p-4">
                <h3 class="text-white font-bold tracking-wide">Historial de Registros</h3>
            </div>
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">N° Presup.</th>
                            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Creado</th>
                            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Aprobado</th>
                            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Monto</th>
                            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Vendedor</th>
                            <th class="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider">Corp.</th>
                        </tr>
                    </thead>
                    <tbody id="tablaCuerpo" class="bg-white divide-y divide-gray-200">
                        </tbody>
                </table>
            </div>
        </div>
        
        <div class="mt-4 text-right">
            <button onclick="borrarTodo()" class="text-xs text-red-500 hover:underline">Borrar todos los datos de la tabla</button>
        </div>
    </div>

    <script>
        const form = document.getElementById('presupuestoForm');
        const tabla = document.getElementById('tablaCuerpo');

        // Cargar datos al iniciar
        document.addEventListener('DOMContentLoaded', mostrarDatos);

        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const nuevoRegistro = {
                numP: document.getElementById('numPresupuesto').value,
                fechaC: document.getElementById('fechaCreacion').value,
                fechaA: document.getElementById('fechaAprobacion').value,
                monto: document.getElementById('monto').value,
                vendedor: document.getElementById('vendedor').value,
                corp: document.getElementById('esCorporativo').checked
            };

            guardarEnStorage(nuevoRegistro);
            form.reset();
            mostrarDatos();
        });

        function guardarEnStorage(registro) {
            let datos = JSON.parse(localStorage.getItem('presupuestos')) || [];
            datos.push(registro);
            localStorage.setItem('presupuestos', JSON.stringify(datos));
        }

        function mostrarDatos() {
            let datos = JSON.parse(localStorage.getItem('presupuestos')) || [];
            tabla.innerHTML = '';
            
            datos.forEach(item => {
                const fila = `
                    <tr class="hover:bg-blue-50 transition-colors">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">${item.numP}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">${item.fechaC}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">${item.fechaA}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-green-600">$${parseFloat(item.monto).toLocaleString()}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 italic">${item.vendedor}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-center">
                            <span class="px-2 py-1 text-xs rounded-full ${item.corp ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-400'}">
                                ${item.corp ? 'CORPORATIVO' : 'No'}
                            </span>
                        </td>
                    </tr>
                `;
                tabla.innerHTML += fila;
            });
        }

        function borrarTodo() {
            if(confirm('¿Estás seguro de que quieres borrar todos los datos?')) {
                localStorage.removeItem('presupuestos');
                mostrarDatos();
            }
        }
    </script>
</body>
</html>