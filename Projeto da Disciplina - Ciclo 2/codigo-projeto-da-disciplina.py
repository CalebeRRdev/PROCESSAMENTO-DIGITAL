# Instalando pacotes necessários
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
    print("Texto embutido na imagem com sucesso!")

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
    print("Texto recuperado da imagem:")
    print(text)

# Função para gerar hash de uma imagem
def generate_hash(image_path):
    with open(image_path, "rb") as f:
        bytes = f.read()
        hash = hashlib.sha256(bytes).hexdigest()
    print(f"Hash da imagem ({image_path}): {hash}")

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
    print("Mensagem encriptada com sucesso!")
    return encrypted

# Função para decriptar mensagem
def decrypt_message(private_key, encrypted_message):
    decrypted = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print("Mensagem decriptada com sucesso!")
    return decrypted.decode()

# Gerar chave pública e privada
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# Loop do menu de opções
while True:
    print("\nMenu de opções:")
    print("(1) Embutir texto em uma imagem (Steganography)")
    print("(2) Recuperar texto de uma imagem (Steganography)")
    print("(3) Gerar hash de imagens")
    print("(4) Encriptar mensagem")
    print("(5) Decriptar mensagem")
    print("(S ou s) Sair")

    option = input("Escolha uma opção: ").strip()

    if option == '1':
        image_path = input("Digite o caminho da imagem original: ")
        output_image_path = input("Digite o caminho para salvar a imagem alterada: ")
        text = input("Digite o texto a ser embutido: ")
        embed_text_in_image(image_path, output_image_path, text)

    elif option == '2':
        image_path = input("Digite o caminho da imagem alterada: ")
        extract_text_from_image(image_path)

    elif option == '3':
        image_path_original = input("Digite o caminho da imagem original: ")
        image_path_altered = input("Digite o caminho da imagem alterada: ")
        generate_hash(image_path_original)
        generate_hash(image_path_altered)

    elif option == '4':
        message = input("Digite a mensagem a ser encriptada: ")
        encrypted_message = encrypt_message(public_key, message)
        print("Mensagem encriptada:", encrypted_message)

    elif option == '5':
        encrypted_message = bytes.fromhex(input("Digite a mensagem encriptada em hexadecimal: "))
        decrypted_message = decrypt_message(private_key, encrypted_message)
        print("Mensagem decriptada:", decrypted_message)

    elif option.lower() == 's':
        print("Encerrando a aplicação. Até mais!")
        break

    else:
        print("Opção inválida. Tente novamente.")