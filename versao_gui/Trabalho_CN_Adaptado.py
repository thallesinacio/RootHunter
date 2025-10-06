# Salve este código como: Trabalho_CN_Adaptado.py

import sys
import sympy
import math
import time


# (Copie e cole aqui as mesmas funções de cálculo da resposta anterior)
# criar_funcao_numerica, encontrar_intervalos, bisseccao, fp, newton_raphson, secante
# É crucial que essas funções agora retornem o LOG, como no exemplo abaixo para a bisseccao:
# def bisseccao(f, a, b, tol, max_iter):
#     log = []
#     ...
#     log.append(f"{i}: p = {p:.7f}, f(p) = {img_p:.7f}")
#     ...
#     return p, i, tempo_total, "\n".join(log)

def criar_funcao_numerica(expressao_str, variavel_simbolica):
    try:
        local_dict = {'exp': sympy.exp, 'cos': sympy.cos, 'sin': sympy.sin, 'ln': sympy.log}
        expressao_simbolica = sympy.parse_expr(expressao_str, local_dict=local_dict)
        return sympy.lambdify(variavel_simbolica, expressao_simbolica, 'math'), expressao_simbolica
    except Exception:
        return None, None


def encontrar_intervalos(f, a, b, p):
    intervalos = [];
    atual = a
    while atual < b:
        proximo = round(min(atual + p, b), 10)
        try:
            if f(atual) * f(proximo) <= 0: intervalos.append((atual, proximo))
        except (ValueError, TypeError):
            pass
        atual = proximo
    return intervalos


def bisseccao(f, a, b, tol, max_iter):
    log = [];
    inicio = time.perf_counter();
    i = 1;
    p = a
    while i <= max_iter:
        p = (a + b) / 2
        try:
            ia, ib, ip = f(a), f(b), f(p)
        except:
            return float('nan'), i, (time.perf_counter() - inicio) * 1000, "\n".join(log)
        log.extend([f"{i}: a = {a:.7f}, f(a) = {ia:.7f}", f"{i}: b = {b:.7f}, f(b) = {ib:.7f}",
                    f"{i}: p = {p:.7f}, f(p) = {ip:.7f}"])
        if math.isclose(ip, 0) or (b - a) / 2 < tol: break
        if ia * ip < 0:
            b = p
        else:
            a = p
        i += 1
    return p, i, (time.perf_counter() - inicio) * 1000, "\n".join(log)


def fp(f, a, b, tol, max_iter):
    log = [];
    inicio = time.perf_counter();
    i = 1;
    p = a
    while i <= max_iter:
        ia, ib = f(a), f(b);
        den = (ib - ia)
        if math.isclose(den, 0): break
        p = ((a * ib) - (b * ia)) / den;
        ip = f(p)
        log.extend([f"{i}: a = {a:.7f}, f(a) = {ia:.7f}", f"{i}: b = {b:.7f}, f(b) = {ib:.7f}",
                    f"{i}: p = {p:.7f}, f(p) = {ip:.7f}"])
        if math.fabs(ip) < tol: break
        if ia * ip < 0:
            b = p
        else:
            a = p
        i += 1
    return p, i, (time.perf_counter() - inicio) * 1000, "\n".join(log)


def newton_raphson(f, df, x0, tol, max_iter):
    log = [];
    inicio = time.perf_counter();
    x = x0
    for i in range(1, max_iter + 1):
        dv = df(x)
        if math.isclose(dv, 0): log.append(f"ERRO: Derivada zero na it {i}."); break
        prox = x - f(x) / dv;
        log.append(f"{i}: raiz = {prox:.7f}")
        if math.fabs(prox - x) < tol: x = prox; break
        x = prox
    return x, i, (time.perf_counter() - inicio) * 1000, "\n".join(log)


