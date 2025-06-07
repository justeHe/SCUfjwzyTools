from evaluation import SCUEvaluation
import logging

logger = logging.getLogger(__name__)

def main():
    while True:
        try:
            username = input("请输入学号(输入q退出): ")
            if username.lower() == 'q':
                break
                
            password = input("请输入密码: ")
            evaluator = SCUEvaluation(username, password)

            if not evaluator.login():
                logger.error("登录失败，请检查学号密码")
                continue

            while True:
                courses = evaluator.get_courses()
                if not courses:
                    logger.info("没有待评教课程")
                    break

                logger.info(f"共有 {len(courses)} 门待评教课程:")
                for i, course in enumerate(courses):
                    print(f"{i}. {course.name}")
                print(f"{len(courses)}. 一键评教所有课程")
                print(f"{len(courses)+1}. 返回")

                choice = input("\n请输入需要评教的课程编号(空格分隔): ")
                if not choice.strip():
                    logger.error("未输入编号")
                    continue

                choices = list(map(int, choice.split()))
                if choices[0] == len(courses)+1:
                    break
                elif choices[0] == len(courses):
                    for course in courses:
                        evaluator.evaluate_course(course)
                else:
                    for idx in choices:
                        if 0 <= idx < len(courses):
                            evaluator.evaluate_course(courses[idx])
                        else:
                            logger.warning(f"无效的课程编号: {idx}")

        except Exception as e:
            logger.error(f"程序执行出错: {e}")
        finally:
            if 'evaluator' in locals():
                evaluator.session.close()

if __name__ == "__main__":
    main()