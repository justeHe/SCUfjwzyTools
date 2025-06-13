from typing import Dict, List, Union
from pathlib import Path
import os
from bs4 import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
import random

from config import Config
from models import Course
from exceptions import LoginError, EvaluationError
from utils import logger, ocr, encode_password


class SCUEvaluation:
    """四川大学教务系统评教类"""
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = encode_password(password)
        self.session = requests.Session()
        self.session.headers.update(Config.DEFAULT_HEADERS)
        self.courses: List[Course] = []
        self.flag = None

    def _get_token(self) -> str:
        """获取token"""
        try:
            response = self.session.get(Config.TOKEN_URL)
            response.raise_for_status()
            token = BeautifulSoup(response.text, "html.parser").find(
                "input", {"id": "tokenValue"}
            )["value"]
            return token
        except Exception as e:
            logger.error(f"获取token失败: {e}")
            raise LoginError("获取token失败") from e

    def _get_captcha(self) -> Path:
        """获取验证码"""
        try:
            response = self.session.get(Config.CAPTCHA_URL)
            response.raise_for_status()
            captcha_path = Path("captcha.jpg")
            captcha_path.write_bytes(response.content)
            return captcha_path
        except Exception as e:
            logger.error(f"获取验证码失败: {e}")
            raise LoginError("获取验证码失败") from e

    def login(self, max_attempts: int = 3) -> bool:
        """登录系统"""
        for attempt in range(max_attempts):
            try:
                captcha_path = self._get_captcha()
                # 显示验证码
                if os.path.exists(captcha_path):
                    with open(captcha_path, 'rb') as f:
                        img_bytes = f.read()

                    captcha_text = ocr.classification(img_bytes)
                logger.info(f"OCR识别验证码为: {captcha_text}")

                # 清理验证码文件
                captcha_path.unlink(missing_ok=True)

                login_data = {
                    "tokenValue": self._get_token(),
                    "j_username": self.username,
                    "j_password": self.password,
                    "j_captcha": captcha_text,
                }

                response = self.session.post(Config.LOGIN_URL, data=login_data)
                if "欢迎您" in response.text:
                    logger.info("登录成功")
                    return True

                logger.warning(f"登录失败，剩余尝试次数: {max_attempts - attempt - 1}")

            except Exception as e:
                logger.error(f"登录过程出错: {e}")
                if attempt == max_attempts - 1:
                    raise LoginError("登录失败次数过多") from e

        return False

    def get_courses(self, flag: str = "ktjs") -> List[Course]:
        """获取待评教课程列表
        :param flag: 评教类型，ktjs为课程及时评教，kt为期末评教
        """
        try:
            data = {"pageNum": "1", "pageSize": "30", "flag": flag}
            if flag == "ktjs":
                self.flag = "ktjs"
            else:
                self.flag = "kt"
            response = self.session.post(Config.PJ_URL, data=data)
            response.raise_for_status()

            courses_data = response.json()["data"]["records"]
            self.courses = [
                Course(
                    name=course["KCM"],
                    ktid=course["KTID"],
                    wjbm=course["WJBM"],
                    type_name=course["WJMC"],
                    is_evaluated=(course["SFPG"] == "1"),
                )
                for course in courses_data
                if course["SFPG"] == "0"  # 只获取未评教的课程
            ]
            return self.courses

        except Exception as e:
            logger.error(f"获取课程列表失败: {e}")
            raise EvaluationError("获取课程列表失败") from e

    def evaluate_course(self, course: Course) -> bool:
        """评教单个课程"""
        try:
            # 获取评教表单
            url = (
                f"{Config.BASE_URL}/student/teachingEvaluation/"
                f"newEvaluation/evaluation/{course.ktid}"
            )
            response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            form_data = self._parse_evaluation_form(soup)

            # 提交评教
            submit_url = (
                f"{Config.BASE_URL}/student/teachingAssessment/"
                f"baseInformation/questionsAdd/doSave"
            )

            # 第一次提交
            form_data["tjcs"] = "0"
            response = self._submit_evaluation(submit_url, form_data)
            if response.json()["result"] == "no":
                logger.error(f"课程 {course.name} 评教失败: {response.json()["msg2"]}")
                return False
            # 第二次提交
            form_data["tjcs"] = "1"
            form_data["tokenValue"] = response.json()["token"]
            response = self._submit_evaluation(submit_url, form_data)

            if response.json()["result"] == "ok":
                logger.info(f"课程 {course.name} 评教完成")
                return True

            logger.error(f"课程 {course.name} 评教失败: {response.text}")
            return False

        except Exception as e:
            logger.error(f"评教过程出错: {e}")
            raise EvaluationError(f"评教课程 {course.name} 失败") from e

    def _parse_evaluation_form(
        self, soup: BeautifulSoup
    ) -> Dict[str, Union[str, List[str]]]:
        """解析评教表单"""
        form_data = {
            "wjbm": soup.find("input", {"name": "wjbm"})["value"],
            "ktid": soup.find("input", {"name": "ktid"})["value"],
            "tokenValue": soup.find("input", {"name": "tokenValue"})["value"],
            "compare": "",
        }

        # 处理所有input元素
        for input_elem in soup.find_all("input"):
            name = input_elem.get("name")
            if not name:
                continue

            if input_elem.get("placeholder") == "请输入1-100的整数":
                form_data[name] = "100"
            elif input_elem["type"] == "radio" and name not in form_data:
                form_data[name] = input_elem["value"]
            elif input_elem["type"] == "radio" and self.flag == "ktjs":
                form_data[name] = max(form_data[name], input_elem["value"])
            elif input_elem["type"] == "checkbox":
                if name not in form_data:
                    form_data[name] = []
                if input_elem["value"] != "K_以上均无":
                    form_data[name].append(input_elem["value"])

        # 处理文本域
        textarea = soup.find("textarea", {"maxlength": "500"})
        if textarea:
            comments = [
                "这门课程的教学效果很好,老师热爱教学,教学方式生动有趣,课程内容丰富且贴合时代特点。",
                "老师教学认真负责,课程内容系统全面,理论与实践结合得很好,让我受益匪浅。",
                "课程设计合理,老师讲解清晰,课堂互动性强,能够激发学生的学习兴趣。",
                "教学方式新颖,案例丰富,能够将抽象的理论知识转化为生动的实践内容。",
                "老师专业素养高,教学态度认真,能够因材施教,关注每个学生的学习情况。"
            ]
            form_data[textarea["name"]] = random.choice(comments)

        return form_data

    def _submit_evaluation(
        self, url: str, form_data: Dict[str, Union[str, List[str]]]
    ) -> requests.Response:
        """提交评教表单"""
        # 处理复选框数据
        params = {
            **{
                f"{k}": v_item
                for k, v in form_data.items()
                if isinstance(v, list)
                for v_item in v
            },
            **{k: v for k, v in form_data.items() if not isinstance(v, list)},
        }

        data = MultipartEncoder(
            params, boundary="------WebKitFormBoundaryPt8uDhx6i4giheJk"
        )

        headers = {
            **Config.DEFAULT_HEADERS,
            "Content-Type": data.content_type,
            "X-Requested-With": "XMLHttpRequest",
        }

        response = self.session.post(
            f"{url}?tokenValue={form_data['tokenValue']}", headers=headers, data=data
        )
        response.raise_for_status()
        return response

