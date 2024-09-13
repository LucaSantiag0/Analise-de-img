from PIL import Image
import numpy as np

# Abrir a imagem
imagem = Image.open('gatodeoculos.png').convert('RGB')
imagem_np = np.array(imagem)

# Criar imagens de canais separados
red_channel = np.zeros_like(imagem_np)
green_channel = np.zeros_like(imagem_np)
blue_channel = np.zeros_like(imagem_np)

# Preencher os canais com os valores correspondentes
red_channel[:, :, 0] = imagem_np[:, :, 0]
green_channel[:, :, 1] = imagem_np[:, :, 1]
blue_channel[:, :, 2] = imagem_np[:, :, 2]

# Converter para imagens Pillow
red_img = Image.fromarray(red_channel)
green_img = Image.fromarray(green_channel)
blue_img = Image.fromarray(blue_channel)

# Salvar imagens
red_img.save('red_channel.png')
green_img.save('green_channel.png')
blue_img.save('blue_channel.png')
