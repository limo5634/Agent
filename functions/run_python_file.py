import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Prüfen, ob file_path innerhalb des working_directory liegt
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Prüfen, ob die Datei existiert
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'

        # Prüfen, ob es eine Python-Datei ist
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        # Python-Datei ausführen
        result = subprocess.run(
            ['python3', abs_file_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        output = ''

        if stdout:
            output += f'STDOUT:\n{stdout}\n'
        if stderr:
            output += f'STDERR:\n{stderr}\n'
        if result.returncode != 0:
            output += f'Process exited with code {result.returncode}\n'

        if not output:
            output = 'No output produced.'

        return output.strip()

    except Exception as e:
        return f'Error: executing Python file: {str(e)}'
