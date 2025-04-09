# Importando as bibliotecas necessárias
from machine import ADC, Pin, SoftI2C
import ssd1306
from ulab import numpy as np
from ulab import utils as utils
import time

# Configuração do ADC para o microfone MAX4466
mic_pin = ADC(Pin(28))

# Parâmetros da FFT
N = 256 # Número de amostras
fs = 40000 # Frequência de amostragem

# Constantes do I2C
SCL_PIN = 15
SDA_PIN = 14

# Configuração do display OLED (I2C)
i2c = SoftI2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))  
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Função para capturar e guardar amostras do microfone a cada intervalo de amostragem
def read_samples(num_samples = N):
  samples = []
  start_time = time.ticks_us()
  for i in range(num_samples):
      samples.append((mic_pin.read_u16() >> 4) - 2048)  # Lê o valor do ADC e normaliza para centrá-lo em 0
      time.sleep_us(int(1e6 / fs))  
  end_time = time.ticks_us()
  T_real = (end_time - start_time) / 1e6
  f_real = num_samples / T_real
  return np.array(samples), f_real

# Função para calcular a FFT
def calcular_fft(samples, num_samples = N):
  magnitude = utils.spectrogram(samples)
  magnitude = magnitude[:num_samples//2]
  magnitude = magnitude / np.max(magnitude) * 64
 
  return magnitude
 
# Função para representar visualmente os dados da fft no display OLED
def display_spectrum(fft_result, f_real, num_samples = N):
  oled.fill(0)  # Limpa a tela
  freqs = np.linspace(0, f_real/2, num_samples//2)
  max_freq = freqs[np.argmax(fft_result)]
  oled.text(f"Max freq:{int(max_freq)}Hz", 0, 0)

  for i in range(0, len(fft_result)):
      oled.vline(i, int(76-fft_result[i]), 64, 1)

  oled.show()

# Loop principal
while True:
  samples, f_real = read_samples()
  fft_result = calcular_fft(samples)
  display_spectrum(fft_result, f_real)
