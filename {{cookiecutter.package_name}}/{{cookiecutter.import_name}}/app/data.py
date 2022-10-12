import os

import requests


def download(job_id):

    storage_host = os.environ.get("STORAGE_API_SERVICE_HOST", "storage-trame")
    storage_port = os.environ.get("STORAGE_API_SERVICE_PORT", "8070")
    bucket_folder = os.environ.get("BUCKET_FOLDER", "trame")
    url = f"http://{storage_host}:{storage_port}/internal/download?name={bucket_folder}/{{cookiecutter.package_name}}/{job_id}.json"
    auth_secret = os.environ.get("INTERNAL_AUTH_SHARED_SECRET")
    r = requests.get(
        url,
        headers={"Authorization": auth_secret},
    )

    spdw = r.json()
    print(spdw)
    print("downloading from ....", url)
    coneResolution = [x for x in spdw["data"]["params"] if x["name"] == "coneResolution"]
    return coneResolution[0]["value"]

