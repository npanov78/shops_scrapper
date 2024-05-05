from config.config import *


def read_urls(handler: str) -> list[str]:
    """
    Функция считывает url для поиска из файла и возвращает
    список url
    :param handler: имя сайта
    :return: list строк с url для поиска
    """
    file_path = f"{project_path}/config/{handler}-urls.txt"
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls


def should_exclude(name: str) -> bool:
    """
    Функция проверяет исключенные позиции.
    :param name: имя позиции
    :return: исключена ли позиция
    """
    return any(keyword.lower() in name.lower() for keyword in exclude)

