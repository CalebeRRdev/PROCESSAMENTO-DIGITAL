# Análise de imagem de câncer de mama para inferir presença ou ausência de câncer

import cv2
import numpy as np

# Carregando a imagem pré-processada com contornos e contraste realçado
imagem_cv2 = cv2.imread('mama_contornos_final.jpg', cv2.IMREAD_GRAYSCALE)

# Calculando o número de pixels brancos e pretos
numero_pixels_branco = np.sum(imagem_cv2 == 255)
numero_pixels_preto = np.sum(imagem_cv2 == 0)

# Calculando o percentual de pixels brancos
percentual_pixels_brancos = numero_pixels_branco / (numero_pixels_branco + numero_pixels_preto) * 100

# Inferindo a presença de câncer com base no percentual de pixels brancos
if percentual_pixels_brancos >= 30:
    print('Imagem com câncer')
else:
    print('Imagem sem câncer')

print(f'Percentual de pixels brancos: {percentual_pixels_brancos:.2f}%')


