import os

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Prüfen, ob file_path innerhalb des working_directory liegt
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Verzeichnis anlegen, falls es nicht existiert
        dir_name = os.path.dirname(abs_file_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # Datei schreiben (überschreiben)
        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'
