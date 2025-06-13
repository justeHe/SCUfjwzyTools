from dataclasses import dataclass

@dataclass
class Course:
    """课程信息类"""

    name: str
    ktid: str
    wjbm: str
    type_name: str
    is_evaluated: bool = False