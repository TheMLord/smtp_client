from SMTP_client import SMTPClient
from file_operations import FileOperation


def main():
    client_smtp = SMTPClient(FileOperation.read_json_file("config.json"))
    client_smtp.send_message()


if __name__ == "__main__":
    main()
