import json
import os
import asyncio
import tempfile
from storage.gcp import VolatileStorage


async def download(job_id):
    bucket_folder = os.environ.get("BUCKET_FOLDER", "dev")
    vs = VolatileStorage()

    temp_dir = tempfile.mkdtemp()
    print("temp_dir", temp_dir)
    await vs.download(f"{bucket_folder}/{job_id}/file_info.json", f"{temp_dir}/file_info.json")
    with open(f"{temp_dir}/file_info.json", "rb") as f:
        file_info = json.load(f)
        calc_id = file_info["calculator"]
        print(f"downloading file_info for {calc_id}")
        files = file_info["files"]
        vs = VolatileStorage()
        file_names = []
        for file in files:
            await vs.download(f"{bucket_folder}/{job_id}/{file}", f"{temp_dir}/{file}")
            file_names.append(f"{temp_dir}/{file}")
        file_info["FileNames"] = file_names
        return file_info


if __name__ == "__main__":
    asyncio.run(download("fd867cd7-c7ed-4b85-9f98-443dcc20ba43"))
