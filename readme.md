# Manual do limi

## Sobre
O limi é um interpretador de uma linguagem de programação minimalista sem nenhum propósito senão o de existir. É um projeto pessoal baseado (losely based) nas ideias do [Know-How Computer](https://en.wikipedia.org/wiki/WDR_paper_computer) e do [Infinite Abacus](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/A6EB7DD8D57056044CCB128923764BEB/S0008439500050967a.pdf/how_to_program_an_infinite_abacus.pdf).

## Funcionamento do interpretador

- Os comandos válidos de um programa são guardados em uma lista ordenada.
- Existe uma variável `CP` (Contador do programa) que guarda um inteiro `>= 0`.
- O valor de `CP` no início da execução é zero.
- O interpretador entra em um loop e executa um comando por iteração.
- Em cada iteração o comando indexado em `CP` na lista de comandos é executado.
- Em cada iteração o valor de `CP` é atualizado.
- O loop é encerrado ao encontrar o comando `F`.

## Operações válidas
Abaixo estão listadas todas as operações válidas.
- `+ X` -> Operação de **incremento** do valor no registrador `X`.
    - `R(X) += 1`
    - `CP += 1`
- `- X` -> Operação de **decremento** do valor no registrador `X`.
    - `R(X) -= 1`
    - `CP += 1`
- `P L` -> Operação de **pular** para uma linha com rótulo `L`.
    - `CP = L`
- `C X` -> Operação de **comparação** do valor `R(X)` no registrador `X`.
    - Se `R(X) <= 0`, então `CP += 2`
    - Se `R(X) > 0`, então `CP +=1`
- `E X` -> **Exibe** o valor `R(X)` na tela. Usado apenas para análise da execução do programa.
    - `print(R(X))`
    - `CP += 1`
- `F _` -> **Fim** da execução.

## Tokens de comando
Cada linha de comando pode conter 2 ou 3 tokens separados por um caractere de espaço.
- **Primeiro token**: é sempre uma operação (`+`, `-`, `P`, `C`, `F` ou `E`).
- **Segundo token**: é o argumento da operação. No caso das operações `+`, `-`, `C` ou `E` o token é um idenficador de registrador. No caso da operação `P` é um rótulo de linha. No caso da operaçã `F` é um token sem função.
- **Terceiro token**: algumas linhas de comando podem ter um terceiro token que é o rótulo para identificar a linha usado na operação `P`.

## Definição de registradores
Os registradores usados em um programa são definidos durante o pré-processamento do programa e guardados em uma lista chamada *registers*.

Todos os registradores podem apenas guardar valores inteiros (positivos, nulo ou negativos).

Todo programa inicializa com pelo menos um registrador no índice `0` de *registers*. O registrador no índice `0` é especial no sentido de que ele deve guardar, sempre que possível, os valores resultantes das funções.

Os demais registradores usados pelo programa devem ser declarados, preferencialmente, no início do programa usando a sintaxe de 3 tokens abaixo.

`R X V`

Onde `R` indica que a linha é uma declaração de registrador, `X` é um inteiro `> 0` identificador do registrador e `V` é o valor inicializado no registrador.

Os registradores devem ser identificados em ordem crescente e sequencial começando em 1.

Como exemplo de uma lista de registradores para um programa que soma 15 e 37 será inicializado como visto abaixo.

`R 1 15`

`R 2 37`

As duas linhas acima serão transformadas durante o pré-processamento na lista de registradores abaixo.

`registers = [0, 15, 37]`

## Estrutura de um programa
Um programa interpretado nessa linguagem tem extensão *.lmp* e deve ser dividido em duas partes: declaração dos registradores e lista de comandos.

A declaração dos registradores serve para que o estágio de pré-processamento do programa identifique todos os registradores usados no programa.

A lista de comandos é o programa em si. É uma lista de operações válidas. Cada operação é descrita em uma nova linha.

Linhas em branco serão ignoradas durante a análise sintática e removidas da lista de comandos.

Qualquer linha que não tenha 2 ou 3 tokens e que o primeiro token não seja reconhecido  (`R`, `+`, `-`, `P`, `C`, `F` ou `E`) será considerada como comentário, ignoradas durante a análise sintática e removidas da lista de comandos.