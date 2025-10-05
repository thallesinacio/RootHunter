# Calculadora de Raízes - Métodos Numéricos

Este programa é uma ferramenta de linha de comando, escrita em Python, para encontrar as raízes de funções matemáticas. Utilizando uma abordagem interativa, o programa primeiro localiza intervalos onde as raízes existem e depois aplica quatro métodos numéricos distintos para calcular o valor da raiz com alta precisão.

## Funcionalidades

### Análise de Função Dinâmica: O usuário pode inserir qualquer função matemática em formato de texto.

Busca Automática de Intervalos: Escaneia um intervalo grande (macro) para encontrar sub-intervalos (micro) que garantidamente contêm uma raiz.

Cálculo Automático de Derivada: Utiliza a biblioteca SymPy para calcular a derivada da função inserida, eliminando a necessidade de cálculo manual para o método de Newton-Raphson.

Chutes Iniciais Inteligentes: Usa o intervalo selecionado pelo usuário para gerar automaticamente chutes iniciais otimizados para os métodos de Newton-Raphson e da Secante.

Comparação de Métodos: Aplica e exibe os resultados dos seguintes métodos:

Método da Bissecção

Método da Falsa Posição

Método de Newton-Raphson

Método da Secante
