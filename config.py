from typing import Dict

class Config:
    """配置类"""

    BASE_URL: str = "http://zhjw.scu.edu.cn"
    CAPTCHA_URL: str = f"{BASE_URL}/img/captcha.jpg"
    TOKEN_URL: str = f"{BASE_URL}/login"
    LOGIN_URL: str = f"{BASE_URL}/j_spring_security_check"
    SCORE_URL: str = (
        f"{BASE_URL}/student/integratedQuery/scoreQuery/allTermScores/index"
    )
    PJ_URL: str = f"{BASE_URL}/student/teachingAssessment/evaluation/queryAll"

    DEFAULT_HEADERS: Dict[str, str] = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "zhjw.scu.edu.cn",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36",
    }