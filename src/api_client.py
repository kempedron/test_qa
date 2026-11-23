import json
import logging

import requests

log = logging.getLogger("api")


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.s = requests.Session()
        self.s.headers.update({"Content-Type": "application/json"})

    def _log(self, method, url, payload=None, resp=None):
        log.info("-" * 50)
        log.info(f"{method.upper()} {url}")
        if payload is not None:
            log.info(f"payload: {payload}")
        if resp is not None:
            try:
                body = resp.json()
            except ValueError:
                body = resp.text
            log.info(f"{resp.status_code} {body}")
        log.info("-" * 50)

    def _req(self, method, path, payload=None):
        url = self.base_url + path
        r = self.s.request(method, url, json=payload, timeout=10)
        self._log(method, url, payload=payload, resp=r)
        return r

    def get_students(self):
        return self._req("GET", "/student")

    def get_student(self, sid):
        return self._req("GET", f"/student/{sid}")

    def create_student(self, data):
        return self._req("POST", "/student", payload=data)

    def update_student(self, sid, data):
        return self._req("PUT", f"/student/{sid}", payload=data)

    def delete_student(self, sid):
        return self._req("DELETE", f"/student/{sid}")
