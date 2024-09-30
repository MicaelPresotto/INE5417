

---

# Yaniv

Este é um jogo de cartas **Yaniv** implementado em Python 3. Yaniv é um jogo estratégico, rápido e fácil de aprender, muito popular em Israel e em outros países. É jogado com um baralho padrão, geralmente por 2 a 4 jogadores, onde o objetivo é reduzir o valor das cartas na sua mão para ser o primeiro a declarar "Yaniv".

## Regras Gerais

1. **Objetivo do Jogo**: 
   O objetivo principal é reduzir o valor total das cartas na sua mão para um número abaixo ou igual a 6. Quando você acredita que tem o menor valor, pode declarar "Yaniv".
   Se outro jogador tiver um valor igual ou menor, ele pode declarar "Yaniv" e vencer a rodada.

3. **Valor das Cartas**:
   - Cartas numéricas (2-10): Valem seus respectivos valores.
   - Ás: Vale 1 ponto.
   - Valete, Dama e Rei: Valem 11, 12 e 13 pontos, respectivamente.
   - Jokers: Tem valor 0.

4. **Rodadas**:
   - Cada jogador começa com cinco cartas.
   - O baralho é colocado no centro com uma pilha de descarte ao lado.
   - A cada turno, um jogador pode:
     - Comprar uma carta do baralho ou da pilha de descarte.
     - Descartar uma ou mais cartas (podem ser sequências ou grupos de cartas iguais).
     - Declarar "Yaniv" se o valor total de sua mão for menor ou igual ao limite de 6 pontos.

5. **Declaração de Yaniv**:
   - Se você declarar "Yaniv", a rodada acaba e todos os jogadores revelam suas cartas.
   - Se alguém tiver um valor de cartas menor ou igual ao seu, você toma uma penalidade de 30 pontos.
   - Se ninguém tiver um valor menor, todos recebem uma penalidade de 10 pontos.

6. **Pontuação**:
   - O vencedor da rodada soma os pontos das cartas de todos os outros jogadores.
   - O jogo continua até que um jogador atinja um limite de 100 pontos, e o vencedor é aquele com a menor pontuação.

7. **Dinâmica de Descarte**:
   - Você pode descartar cartas únicas ou grupos, como pares, trios, ou sequências de cartas do mesmo naipe.
   - Descartar sequências ou grupos ajuda a reduzir o valor de sua mão mais rapidamente.

## Como Jogar

1. Clone este repositório.
2. O jogo tem suporte para jogar de forma online, ou seja, é possível jogar com outra pessoa que também clonou o repositório.
3. Por início, após clonar o repositório execute:
  ```bash
  pip install -r requirements.txt
``` 
4. Para executar o programa, basta entrar na pasta src/ e executar:
```bash
python3 main.py
```
5. Coloque seu nome e o jogo irá conectar-se automaticamente com a outra pessoa que também executou o programa. Bom jogo!
