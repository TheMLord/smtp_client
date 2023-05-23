import base64
import random
import ssl
import socket

from file_operations import FileOperation


def send_request(client_socket: ssl.SSLSocket, data_request: str):
    client_socket.send((data_request + '\n').encode())
    receive_response(client_socket)


def receive_response(client_socket: ssl.SSLSocket):
    client_socket.settimeout(0.05)
    while True:
        try:
            recv_data = client_socket.recv(1024).decode("UTF-8")
            print(recv_data)
        except socket.timeout:
            break
    print(client_socket.recv(65535).decode("UTF-8"))


def generate_boundary():
    list_number = [n for n in range(0, 10)]
    random_number = ""
    for _ in range(6):
        random_number += str(random.choice(list_number))
    return f"bound.{random_number}"


class SMTPClient:
    def __init__(self, config_dict: dict):
        self.smtp_host = "smtp.yandex.ru"
        self.smtp_port = 465

        self.user_password = FileOperation.read_txt_file("password.txt")

        self.user_name_from = config_dict["from"]
        self.user_name_to_list = config_dict["to"]
        self.subject_message = config_dict["subject"]
        self.send_files_dict = FileOperation.prepare_files(config_dict["path_directory_files"])

    def message_prepare(self, user_name_to: str, text_message: str):
        boundary_msg = generate_boundary()

        # заголовки
        headers = f'from: {self.user_name_from}\n'
        headers += f'to: {user_name_to}\n'
        headers += f'subject: {self.subject_message}\n'
        headers += 'MIME-Version: 1.0\n'
        headers += 'Content-Type: multipart/mixed;\n' \
                   f'    boundary={boundary_msg}\n'

        # тело сообщения началось
        message_body = f'--{boundary_msg}\n'
        message_body += 'Content-Type: text/plain; charset=utf-8\n\n'
        message_body += text_message + '\n'
        message_body += f'--{boundary_msg}\n'
        for send_file in self.send_files_dict:
            message_body += f'Content-Disposition: attachment;\n' \
                            f'   filename={send_file}\n'
            message_body += 'Content-Transfer-Encoding: base64\n'
            message_body += f'Content-Type: {self.send_files_dict[send_file][1]};\n\n'
            message_body += self.send_files_dict[send_file][0] + '\n'
            message_body += f'--{boundary_msg}\n'

        message_body += f'--{boundary_msg}--'
        message = headers + '\n' + message_body + '\n.\n'
        return message

    def send_message(self):
        text_message = FileOperation.read_txt_file("msg.txt")

        base64login = base64.b64encode(self.user_name_from.encode()).decode()
        base64password = base64.b64encode(self.user_password.encode()).decode()

        ssl_contex = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_contex.check_hostname = False
        ssl_contex.verify_mode = ssl.CERT_NONE

        try:
            with socket.create_connection((self.smtp_host, self.smtp_port)) as sock:
                try:
                    with ssl_contex.wrap_socket(sock, server_hostname=self.smtp_host) as client:
                        receive_response(client)  # в smpt сервер первый говорит

                        send_request(client, f'ehlo {self.user_name_from}')
                        send_request(client, 'AUTH LOGIN')
                        send_request(client, base64login)
                        send_request(client, base64password)

                        for user_name_to in self.user_name_to_list:
                            send_request(client, f'MAIL FROM:{self.user_name_from}')
                            send_request(client, f"RCPT TO:{user_name_to}")
                            send_request(client, 'DATA')
                            send_request(client, self.message_prepare(user_name_to, text_message))
                except ssl.SSLError as e:
                    print(f"Ошибка SSL: {e}")
        except socket.error as e:
            print(f"Ошибка сокета: {e}")
