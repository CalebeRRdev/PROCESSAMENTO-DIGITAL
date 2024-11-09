# Separação de imagem colorida entre os canais vermelho, verde e azul (RGB)

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Carregando a imagem
imagem_cachorro = cv2.imread('Bernese_Mountain_Dog.jpg')

# Separação dos canais de cor (RGB)
azul, verde, vermelho = cv2.split(imagem_cachorro)

# Criando imagens dos canais separados
blank = np.zeros(imagem_cachorro.shape[:2], dtype='uint8')
canal_azul = cv2.merge([azul, blank, blank])
canal_verde = cv2.merge([blank, verde, blank])
canal_vermelho = cv2.merge([blank, blank, vermelho])

# Exibindo as imagens separadas dos canais RGB
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(cv2.cvtColor(canal_vermelho, cv2.COLOR_BGR2RGB))
axes[0].set_title('Canal Vermelho')
axes[1].imshow(cv2.cvtColor(canal_verde, cv2.COLOR_BGR2RGB))
axes[1].set_title('Canal Verde')
axes[2].imshow(cv2.cvtColor(canal_azul, cv2.COLOR_BGR2RGB))
axes[2].set_title('Canal Azul')

for ax in axes:
    ax.axis('off')

plt.show()

# Salvando os canais em arquivos
cv2.imwrite('canal_vermelho.jpg', canal_vermelho)
cv2.imwrite('canal_verde.jpg', canal_verde)
cv2.imwrite('canal_azul.jpg', canal_azul)
