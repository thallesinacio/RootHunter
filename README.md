# Calculadora de Raízes - Métodos Numéricos

Este programa é uma ferramenta de linha de comando, escrita em Python, para encontrar as raízes de funções matemáticas. Utilizando uma abordagem interativa, o programa primeiro localiza intervalos onde as raízes existem e depois aplica quatro métodos numéricos distintos para calcular o valor da raiz com alta precisão.

## Funcionalidades

  Análise de Função Dinâmica: O usuário pode inserir qualquer função matemática em formato de texto.

  Busca Automática de Intervalos: Escaneia um intervalo grande (macro) para encontrar sub-intervalos (micro) que garantidamente contêm uma raiz.

  Cálculo Automático de Derivada: Utiliza a biblioteca SymPy para calcular a derivada da função inserida, eliminando a necessidade de cálculo manual para o método de Newton-Raphson.

  Chutes Iniciais Inteligentes: Usa o intervalo selecionado pelo usuário para gerar automaticamente chutes iniciais otimizados para os métodos de Newton-Raphson e da Secante.

  Comparação de Métodos: Aplica e exibe os resultados dos seguintes métodos:

    1. Método da Bissecção

    2. Método da Falsa Posição

    3. Método de Newton-Raphson

    4. Método da Secante

  ## Como Usar o Programa

  ### Passo 1: Inserir a Função
  
    O programa pedirá para você digitar a função f(x) que deseja analisar. Você deve usar a sintaxe do Python.

  ### Passo 2: Definir o Intervalo de Busca
  
    Em seguida, você definirá um intervalo "macro" onde o programa procurará por raízes. Insira os dois números que definem o início e o fim do intervalo, separados por um espaço.

  ### Passo 3: Definir o Passo da Busca
  
    O "passo" define a precisão da busca por intervalos. Um valor menor é mais preciso, mas pode ser mais lento. Um bom valor inicial é 0.1.

  ### Passo 4: Escolher o Micro Intervalo
  
    O programa irá escanear o intervalo macro e exibir uma lista de todos os sub-intervalos onde encontrou uma mudança de sinal, indicando a presença de uma raiz.

  ### Passo 5: Análise dos Resultados
  
    Após sua escolha, o programa fará o cálculo da raíz no intervalo selecionado pelos 4 métodos. 
