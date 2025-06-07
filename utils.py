import hashlib
import logging
import os
from pathlib import Path
from typing import Dict, List, Union
from PIL import Image
import pytesseract
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
    md5_1 = hashlib.md5((password + "{Urp602019}").encode()).hexdigest()
    md5_2 = hashlib.md5(password.encode()).hexdigest()
    return f"{md5_1}*{md5_2}"

def recognize_captcha(path: Path) -> str:
    """自动识别验证码"""
    try:
        image = Image.open(path).convert("L")  # 灰度图
        image = image.point(lambda x: 0 if x < 140 else 255, '1')
        text = pytesseract.image_to_string(image, config='--psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return text.strip()
    except Exception as e:
        logger.error(f"OCR识别失败: {e}")
        return ""