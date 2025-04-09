# Analisador de Espectro Sonoro

## Descrição do projeto
O objetivo do projeto é implementar um sistema para analisar o espectro dos sons captados por um microfone e representá-los visualmente em um display OLED.

## Componentes utilizados
Para esse projeto, foi utilizado a placa BitDogLab que possui diversos recursos presentes. Porém, para esse projeto, foram utilizados:
* Microcontrolador Raspberry Pi Pico W - RP2040.
* Microfone - MAX4465.
* Display OLED 128x64.

## Linguagem utilizada
Para a programação da Pi Pico W, foi escolhida a linguagem MicroPython. Alguns ds motivos para tal escolha são:
* Simplicidade e familiaridade com a lingua;
* Não era necessária uma taxa de performance extremamente elevada;

A versão do MicroPython utilizada foi aquela que contia a biblioteca `ulab` diretamente, através do [link](https://github.com/v923z/micropython-builder/releases). Essa biblioteca possibilita os cálculos usados de forma rápida e eficiente, simulando a `Numpy` e `Scipy`.

## Adaptações feitas
Inicialmente, foi pensado em utilizar o DMA da Pico W para agilizar as operações e melhorar a performance do projeto. Porém, o MicroPython não possui suporte completo para o controle do DMA (não habilita a função de colocar intervalos nas medições do ADC) e como o desempenho não era uma questão crucial, foi escolhido utilizar uma abordagem mais simples com temporização a partir do `time.sleep_us`.

## Código
O código criado está disponível no arquivo main.py

`read_samples`:
Essa função recebe o número de amostras desejadas como parâmetro opcional (considera N = 256 como valor padrão) e retorna a frequência real das medições juntamente com  um array (lista) com os valores observados pelo ADC no microfone (normalizados para 0).

`calcular_fft`:
Recebe a lista de amostras a serem analisadas (retorno da função acima) em conjunto com o número de amostras e retorna a magnitude do resultado da operação FFT (*Fast Fourier Transform*) sobre o sinal (amostras).

`display_spectrum`:
Recebe o resultado da FFT, obtida acima, a frequência real do sinal e o número de amostras. Não possui retorno, sendo apenas para mostrar visualmente o resultado da FFT no display OLED.

Alguns pontos importantes sobre ele:
* Para a função `read_samples` foi calculado a frequência real das amostra devido a imprecisão do método `sleep_us` da biblioteca `time` do MicroPython.
    * Dessa forma, com fs = 40kHz, é obtida uma f_real de cerca de 20kHz.
* Na função `calcular_fft`, foi preferido a utilização da função `np.spectrogram` pelo seu uso reduzido de memória RAM e por já calcular diretamente o valor absoluto do espectro. 

## Resultados
Como apresentado nas imagens abaixo, temos que com o ajuste, a imprecisão foi muito reduzida para essa faixa de frequência.
* Onda senoidal:
![20250409_155122](https://github.com/user-attachments/assets/c1cd197f-c20e-45dc-a85b-975235ec0f63)
* Onda quadrada:
![Screenshot_20250409_163059_Gallery](https://github.com/user-attachments/assets/4b73a34c-7c81-42bd-9b42-b3ec6d187b13)


