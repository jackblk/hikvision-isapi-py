import os

from dotenv import load_dotenv

load_dotenv()

from hikvision_isapi import HikvisionClient

hikvision_client = HikvisionClient(
    base_url=os.getenv("HIK_URL", ""),
    username=os.getenv("HIK_USERNAME", ""),
    password=os.getenv("HIK_PASSWORD", ""),
)

# res = hikvision_client.remote_control_door(door_id="1", command="close")
res = hikvision_client.remote_control_door(door_id="1", command="alwaysOpen")
print(res.status_code)
