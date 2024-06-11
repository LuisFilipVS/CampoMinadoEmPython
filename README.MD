# Campo Minado com PyQt5

Este é um projeto rápido que fiz utilizando totalmente a biblioteca PyQt do Python.
A biblioteca se mostrou eficiente e para trabalhar com cenários estáticos, ou seja, jogos de tabuleiro.

## Funcionamento do programa

* O programa inicializa com uma interface gráfica e aguarda o clique do usuário no botão ***Começar*** para carregar o frame de configurações do jogo, no qual pode ser selecionado o tamanho do campo e a quantidade de bombas que serão plantadas.

* O campo de jogo é uma matriz quadrada
* A princípio foi realizado algumas verificações para impedir que o usuário adicione informações fora da lógica, ou seja, não é possivel adicionar um campo menor do que o previsto ou maior do que a interface comporta. Além disso a quantidade de bombas tem que ser menor do que o quadrado do lado do campo desejado. Fora dessas condições ou mantendo os campos em branco, o jogo define um campo por padrão (Matriz 10x10 & 15 bombas)

## Instruções de Jogo

A área de jogo consiste num campo de quadrados retangular. Cada quadrado pode ser revelado clicando sobre ele, e se o quadrado clicado contiver uma bomba, então o jogo acaba. Se, por outro lado, o quadrado não contiver uma mina, uma de duas coisas poderá acontecer:

1. Um número aparece, indicando a quantidade de quadrados adjacentes que contêm bomba;
2. Nenhum número aparece. Neste caso, o jogo revela automaticamente os quadrados que se encontram adjacentes ao quadrado vazio, já que não podem conter bomba;

O jogo é ganho quando todos os quadrados que não têm bomba são revelados.


## Inicialização

* Primeiramente, instale as dependências necessárias contidos no arquivo requirements

~~~bash
pip install -r requirements.txt
~~~

* Inicialize o programa por meio do arquivo main.py, contido na raiz

~~~bash
python main.py
~~~

* Ao iniciar a interface gráfica aperte o botão ***Começar*** para abrir as configurações e aperte o botão ***Iniciar o jogo*** para começar o game.