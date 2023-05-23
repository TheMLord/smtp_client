import base64
import json
import os


class FileOperation:
    @staticmethod
    def read_txt_file(file_name: str):
        with open(file_name, "r", encoding="UTF-8") as file_txt:
            return file_txt.read().strip()

    @staticmethod
    def read_json_file(file_name: str):
        with open(file_name, "r", encoding="UTF-8") as file_json:
            return json.load(file_json)

    @staticmethod
    def get_send_type_file(type_file):
        if type_file == "txt":
            return "text/plain"
        elif type_file == "html":
            return "text/html"
        elif type_file == "jpg" or type_file == "jpeg" or type_file == "png" or type_file == "gif":
            return f"image/{type_file}"
        elif type_file == "mpeg" or type_file == "wav":
            return f"audio/{type_file}"
        elif type_file == "mp4" or type_file == "mpeg":
            return f"video/{type_file}"
        elif type_file == "pdf":
            return f"application/{type_file}"
        elif type_file == "doc":
            return "application/msword"
        elif type_file == "docx":
            return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif type_file == "xls":
            return "application/vnd.ms-excel"
        elif type_file == "xlsx":
            return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif type_file == "ppt":
            return "application/vnd.ms-powerpoint"
        elif type_file == "pptx":
            return "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        elif type_file == "zip":
            return "application/zip"
        else:
            return False

    @staticmethod
    def prepare_files(directory_path: str):
        dict_files_info = {}
        for file_name in os.listdir(directory_path):
            path_file = os.path.join(directory_path, file_name)
            if os.path.isfile(path_file):
                with open(path_file, "rb") as byte_file:
                    base64file = base64.b64encode(byte_file.read()).decode("UTF-8")
                type_file = FileOperation.get_send_type_file(os.path.splitext(file_name)[1][1:])
                if type_file:
                    dict_files_info[file_name] = [base64file, type_file]
                else:
                    print(f"файл {file_name} не распознан, отправлен не будет")

        return dict_files_info