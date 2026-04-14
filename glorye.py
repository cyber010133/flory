import socket
import time
import sys

def iniciar_agente():
    # Pergunta o IP ao abrir o script no celular
    print("=== CONFIGURAÇÃO DO AGENTE ===")
    SERVER_IP = input("Digite o IP do Controlador (ex: 192.168.0.10): ").strip()
    PORT = 9999
    
    # Identificador único baseado no nome do celular
    ID_DISPOSITIVO = socket.gethostname()

    while True:
        try:
            print(f"\n[*] Tentando conectar em {SERVER_IP}:{PORT}...")
            
            # Criando o socket TCP
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Define um timeout para não ficar travado se o IP estiver errado
            s.settimeout(10) 
            s.connect((SERVER_IP, PORT))
            s.settimeout(None) # Remove o timeout após conectar
            
            # Envia o registro para o seu controlador aparecer na lista
            registro = f"REGISTER {ID_DISPOSITIVO}"
            s.send(registro.encode('utf-8'))
            
            print(f"[+] Conectado com sucesso! ID: {ID_DISPOSITIVO}")

            # Loop de escuta de comandos
            while True:
                dados = s.recv(1024).decode('utf-8')
                if not dados:
                    print("[-] Conexão encerrada pelo servidor.")
                    break
                print(f"[*] Comando recebido: {dados}")
                
        except Exception as e:
            print(f"[!] Erro de conexão: {e}")
            print("[!] Tentando reconectar em 5 segundos...")
            time.sleep(5)
        finally:
            try:
                s.close()
            except:
                pass

if __name__ == "__main__":
    iniciar_agente()
