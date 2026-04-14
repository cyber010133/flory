import socket
import time
import sys

def iniciar_agente():
    # CONFIGURAÇÃO: Coloque o IP do seu computador/controlador aqui
    # Se estiver no mesmo Wi-Fi, será algo como 192.168.x.x
    SERVER_IP = "192.168.0.10" 
    PORT = 9999
    
    # Identificador único para cada celular (ex: Celular_1, Celular_2)
    ID_DISPOSITIVO = socket.gethostname()

    while True:
        try:
            print(f"[*] Tentando conectar em {SERVER_IP}...")
            
            # Criando a conexão TCP
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, PORT))
            
            # Enviando o comando de registro que o seu controlador exige
            registro = f"REGISTER {ID_DISPOSITIVO}"
            s.send(registro.encode('utf-8'))
            
            print(f"[+] Conectado com sucesso como: {ID_DISPOSITIVO}")

            # Mantém a conexão aberta e escuta comandos
            while True:
                dados = s.recv(1024).decode('utf-8')
                if not dados:
                    break
                print(f"[*] Comando recebido: {dados}")
                
        except Exception as e:
            print(f"[!] Erro: {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)
        finally:
            s.close()

if __name__ == "__main__":
    iniciar_agente()
