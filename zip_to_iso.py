import zipfile
import os
import pycdlib
import re


def zip_to_iso(zip_path, iso_path, temp_dir):
    # 1. Извлечение файлов из ZIP-архива во временную директорию
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    # 2. Создание ISO-образа из извлеченных файлов
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3)

    # Функция для добавления директорий
    def add_directory_structure(iso, relpath):
        parts = relpath.strip("/").split("/")
        for i in range(1, len(parts) + 1):
            dir_path = "/" + "/".join(parts[:i]).upper()
            try:
                iso.add_directory(dir_path)
            except pycdlib.pycdlibexception.PyCdlibInvalidInput:
                # Игнорируем ошибку, если папка уже существует
                pass

    # Функция для приведения имени к формату ISO9660
    def sanitize_iso_name(name):
        # Разделяем имя файла и его расширение
        base_name, ext = os.path.splitext(name)

        # Преобразуем имя файла
        base_name = base_name.upper()
        base_name = re.sub(
            r"[^A-Z0-9_]", "_", base_name
        )  # Заменяем неподходящие символы на '_'
        if len(base_name) > 31:  # Ограничиваем длину имени до 31 символа
            base_name = base_name[:31]

        # Возвращаем преобразованное имя файла с расширением
        return base_name + ext

    # Проходим по всем файлам и добавляем их в ISO
    for root, dirs, files in os.walk(temp_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            rel_path = os.path.relpath(file_path, temp_dir).replace(os.sep, "/").upper()

            # Применяем обработку имени файла для ISO9660
            sanitized_parts = [sanitize_iso_name(part) for part in rel_path.split("/")]
            iso_path_in_iso = "/" + "/".join(sanitized_parts)

            # Создаем необходимые директории
            add_directory_structure(iso, os.path.dirname(iso_path_in_iso))

            # Добавляем файл
            iso.add_file(file_path, iso_path_in_iso)

    # 3. Закрытие и сохранение ISO-образа
    iso.write(iso_path)
    iso.close()

    print(f"ISO файл '{iso_path}' успешно создан из '{zip_path}'.")


# Пример использования
zip_file = "ai25front.zip"  # Путь к исходному zip файлу
iso_file = "front.iso"  # Имя и путь для создаваемого ISO
temp_directory = "temp_extracted"  # Временная папка для извлечения файлов

# Создаем временную директорию, если она еще не существует
os.makedirs(temp_directory, exist_ok=True)

# Конвертируем ZIP в ISO
zip_to_iso(zip_file, iso_file, temp_directory)

# Удаляем временную директорию после создания ISO
import shutil

shutil.rmtree(temp_directory)
