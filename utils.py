import hashlib
import logging
import ddddocr
from contextlib import contextmanager
from io import StringIO
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@contextmanager
def suppress_stdout():
    original_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        yield
    finally:
        sys.stdout = original_stdout

with suppress_stdout():
    ocr = ddddocr.DdddOcr()

def encode_password(password: str) -> str:
    """密码加密"""
    md5_1 = hashlib.md5(hashlib.md5((password + "{Urp602019}").encode()).hexdigest().encode()).hexdigest()
    md5_2 = hashlib.md5(hashlib.md5(password.encode()).hexdigest().encode()).hexdigest()
    return f"{md5_1}*{md5_2}"