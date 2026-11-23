import logging

import allure
import pytest


class LogCapture(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(self.format(record))

    def get_log(self):
        return "\n".join(self.records)


@pytest.fixture
def log_capture():
    h = LogCapture()
    h.setLevel(logging.INFO)
    h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    lg = logging.getLogger("api")
    lg.addHandler(h)
    lg.setLevel(logging.INFO)
    yield h
    lg.removeHandler(h)


@pytest.fixture(autouse=True)
def attach_log(log_capture, request):
    yield
    text = log_capture.get_log()
    if text.strip():
        allure.attach(
            text,
            name=f"{request.node.name} log",
            attachment_type=allure.attachment_type.TEXT,
        )
