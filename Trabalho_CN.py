import math
import sympy
import time

TOLERANCIA = 0.0000001

# --- FUNÇÕES AUXILIARES ---

def criar_funcao_numerica(expressao_str, variavel_simbolica):
    """
    Converte uma string em uma expressão simbólica e uma função numérica.
    """
    try:
        expressao_simbolica = sympy.parse_expr(expressao_str)
        funcao_numerica = sympy.lambdify(variavel_simbolica, expressao_simbolica, 'math')
        return expressao_simbolica, funcao_numerica
    except (sympy.SympifyError, TypeError) as e:
        print(f"ERRO: A expressão '{expressao_str}' não é válida. Detalhes: {e}")
        exit()

def encontrar_intervalos(f, a_macro, b_macro, passo=0.1):
    """
    Varre um intervalo macro e encontra micro intervalos onde a função troca de sinal,
    fundindo intervalos adjacentes para evitar duplicidade.
    """
    intervalos_encontrados = []
    ponto_atual = a_macro
    
    while ponto_atual < b_macro:
        proximo_ponto = round(min(ponto_atual + passo, b_macro), 10)
        
        try:
            valor_atual = f(ponto_atual)
            valor_proximo = f(proximo_ponto)

            if valor_atual * valor_proximo <= 0:
                if intervalos_encontrados and math.isclose(ponto_atual, intervalos_encontrados[-1][1]):
                    intervalo_anterior = intervalos_encontrados.pop()
                    intervalos_encontrados.append((intervalo_anterior[0], proximo_ponto))
                else:
                    intervalos_encontrados.append((ponto_atual, proximo_ponto))

        except (ValueError, TypeError):
            pass

        ponto_atual = proximo_ponto
        
    return intervalos_encontrados

# --- MÉTODOS NUMÉRICOS (com retorno de iterações) ---

def bisseccao(f, a, b):
    i = 1
    p = 0.0 
    while True:
        p = (a + b) / 2
        img_a = f(a)
        img_b = f(b)
        img_p = f(p)
        print(f"{i}: a = {a:.7f}, f(a) = {img_a:.7f}")
        print(f"{i}: b = {b:.7f}, f(b) = {img_b:.7f}")
        print(f"{i}: p = {p:.7f}, f(p) = {img_p:.7f}")
        if (img_a * img_p < 0):
            b = p
        elif (img_b * img_p < 0):
            a = p
        elif img_p == 0:
            return p, i
        i += 1
        if not (math.fabs(img_p) > TOLERANCIA):
            break
    return p, i - 1

def fp(f, a, b):
    i = 1
    p = 0.0
    while True:
        img_a = f(a)
        img_b = f(b)
        if (img_b - img_a) == 0:
            print("Divisão por zero no método da Falsa Posição. Interrompendo.")
            return p, i - 1
        p = ((a * img_b) - (b * img_a)) / (img_b - img_a)
        img_p = f(p)
        print(f"{i}: a = {a:.7f}, f(a) = {img_a:.7f}")
        print(f"{i}: b = {b:.7f}, f(b) = {img_b:.7f}")
        print(f"{i}: p = {p:.7f}, f(p) = {img_p:.7f}")
        if (img_a * img_p < 0):
            b = p
        elif (img_b * img_p < 0):
            a = p
        elif img_p == 0:
            return p, i
        i += 1
        if not (math.fabs(img_p) > TOLERANCIA):
            break
    return p, i - 1

def NewtonRaphson(ff, x):
    ant = x + 2
    x2 = x
    i = 1
    while (i <= 500):
        try:
            x2 = ff(x2)
        except ZeroDivisionError:
            print(f"ERRO: Divisão por zero na iteração {i} de Newton-Raphson (derivada foi zero).")
            return x2, i
        if (math.fabs(ant - x2) < TOLERANCIA):
            return x2, i - 1
        else:
            ant = x2
        print(f"{i}: raiz = {x2:.7f}")
        i += 1
    print(f"Não convergiu após {i-1} iterações.")
    return x2, i - 1
    
def secante(f, c1, c2):
    x = 0.0
    x1 = c1
    x2 = c2
    i = 1
    while True:
        if math.isclose(x1, x2):
            print("Chutes iniciais para o método da Secante são muito próximos. Interrompendo.")
            return x1, 0

        img_x1 = f(x1)
        img_x2 = f(x2)
        if (math.fabs(img_x2) < TOLERANCIA):
            return x2, i - 1
        denominador = (img_x2 - img_x1)
        if denominador == 0:
            print("Divisão por zero no método da Secante. Interrompendo.")
            return x2, i 
        x = x2 - (img_x2 * (x2 - x1) / denominador)
        print(f"{i}: raiz = {x:.7f}")
        x1 = x2
        x2 = x
        i += 1
        if i > 500:
            print("Não convergiu após 500 iterações.")
            return x, i - 1

