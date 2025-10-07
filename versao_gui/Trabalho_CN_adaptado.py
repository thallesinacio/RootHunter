import math
import sympy
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')


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

def encontrar_intervalos(f, a_macro, b_macro, passo):
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

def bisseccao(f, a, b, TOLERANCIA, max_iter):
    log=[]
    inicio = time.perf_counter()
    i = 1
    p = 0.0
    while i<=max_iter:
        p = (a + b) / 2
        img_a = f(a)
        img_b = f(b)
        img_p = f(p)
        log.extend([f"{i}: a = {a:.7f}, f(a) = {img_a:.7f}",f"{i}: b = {b:.7f}, f(b) = {img_b:.7f}",f"{i}: p = {p:.7f}, f(p) = {img_p:.7f}"])
        if (img_a * img_p < 0):
            b = p
        elif (img_b * img_p < 0):
            a = p
        elif img_p == 0:
            return p, i, (time.perf_counter() - inicio) * 1000, "\n".join(log)
        i += 1
        if not (math.fabs(img_p) > TOLERANCIA):
            break
    return p, i - 1,(time.perf_counter() - inicio) * 1000, "\n".join(log)

def fp(f, a, b, TOLERANCIA, max_iter):
    log=[]
    inicio = time.perf_counter()
    i = 1
    p = 0.0
    while i<=max_iter:
        img_a = f(a)
        img_b = f(b)
        if (img_b - img_a) == 0:
            log.append("Divisão por zero no método da Falsa Posição. Interrompendo.")
            return p, i - 1,(time.perf_counter() - inicio) * 1000, "\n".join(log)
        p = ((a * img_b) - (b * img_a)) / (img_b - img_a)
        img_p = f(p)
        log.extend([f"{i}: a = {a:.7f}, f(a) = {img_a:.7f}", f"{i}: b = {b:.7f}, f(b) = {img_b:.7f}",f"{i}: p = {p:.7f}, f(p) = {img_p:.7f}"])
        if (img_a * img_p < 0):
            b = p
        elif (img_b * img_p < 0):
            a = p
        elif img_p == 0:
            return p, i, (time.perf_counter() - inicio) * 1000, "\n".join(log)
        i += 1
        if not (math.fabs(img_p) > TOLERANCIA):
            break
    return p, i - 1,(time.perf_counter() - inicio) * 1000, "\n".join(log)

def NewtonRaphson(ff, x,TOLERANCIA, max_iter):
    log = []
    inicio = time.perf_counter()
    ant = x + 2
    x2 = x
    i = 1
    while i<=max_iter:
        try:
            x2 = ff(x2)
        except ZeroDivisionError:
            log.append(f"ERRO: Divisão por zero na iteração {i} de Newton-Raphson (derivada foi zero).")
            return x2, i,(time.perf_counter() - inicio) * 1000, "\n".join(log)
        if (math.fabs(ant - x2) < TOLERANCIA):
            return x2, i - 1,(time.perf_counter() - inicio) * 1000, "\n".join(log)
        else:
            ant = x2
        log.append(f"{i}: raiz = {x2:.7f}")
        i += 1
    log.append(f"Não convergiu após {i-1} iterações.")
    return x2, i - 1,(time.perf_counter() - inicio) * 1000, "\n".join(log)
    
def secante(f, x0, x1, tol, max_iter):
    log = []
    inicio = time.perf_counter()
    i = 0
    for i in range(1, max_iter + 1):
        if math.isclose(x0, x1):
            log.append(f"ERRO: Chutes iniciais x0 e x1 são iguais na iteração {i}.")
            break
        ix1, ix0 = f(x1), f(x0)
        denominador = (ix1 - ix0)
        if math.isclose(denominador, 0):
            log.append(f"ERRO: Divisão por zero na iteração {i} (f(x1) e f(x0) são iguais).")
            break
        x2 = x1 - (ix1 * (x1 - x0)) / denominador
        log.append(f"{i}: raiz = {x2:.7f}")
        if math.fabs(x2 - x1) < tol:
            x1 = x2
            break
        x0, x1 = x1, x2
    tempo_total = (time.perf_counter() - inicio) * 1000
    return x1, i, tempo_total, "\n".join(log)
  
        

def executar_busca_intervalos(args):
    funcao_str, a_str, b_str, passo_str = args
    _, f = criar_funcao_numerica(funcao_str, sympy.symbols('x'))
    if not f: raise ValueError("Função inválida")
    intervalos = encontrar_intervalos(f, float(a_str), float(b_str), float(passo_str))
    for inicio, fim in intervalos:
        print(f"[{inicio:.4f}, {fim:.4f}]")


