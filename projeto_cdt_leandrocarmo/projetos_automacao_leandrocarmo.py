from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Base de dados inicial de exemplo
registros_alunos = {
    "Leandro Do Carmo": {"aulas_assistidas": 18, "total_aulas": 20},
    "Ana Silva": {"aulas_assistidas": 12, "total_aulas": 20},
    "Carlos Eduardo": {"aulas_assistidas": 16, "total_aulas": 20},
    "Beatriz Souza": {"aulas_assistidas": 9, "total_aulas": 20}
}

HTML_TEMPLATE = """
<!doctype html>
<html lang="pt-BR" class="dark">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartFrequência | Sistema de Gestão Escolar</title>
    <!-- Tailwind CSS para um design ultra moderno -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        darker: '#0b0f19',
                        darkcard: '#111827',
                        accent: '#3b82f6',
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-darker text-gray-100 min-h-screen font-sans selection:bg-blue-500 selection:text-white">

    <!-- Header / Navbar -->
    <header class="border-b border-gray-800 bg-darkcard/50 backdrop-blur-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="bg-blue-600 p-2.5 rounded-xl text-white shadow-lg shadow-blue-500/30">
                    <i class="fa-solid fa-graduation-cap text-xl"></i>
                </div>
                <div>
                    <h1 class="text-xl font-bold tracking-tight text-white">SmartFrequência</h1>
                    <p class="text-xs text-gray-400">Sistema Inteligente de Controle Acadêmico</p>
                </div>
            </div>
            <div class="hidden md:flex items-center space-x-2 text-sm bg-gray-800/60 px-4 py-2 rounded-full border border-gray-700/50">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span class="text-gray-300">Status do Sistema: <strong class="text-white">Online no Render</strong></span>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-6 py-10 space-y-10">

        <!-- Cards de Estatísticas Rápidas -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-darkcard border border-gray-800/80 p-6 rounded-2xl shadow-xl relative overflow-hidden group hover:border-blue-500/50 transition-all">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-sm font-medium text-gray-400">Total de Alunos</p>
                        <h3 class="text-3xl font-extrabold text-white mt-1">{{ total_alunos }}</h3>
                    </div>
                    <div class="p-3 bg-blue-500/10 text-blue-400 rounded-xl">
                        <i class="fa-solid fa-users text-xl"></i>
                    </div>
                </div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 to-indigo-500"></div>
            </div>

            <div class="bg-darkcard border border-gray-800/80 p-6 rounded-2xl shadow-xl relative overflow-hidden group hover:border-emerald-500/50 transition-all">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-sm font-medium text-gray-400">Alunos Aptos (>= 75%)</p>
                        <h3 class="text-3xl font-extrabold text-emerald-400 mt-1">{{ total_aptos }}</h3>
                    </div>
                    <div class="p-3 bg-emerald-500/10 text-emerald-400 rounded-xl">
                        <i class="fa-solid fa-circle-check text-xl"></i>
                    </div>
                </div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-emerald-500 to-teal-500"></div>
            </div>

            <div class="bg-darkcard border border-gray-800/80 p-6 rounded-2xl shadow-xl relative overflow-hidden group hover:border-rose-500/50 transition-all">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-sm font-medium text-gray-400">Alunos Retidos (< 75%)</p>
                        <h3 class="text-3xl font-extrabold text-rose-400 mt-1">{{ total_retidos }}</h3>
                    </div>
                    <div class="p-3 bg-rose-500/10 text-rose-400 rounded-xl">
                        <i class="fa-solid fa-triangle-exclamation text-xl"></i>
                    </div>
                </div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-rose-500 to-red-500"></div>
            </div>
        </div>

        <!-- Seção de Ação e Tabela -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <!-- Formulário de Chamada (Esquerda) -->
            <div class="bg-darkcard border border-gray-800/80 p-6 rounded-2xl shadow-xl h-fit">
                <h2 class="text-lg font-bold text-white mb-4 flex items-center space-x-2">
                    <i class="fa-solid fa-pen-to-square text-blue-500"></i>
                    <span>Registrar Chamada</span>
                </h2>
                
                <form action="/registrar" method="POST" class="space-y-4">
                    <div>
                        <label class="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Nome Completo do Aluno</label>
                        <input type="text" name="nome" required placeholder="Ex: João da Silva" 
                            class="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors">
                    </div>

                    <div>
                        <label class="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Status da Aula</label>
                        <select name="status" class="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-colors">
                            <option value="presente">✅ Presente</option>
                            <option value="ausente">❌ Ausente</option>
                        </select>
                    </div>

                    <button type="submit" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-3.5 px-4 rounded-xl shadow-lg shadow-blue-600/30 transition-all flex items-center justify-center space-x-2">
                        <i class="fa-solid fa-floppy-disk"></i>
                        <span>Salvar Registro</span>
                    </button>
                </form>
            </div>

            <!-- Tabela de Alunos e Frequências (Direita - Ocupa 2 colunas) -->
            <div class="lg:col-span-2 bg-darkcard border border-gray-800/80 rounded-2xl shadow-xl overflow-hidden flex flex-col">
                <div class="p-6 border-b border-gray-800 flex justify-between items-center">
                    <h2 class="text-lg font-bold text-white flex items-center space-x-2">
                        <i class="fa-solid fa-list-check text-blue-500"></i>
                        <span>Relatório de Frequência em Tempo Real</span>
                    </h2>
                    <span class="text-xs text-gray-400 font-medium">Corte mínimo: 75%</span>
                </div>

                <div class="overflow-x-auto flex-1">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-gray-900/50 text-gray-400 text-xs uppercase tracking-wider border-b border-gray-800">
                                <th class="py-4 px-6 font-semibold">Aluno</th>
                                <th class="py-4 px-6 font-semibold text-center">Presenças / Total</th>
                                <th class="py-4 px-6 font-semibold">Frequência</th>
                                <th class="py-4 px-6 font-semibold text-center">Status</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-800/60 text-sm">
                            {% for nome, dados in alunos.items() %}
                            {% set pct = (dados.aulas_assistidas / dados.total_aulas * 100) if dados.total_aulas > 0 else 0 %}
                            <tr class="hover:bg-gray-800/30 transition-colors">
                                <td class="py-4 px-6 font-medium text-white flex items-center space-x-3">
                                    <div class="w-8 h-8 rounded-full bg-blue-500/10 text-blue-400 flex items-center justify-center font-bold text-xs border border-blue-500/20">
                                        {{ nome[:2].upper() }}
                                    </div>
                                    <span>{{ nome }}</span>
                                </td>
                                <td class="py-4 px-6 text-center text-gray-300">
                                    <span class="text-white font-semibold">{{ dados.aulas_assistidas }}</span> / {{ dados.total_aulas }}
                                </td>
                                <td class="py-4 px-6 w-44">
                                    <div class="flex items-center space-x-3">
                                        <div class="flex-1 bg-gray-800 rounded-full h-2 overflow-hidden">
                                            <div class="h-full rounded-full transition-all duration-500 {% if pct >= 75 %}bg-emerald-500{% else %}bg-rose-500{% endif %}" style="width: {{ '%.1f'|format(pct) }}%"></div>
                                        </div>
                                        <span class="text-xs font-bold {% if pct >= 75 %}text-emerald-400{% else %}text-rose-400{% endif %}">{{ "%.1f"|format(pct) }}%</span>
                                    </div>
                                </td>
                                <td class="py-4 px-6 text-center">
                                    {% if pct >= 75 %}
                                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                                        <i class="fa-solid fa-check mr-1.5"></i> Apto
                                    </span>
                                    {% else %}
                                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
                                        <i class="fa-solid fa-xmark mr-1.5"></i> Retido
                                    </span>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

        </div>

    </main>

    <!-- Footer -->
    <footer class="border-t border-gray-800 mt-20 py-8 text-center text-xs text-gray-500">
        <p>SmartFrequência &bull; Desenvolvido para Apresentação Acadêmica &bull; Rodando no Render</p>
    </footer>

</body>
</html>
"""

@app.route('/')
def index():
    total_alunos = len(registros_alunos)
    total_aptos = 0
    total_retidos = 0
    
    for dados in registros_alunos.values():
        total = dados["total_aulas"]
        pct = (dados["aulas_assistidas"] / total * 100) if total > 0 else 0
        if pct >= 75:
            total_aptos += 1
        else:
            total_retidos += 1
            
    return render_template_string(
        HTML_TEMPLATE, 
        alunos=registros_alunos,
        total_alunos=total_alunos,
        total_aptos=total_aptos,
        total_retidos=total_retidos
    )

@app.route('/registrar', methods=['POST'])
def registrar():
    nome = request.form.get('nome').strip()
    status = request.form.get('status')
    
    if nome:
        if nome not in registros_alunos:
            registros_alunos[nome] = {"aulas_assistidas": 0, "total_aulas": 0}
        
        registros_alunos[nome]["total_aulas"] += 1
        if status == 'presente':
            registros_alunos[nome]["aulas_assistidas"] += 1
            
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)