def secante(f, x0, x1, tol, max_iter):
    log = [];
    inicio = time.perf_counter()
    for i in range(1, max_iter + 1):
        ix1, ix0 = f(x1), f(x0);
        den = (ix1 - ix0)
        if math.isclose(den, 0): log.append(f"ERRO: Divisão por zero na it {i}."); break
        x2 = x1 - (ix1 * (x1 - x0)) / den;
        log.append(f"{i}: raiz = {x2:.7f}")
        if math.fabs(x2 - x1) < tol: x1 = x2; break
        x0, x1 = x1, x2
    return x1, i, (time.perf_counter() - inicio) * 1000, "\n".join(log)


def executar_busca_intervalos(args):
    funcao_str, a_str, b_str, passo_str = args
    f, _ = criar_funcao_numerica(funcao_str, sympy.symbols('x'))
    if not f: raise ValueError("Função inválida")
    intervalos = encontrar_intervalos(f, float(a_str), float(b_str), float(passo_str))
    for inicio, fim in intervalos:
        print(f"[{inicio:.4f}, {fim:.4f}]")


def executar_analise(args):
    funcao_str, a_str, b_str, tol_str, max_iter_str = args
    A, B, TOL, MAX_ITER = float(a_str), float(b_str), float(tol_str), int(max_iter_str)
    x_sym = sympy.symbols('x')
    f, f_expr = criar_funcao_numerica(funcao_str, x_sym)
    if not f: raise ValueError("Função inválida")
    df = sympy.lambdify(x_sym, sympy.diff(f_expr, x_sym), 'math')

    res = [];
    logs = []
    ref_nr, ref_s1, ref_s2 = (A + B) / 2, A, B

    # Coleta de dados e logs
    r, i, t, l = bisseccao(f, A, B, TOL, MAX_ITER);
    res.append(("Bissecção", r, i, t));
    logs.append(f"------------- BISSECÇÃO -------------\n{l}\nSua raiz eh: {r:.7f}\n")
    r, i, t, l = fp(f, A, B, TOL, MAX_ITER);
    res.append(("Falsa Posição", r, i, t));
    logs.append(f"------------- FALSA POSIÇÃO -------------\n{l}\nSua raiz eh: {r:.7f}\n")
    r, i, t, l = newton_raphson(f, df, ref_nr, TOL, MAX_ITER);
    res.append(("Newton-Raphson", r, i, t));
    logs.append(
        f"------------- NEWTON-RAPHSON -------------\nDerivada: f'(x) = {sympy.diff(f_expr, x_sym)}\n{l}\nSua raiz eh aprox: {r:.7f}\n")
    r, i, t, l = secante(f, ref_s1, ref_s2, TOL, MAX_ITER);
    res.append(("Secante", r, i, t));
    logs.append(f"------------- SECANTE -------------\n{l}\nSua raiz eh: {r:.7f}\n")

    # Impressão da Tabela
    print("================== TABELA COMPARATIVA ==================")
    print(f"{'Método':<20} | {'Raiz Encontrada':<20} | {'Iterações':<10} | {'Tempo (ms)':<15} | {'|f(raiz)|':<20}")
    print("-" * 105)
    for metodo, raiz, it, tempo in res:
        precisao = abs(f(raiz)) if not math.isnan(raiz) else float('nan')
        print(f"{metodo:<20} | {raiz:<20.7f} | {it:<10} | {tempo:<15.4f} | {precisao:<20.2e}")
    print("==========================================================")

    # Impressão do separador e do log
    print("\n---LOG_DETALHADO---\n")
    print("\n".join(logs))


if __name__ == '__main__':
    try:
        modo = sys.argv[1]
        if modo == "--buscar" and len(sys.argv) == 6:
            executar_busca_intervalos(sys.argv[2:])
        elif modo == "--analisar" and len(sys.argv) == 7:
            executar_analise(sys.argv[2:])
        else:
            raise IndexError
    except (IndexError, ValueError):
        print("Erro: Modo ou argumentos inválidos.", file=sys.stderr)
        print("Uso --buscar: <funcao> <A> <B> <passo>", file=sys.stderr)
        print("Uso --analisar: <funcao> <A> <B> <tol> <max_iter>", file=sys.stderr)
        exit(1)