import os

def get_files_info(working_directory, directory=None):
    try:
        # Wenn directory None ist, soll das working_directory gelistet werden
        if directory is None:
            directory = "."
        # Absoluten Pfad zum Zielverzeichnis berechnen
        abs_working_dir = os.path.abspath(working_directory)
        abs_directory = os.path.abspath(os.path.join(working_directory, directory))

        # Prüfen, ob das Zielverzeichnis innerhalb des working_directory liegt
        if not abs_directory.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Prüfen, ob das Zielverzeichnis ein Verzeichnis ist
        if not os.path.isdir(abs_directory):
            return f'Error: "{directory}" is not a directory'

        # Verzeichnisinhalt auflisten
        result_lines = []
        for name in sorted(os.listdir(abs_directory)):
            item_path = os.path.join(abs_directory, name)
            is_dir = os.path.isdir(item_path)
            # Für Verzeichnisse ist die Größe oft 0, für Dateien echte Größe
            size = os.path.getsize(item_path) if os.path.isfile(item_path) else 0
            result_lines.append(f'- {name}: file_size={size} bytes, is_dir={is_dir}')
        return '\n'.join(result_lines)
    except Exception as e:
        return f'Error: {str(e)}'


from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
