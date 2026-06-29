import os
import re
import zipfile
import io
from pathlib import Path

def create_zip_in_memory(directory: str) -> io.BytesIO:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory)
                zipf.write(file_path, arcname)
    zip_buffer.seek(0)
    return zip_buffer

def sanitize_filename(filename: str) -> str:
    filename = filename.replace('/', '_').replace('\\', '_')
    filename = ''.join(c for c in filename if ord(c) >= 32 or ord(c) == 10)
    filename = re.sub(r'[<>:"|?*]', '', filename)
    return filename
