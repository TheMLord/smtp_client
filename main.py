"""Модуль с функцией main"""
from SMTP_client import SMTPClient
from file_operations import FileOperation


def main():
    """Функция main

    Создает объект класса SMTPClient и запускает отправку сообщений.
    """
    client_smtp = SMTPClient(FileOperation.read_json_file("config.json"))
    client_smtp.send_message()


if __name__ == "__main__":
    main()
