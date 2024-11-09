# Importar o módulo de upload de arquivos
from google.colab import files

# Fazer upload da imagem para o Colab
uploaded = files.upload()

# Instalar pacotes necessários (se ainda não estiverem instalados)

!pip install cryptography pillow

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from PIL import Image
import numpy as np
import hashlib

# Função para embutir texto em uma imagem (Steganography)
def embed_text_in_image(image_path, output_image_path, text):
    image = Image.open(image_path)
    image = image.convert('RGB')
    data = np.array(image)

    text_bin = ''.join(format(ord(char), '08b') for char in text) + '1111111111111110'
    h, w, _ = data.shape
    index = 0

    for i in range(h):
        for j in range(w):
            if index < len(text_bin):
                r, g, b = data[i, j]
                r = (r & ~1) | int(text_bin[index])
                data[i, j] = [r, g, b]
                index += 1
            else:
                break
        if index >= len(text_bin):
            break

    result_image = Image.fromarray(data)
    result_image.save(output_image_path)
    print("\n\tTexto embutido na imagem com sucesso!")

# Função para recuperar texto de uma imagem (Steganography)
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    data = np.array(image)

    text_bin = ''
    for i in data:
        for j in i:
            r, _, _ = j
            text_bin += str(r & 1)

    text = ''.join(chr(int(text_bin[i:i + 8], 2)) for i in range(0, len(text_bin), 8))
    end_marker = text.find('\xFF\xFE')
    if end_marker != -1:
        text = text[:end_marker]
    else:
        text = text.split("\x00", 1)[0]  # Parar na primeira ocorrência de \x00 como uma alternativa

    print("\n\tTexto recuperado da imagem:")
    print(text)

# Função para gerar hash de uma imagem
def generate_hash(image_path):
    with open(image_path, "rb") as f:
        bytes = f.read()
        hash = hashlib.sha256(bytes).hexdigest()
    print(f"\n\tHash da imagem ({image_path}): {hash}")

# Função para encriptar mensagem
def encrypt_message(public_key, message):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print("\n\tMensagem encriptada com sucesso!")
    # Retornar a mensagem encriptada em formato hexadecimal para facilitar a visualização
    encrypted_hex = encrypted.hex()
    print("\n\tMensagem encriptada (em hexadecimal):", encrypted_hex)
    return encrypted_hex

# Função para decriptar mensagem
def decrypt_message(private_key, encrypted_message_hex):
    encrypted_message = bytes.fromhex(encrypted_message_hex)
    decrypted = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print("\n\tMensagem decriptada com sucesso!")
    return decrypted.decode()

# Gerar chave pública e privada
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# Loop do menu de opções
while True:
    print("\n\tMenu de opções:")
    print("\n\n\t(1) Embutir texto em uma imagem (Steganography)")
    print("\n\t(2) Recuperar texto de uma imagem (Steganography)")
    print("\n\t(3) Gerar hash de imagens")
    print("\n\t(4) Encriptar mensagem")
    print("\n\t(5) Decriptar mensagem")
    print("\n\t(S ou s) Sair")

    option = input("\n\tEscolha uma opção: ").strip()

    if option == '1':
        image_path = input("\n\tDigite o caminho da imagem original: ").strip()
        output_image_path = input("\n\tDigite o caminho para salvar a imagem alterada: ").strip()
        text = input("\n\tDigite o texto a ser embutido: ")
        embed_text_in_image(image_path, output_image_path, text)

    elif option == '2':
        image_path = input("\n\tDigite o caminho da imagem alterada: ").strip()
        extract_text_from_image(image_path)

    elif option == '3':
        image_path_original = input("\n\tDigite o caminho da imagem original: ").strip()
        image_path_altered = input("\n\tDigite o caminho da imagem alterada: ").strip()
        generate_hash(image_path_original)
        generate_hash(image_path_altered)

    elif option == '4':
        message = input("\n\tDigite a mensagem a ser encriptada: ")
        encrypted_message_hex = encrypt_message(public_key, message)
        print("\n\tMensagem encriptada (em hexadecimal):", encrypted_message_hex)

    elif option == '5':
        encrypted_message_hex = input("\n\tDigite a mensagem encriptada em hexadecimal: ")
        decrypted_message = decrypt_message(private_key, encrypted_message_hex)
        print("\n\tMensagem decriptada:", decrypted_message)

    elif option.lower() == 's':
        print("\n\tEncerrando a aplicação. Até mais!")
        break

    else:
        print("\n\tOpção inválida. Tente novamente.")