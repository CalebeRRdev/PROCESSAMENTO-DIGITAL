# Pré-processamento de imagem de câncer de mama

from PIL import Image, ImageDraw, ImageEnhance
from skimage import measure
import numpy as np
import matplotlib.pyplot as plt

# Carregando a imagem de câncer de mama
imagem_mama = Image.open('mama.jpg')

# Convertendo a imagem para tons de cinza
imagem_cinza = imagem_mama.convert('L')

# Convertendo a imagem para uma matriz numpy
matriz_imagem = np.array(imagem_cinza)

# Encontrando contornos usando a função find_contours da skimage
contornos = measure.find_contours(matriz_imagem, 0.8)

# Desenhando os contornos na imagem
desenhar = ImageDraw.Draw(imagem_mama)
for contorno in contornos:
    for i in range(len(contorno) - 1):
        desenhar.line(
            (
                contorno[i][1],
                contorno[i][0],
                contorno[i + 1][1],
                contorno[i + 1][0],
            ),
            fill='red',
            width=2,
        )

# Realçando o contraste da imagem
realcar = ImageEnhance.Contrast(imagem_mama)
imagem_realcada = realcar.enhance(15.5)

# Salvando a imagem final
imagem_realcada.save('mama_contornos_final.jpg')

# Exibindo a imagem resultante
plt.imshow(imagem_realcada, cmap='gray')
plt.title('Imagem com Contornos e Contraste Aumentado')
plt.axis('off')
plt.show()
