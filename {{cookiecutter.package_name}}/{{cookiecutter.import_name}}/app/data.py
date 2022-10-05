import json
import os

import requests


def download(job_id):

    storage_host = os.environ.get("STORAGE_API_SERVICE_HOST", "storage")
    storage_port = os.environ.get("STORAGE_API_SERVICE_PORT", "8070")
    url = f"http://{storage_host}:{storage_port}/internal/download?name=trame/vis/{job_id}.json"
    auth_secret = os.environ.get("INTERNAL_AUTH_SHARED_SECRET")
    r = requests.get(url, headers={"Authorization": auth_secret},)

    data = r.json()
    print("downloading from ....", url)
    return data["data"]["params"][0]["value"]
