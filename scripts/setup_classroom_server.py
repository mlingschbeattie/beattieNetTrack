import os

target_dir = r"c:\CustomApps\26_27_ LessonsAndAgendas"
server_py_path = os.path.join(target_dir, "server.py")
start_bat_path = os.path.join(target_dir, "START_SERVER.bat")

server_code = """import http.server
import socketserver
import os
import socket

CANDIDATE_PORTS = [5000, 3000, 8088, 5500, 9000, 7777]
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "172.16.96.79"

class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def guess_type(self, path):
        if path.endswith('.pptx'):
            return 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        return super().guess_type(path)

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

if __name__ == "__main__":
    local_ip = get_ip()
    handler = CustomHTTPHandler
    httpd = None
    active_port = None

    for port in CANDIDATE_PORTS:
        try:
            httpd = ThreadingHTTPServer(("0.0.0.0", port), handler)
            active_port = port
            break
        except Exception:
            continue

    if not httpd:
        print("[!] ERROR: Could not bind to any candidate port.")
        exit(1)

    print("=" * 72)
    print("  BEATTIE-NET // LOCAL CLASSROOM SERVER IS ONLINE & ACCESSIBLE!")
    print("=" * 72)
    print(f"  [+] Host Machine:      http://localhost:{active_port}")
    print(f"  [+] Student Hub:       http://{local_ip}:{active_port}")
    print(f"  [+] Student Lab:       http://{local_ip}:{active_port}/activity.html")
    print(f"  [+] Slide Deck:        http://{local_ip}:{active_port}/presentation.html")
    print(f"  [+] PowerPoint PPTX:   http://{local_ip}:{active_port}/Divide_and_Conquer_Mastery.pptx")
    print("=" * 72)
    print("  Tell students to open: http://" + local_ip + f":{active_port}")
    print("=" * 72)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\nServer stopped.")
"""

bat_code = """@echo off
title Beattie-Net Classroom Server
color 0A
cls
echo ======================================================================
echo    BEATTIE-NET // STARTING CLASSROOM TROUBLESHOOTING SERVER
echo ======================================================================
python server.py
pause
"""

with open(server_py_path, "w", encoding="utf-8") as f:
    f.write(server_code)

with open(start_bat_path, "w", encoding="utf-8") as f:
    f.write(bat_code)

print("Updated server.py and START_SERVER.bat with multi-port auto-binding!")