# --- BLOCO PRINCIPAL ---
if __name__ == '__main__':
    x_simbolico = sympy.symbols('x')
    
    print("------------------------------------")
    print("Digite a função f(x) a ser analisada.")
    funcao_str = input("f(x) = ")
    
    f_expr, f = criar_funcao_numerica(funcao_str, x_simbolico)
    
    print("\nDigite o intervalo MACRO [A, B] para procurar por raízes: ")
    A_macro, B_macro = map(float, input().split())

    print("Digite o tamanho do passo para a busca (sugestão: 0.1): ")
    passo_busca = float(input())
    print("------------------------------------")
    
    print(f"\nBuscando raízes no intervalo [{A_macro}, {B_macro}]...")
    intervalos = encontrar_intervalos(f, A_macro, B_macro, passo_busca)
    
    if not intervalos:
        print("Nenhuma raiz encontrada no intervalo fornecido com o passo especificado.")
        exit()
        
    print("\nForam encontrados os seguintes intervalos com possíveis raízes:")
    for i, (inicio, fim) in enumerate(intervalos):
        print(f"  {i+1}: [{inicio:.4f}, {fim:.4f}]")
        
    escolha = int(input("\nEscolha o número do intervalo que deseja analisar: "))
    
    A, B = intervalos[escolha - 1]
    
    ref_nr = (A + B) / 2
    ref_s1 = A
    ref_s2 = B
    
    print("\n------------------------------------")
    print(f"Intervalo [{A:.4f}, {B:.4f}] selecionado.")
    print(f"Chute para Newton-Raphson definido como o ponto médio: {ref_nr:.4f}")
    print(f"Chutes para Secante definidos como os limites do intervalo: {ref_s1:.4f} e {ref_s2:.4f}")
    print("------------------------------------")

    resultados_finais = []

    # --- Execução dos métodos ---
    print("\n-------------BISSECCAO-------------")
    inicio_tempo = time.perf_counter()
    resultado, iteracoes = bisseccao(f, A, B)
    fim_tempo = time.perf_counter()
    resultados_finais.append({'metodo': 'Bissecção', 'raiz': resultado, 'tempo': fim_tempo - inicio_tempo, 'iteracoes': iteracoes})
    print(f"Sua raiz eh: {resultado:.7f}")
    
    print("\n-------------FALSA POSICAO-------------")
    inicio_tempo = time.perf_counter()
    resultado, iteracoes = fp(f, A, B)
    fim_tempo = time.perf_counter()
    resultados_finais.append({'metodo': 'Falsa Posição', 'raiz': resultado, 'tempo': fim_tempo - inicio_tempo, 'iteracoes': iteracoes})
    print(f"Sua raiz eh: {resultado:.7f}")

    print("\n-------------NEWTON-RAPHSON-------------")
    f_derivada_expr = sympy.diff(f_expr, x_simbolico)
    print(f"Derivada calculada automaticamente: f'(x) = {f_derivada_expr}")
    f_derivada = sympy.lambdify(x_simbolico, f_derivada_expr, 'math')
    def ff(x_val):
        derivada_val = f_derivada(x_val)
        if derivada_val == 0: raise ZeroDivisionError
        return x_val - f(x_val) / derivada_val
    inicio_tempo = time.perf_counter()
    resultado, iteracoes = NewtonRaphson(ff, ref_nr)
    fim_tempo = time.perf_counter()
    resultados_finais.append({'metodo': 'Newton-Raphson', 'raiz': resultado, 'tempo': fim_tempo - inicio_tempo, 'iteracoes': iteracoes})
    print(f"Sua raiz eh aproximadamente {resultado:.7f}")

    print("\n-------------SECANTE-------------")
    inicio_tempo = time.perf_counter()
    resultado, iteracoes = secante(f, ref_s1, ref_s2)
    fim_tempo = time.perf_counter()
    resultados_finais.append({'metodo': 'Secante', 'raiz': resultado, 'tempo': fim_tempo - inicio_tempo, 'iteracoes': iteracoes})
    print(f"Sua raiz eh: {resultado:.7f}")
    print("------------------------------------")

    # --- Tabela Comparativa ---
    print("\n\n======== TABELA COMPARATIVA DE RESULTADOS ========")
    print(f"{'Método':<20} | {'Raiz Encontrada':<25} | {'Iterações':<12} | {'Tempo de Execução (ms)':<25}") # <--- ALTERADO
    print("-" * 90)
    for res in resultados_finais:
        tempo_ms = res['tempo'] * 1000 # <--- ALTERADO
        print(f"{res['metodo']:<20} | {res['raiz']:<25.7f} | {res['iteracoes']:<12} | {tempo_ms:<25.6f}") # <--- ALTERADO
    print("==========================================================================================")