def executar_analise(args):
    try:
        funcao_str, a_str, b_str, tol_str, max_iter_str = args
        A, B, TOL, MAX_ITER = float(a_str), float(b_str), float(tol_str), int(max_iter_str)
        x_sym = sympy.symbols('x')
        
        expressao_simbolica, funcao_numerica = criar_funcao_numerica(funcao_str, x_sym)
        
        if not funcao_numerica: 
            raise ValueError("Função inválida")
        
        res = []
        logs = []
        ref_nr, ref_s1, ref_s2 = (A + B) / 2, A, B

        # Coleta de dados e logs - use funcao_numerica em vez de f
        r, i, t, l = bisseccao(funcao_numerica, A, B, TOL, MAX_ITER)
        res.append(("Bissecção", r, i, t))
        logs.append(f"------------- BISSECÇÃO -------------\n{l}\nSua raiz eh: {r:.7f}\n")
        
        r, i, t, l = fp(funcao_numerica, A, B, TOL, MAX_ITER)
        res.append(("Falsa Posição", r, i, t))
        logs.append(f"------------- FALSA POSIÇÃO -------------\n{l}\nSua raiz eh: {r:.7f}\n")
        
        # Para Newton-Raphson precisamos da derivada
        f_derivada_expr = sympy.diff(expressao_simbolica, x_sym)
        f_derivada = sympy.lambdify(x_sym, f_derivada_expr, 'math')
        
        def ff(x_val):
            derivada_val = f_derivada(x_val)
            if derivada_val == 0: 
                raise ZeroDivisionError
            return x_val - funcao_numerica(x_val) / derivada_val
            
        r, i, t, l = NewtonRaphson(ff, ref_nr, TOL, MAX_ITER)
        res.append(("Newton-Raphson", r, i, t))
        logs.append(f"------------- NEWTON-RAPHSON -------------\nDerivada: f'(x) = {f_derivada_expr}\n{l}\nSua raiz eh aprox: {r:.7f}\n")
        
        r, i, t, l = secante(funcao_numerica, ref_s1, ref_s2, TOL, MAX_ITER)
        res.append(("Secante", r, i, t))
        logs.append(f"------------- SECANTE -------------\n{l}\nSua raiz eh: {r:.7f}\n")

        # Impressão da Tabela
        print("================== TABELA COMPARATIVA ==================")
        print(f"{'Método':<20} | {'Raiz Encontrada':<20} | {'Iterações':<10} | {'Tempo (ms)':<15} | {'|f(raiz)|':<20}")
        print("-" * 105)
        for metodo, raiz, it, tempo in res:
            if not math.isnan(raiz):
                precisao = abs(funcao_numerica(raiz))
            else:
                precisao = float('nan')
            print(f"{metodo:<20} | {raiz:<20.7f} | {it:<10} | {tempo:<15.4f} | {precisao:<20.2e}")
        print("-" * 105)

        # Impressão do separador e do log
        print("\n---LOG_DETALHADO---\n")
        print("\n".join(logs))

    except Exception as e:
        print(f"ERRO na análise: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == '__main__':
    try:
        # Limpar possíveis caracteres extras
        sys.argv = [arg.strip() for arg in sys.argv]
        
        modo = sys.argv[1].strip()
        
        if modo == "--buscar" and len(sys.argv) == 6:
            executar_busca_intervalos(sys.argv[2:])
        elif modo == "--analisar" and len(sys.argv) == 7:
            executar_analise(sys.argv[2:])
        else:
            # Debug mais detalhado
            print(f"DEBUG: Condições falharam:", file=sys.stderr)
            print(f"DEBUG: modo == '--buscar': {modo == '--buscar'}", file=sys.stderr)
            print(f"DEBUG: modo == '--analisar': {modo == '--analisar'}", file=sys.stderr)
            print(f"DEBUG: len == 6: {len(sys.argv) == 6}", file=sys.stderr)
            print(f"DEBUG: len == 7: {len(sys.argv) == 7}", file=sys.stderr)
            raise IndexError
    except (IndexError, ValueError) as e:
        print("Erro: Modo ou argumentos inválidos.", file=sys.stderr)
        print("Uso --buscar: <funcao> <A> <B> <passo>", file=sys.stderr)
        print("Uso --analisar: <funcao> <A> <B> <tol> <max_iter>", file=sys.stderr)
        exit(1)