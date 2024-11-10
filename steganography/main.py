#lembrando que precisa escrever o nome da img e seu tipo ".png"

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from stegano import lsb
from PIL import Image
import hashlib
import os

# Função para gerar as chaves públicas e privadas RSA
def gerar_chaves_rsa():
    chave_privada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    chave_publica = chave_privada.public_key()
    
    # Serializar a chave privada para PEM
    chave_privada_pem = chave_privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serializar a chave pública para PEM
    chave_publica_pem = chave_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return chave_publica_pem, chave_privada_pem

# Função para encriptar o texto usando chave pública
def encriptar_texto(chave_publica_pem, texto):
    chave_publica = serialization.load_pem_public_key(chave_publica_pem, backend=default_backend())
    
    texto_encriptado = chave_publica.encrypt(
        texto.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return texto_encriptado

# Função para decriptar o texto usando chave privada
def decriptar_texto(chave_privada_pem, texto_encriptado):
    chave_privada = serialization.load_pem_private_key(chave_privada_pem, password=None, backend=default_backend())
    
    texto_decriptado = chave_privada.decrypt(
        texto_encriptado,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return texto_decriptado.decode("utf-8")

# Função para embutir o texto em uma imagem
def embutir_texto(imagem_path, texto, imagem_saida_path):
    secret = lsb.hide(imagem_path, texto)  
    secret.save(imagem_saida_path)          
    print("Texto embutido com sucesso!")

# Função para recuperar o texto de uma imagem
def recuperar_texto(imagem_path):
    texto_recuperado = lsb.reveal(imagem_path)  
    return texto_recuperado

# Função para gerar o hash de uma imagem
def gerar_hash(imagem_path):
    with open(imagem_path, "rb") as img_file:
        img_data = img_file.read()
        img_hash = hashlib.sha256(img_data).hexdigest() 
    return img_hash


def menu():
    chave_publica_pem, chave_privada_pem = gerar_chaves_rsa() 
    
    while True:
        print("\nMenu:")
        print("(1) Embutir texto em uma imagem usando Steganography")
        print("(2) Recuperar texto de uma imagem modificada com Steganography")
        print("(3) Gerar o hash das imagens original e alterada")
        print("(4) Encriptar a mensagem usando chave pública")
        print("(5) Decriptar a mensagem usando chave privada")
        print("(S ou s) para sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            imagem_path = input("Digite o caminho da imagem: ")
            texto = input("Digite o texto para embutir: ")
            imagem_saida_path = input("Digite o caminho para salvar a imagem alterada: ")
            embutir_texto(imagem_path, texto, imagem_saida_path)
        
        elif opcao == "2":
            imagem_path = input("Digite o caminho da imagem: ")
            texto = recuperar_texto(imagem_path)
            print("Texto recuperado:", texto)
        
        elif opcao == "3":
            imagem_path_original = input("Digite o caminho da imagem original: ")
            imagem_path_alterada = input("Digite o caminho da imagem alterada: ")
            hash_original = gerar_hash(imagem_path_original)
            hash_alterada = gerar_hash(imagem_path_alterada)
            print(f"Hash da imagem original: {hash_original}")
            print(f"Hash da imagem alterada: {hash_alterada}")
        
        elif opcao == "4":
            texto = input("Digite o texto para encriptar: ")
            texto_encriptado = encriptar_texto(chave_publica_pem, texto)
            print("Texto encriptado:", texto_encriptado)
        
        elif opcao == "5":
            encrypted_text = input("Digite o texto encriptado para decriptar: ")
            
         
            encrypted_bytes = eval(encrypted_text) 
            
            original_text = decriptar_texto(chave_privada_pem, encrypted_bytes)
            print("Texto decriptado:", original_text)
        
        elif opcao.lower() == "s":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


menu()