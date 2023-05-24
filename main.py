"""Модуль с функцией main"""
import argparse
import os.path

from SMTP_client import SMTPClient
from file_operations import FileOperation


def main():
    """Функция main

    Создает объект класса SMTPClient и запускает отправку сообщений.
    """
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument("--config", type=str, help="путь до файла конфигурации", required=True)
        parser.add_argument("--password", type=str, help="путь до файла с паролем", required=True)
        parser.add_argument("--msg", type=str, help="путь до файла письмом", required=True)
        args = parser.parse_args()

        config_file = args.config
        password_file = args.password
        msg_file = args.msg

        if os.path.isfile(config_file) and os.path.isfile(password_file) \
                and os.path.isfile(msg_file):
            client_smtp = SMTPClient(
                FileOperation.read_json_file(config_file),
                password_file,
                msg_file
            )
            client_smtp.send_message()
        else:
            print("В качестве аргументов нужно указывать путь до файла")
    except SystemExit:
        print(f"Ошибка ввода аргументов")
        print("Введите еще раз")


if __name__ == "__main__":
    main()
