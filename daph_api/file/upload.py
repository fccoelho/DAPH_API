from hashlib import md5

def upload_file(file_bytes: bytes):
    name = md5(file_bytes).hexdigest()
    path = f"files/{name}.pdf"

    with open(path, "wb") as file:
        file.write(file_bytes)

    return path
