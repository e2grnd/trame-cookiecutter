import os

import requests


def download(job_id):

    storage_host = os.environ.get("STORAGE_API_SERVICE_HOST", "storage")
    storage_port = os.environ.get("STORAGE_API_SERVICE_PORT", "8070")
    url = f"http://{storage_host}:{storage_port}/e2g/download?name=trame/{{ cookiecutter.package_name }}/{job_id}.json"
    r = requests.get(url)

    data = r.json()
    print("downloading from ....", url)
    return data["data"]["params"][0]["value"]
