import os
from urllib.parse import urlparse

import requests

AVAILABLE_EXT = [".csv"]


def loader(url, local_path):
    response = requests.get(url)
    if not response.ok:
        return response.status_code, response.reason

    filename = os.path.basename(urlparse(url).path)
    f_name, f_ext = os.path.splitext(filename)

    if f_ext not in AVAILABLE_EXT:
        return 0, "unsupported file extension"

    filepath = os.path.join(local_path, filename)
    suffix = 0

    while os.path.exists(filepath):
        suffix += 1
        filepath = os.path.join(local_path, f"{f_name}-{suffix}{f_ext}")

    with open(filepath, "w") as f:
        f.write(response.content.decode())

    return response.status_code, filepath
