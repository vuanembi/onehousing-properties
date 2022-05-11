import time

import httpx


def get_client():
    return httpx.Client(
        base_url="https://api.onehousing.vn/transaction-platform/v1/my-home/",
        timeout=None,
    )


def get_resource(client, resource: str, id: str):
    time.sleep(0.5)
    r = client.get(f"{resource}/{id}")
    if r.status_code == 429:
        time.sleep(10)
        return get_resource(client, resource, id)
    try:
        res = r.json()
        return res["data"]
    except:
        return []
