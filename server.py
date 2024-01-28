import socket
import threading


credentials = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'password3',
    'user4': 'password4',
    'user5': 'password5'
}

# Lista połączonych klientów
connected_clients = {}


# Funkcja obsługująca połączenie z danym klientem
def handle_client(client_socket, client_address):
    print(f"Połączono z {client_address}")

    # Logowanie klienta
    logged_in = False
    while not logged_in:
        login = client_socket.recv(1024).decode('utf-8')
        password = client_socket.recv(1024).decode('utf-8')

        if login in credentials and credentials[login] == password:
            client_socket.sendall(b"OK")
            logged_in = True
            print(f"Zalogowano: {login}")
            connected_clients[login] = client_socket
        else:
            client_socket.sendall(b"Invalid credentials")

    # Obsługa komunikacji z klientem
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Otrzymane dane od klienta {client_address}: {message}")

            if message.lower() == 'exit':
                print(f"Zamykanie połączenia z klientem {client_address}...")
                break

            # Wysyłanie wiadomości do wszystkich klientów
            for username, socket_conn in connected_clients.items():
                if username != login:
                    try:
                        socket_conn.sendall(data)
                    except socket.error:
                        # Jeśli wysyłanie nie powiedzie się, usuwamy klienta z listy połączonych
                        del connected_clients[username]
        except Exception as e:
            print(f"Błąd obsługi klienta {client_address}: {e}")
            break

    client_socket.close()
    del connected_clients[login]
    print(f"Zamknięto połączenie z klientem {client_address}")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('10.206.0.76', 55128)
server_socket.bind(server_address)
server_socket.listen(5)

print("Czekam na połączenia...")

while True:
    client_socket, client_address = server_socket.accept()

    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()