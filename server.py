import socket
import time

HOST = ''         # Listen on all interfaces
PORT = 22      # Must match the port in your ESP8266 code

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(1)
            print(f"Listening on port {PORT}...")
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                print('Received device IP:', data.decode())
                # wait for a moment before sending command
                time.sleep(3)
                # try sending ALERT command
                try:
                    # answer to the same device IP and port
                    alert_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    alert_socket.sendto(b'info', (data.decode(), PORT))
                    print('Sent info command to device.')
                    time.sleep(10)  # wait before next command for 10 seconds
                    print('Sent second ALERT command to device.')
                    alert_socket.sendto(b'ALERT\n', (data.decode(), PORT))
                    alert_socket.close()
                except Exception as e:
                    print('Error sending command:', e)
    except KeyboardInterrupt:
        print("Server shutting down.")
        break