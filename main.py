from evaluation import SCUEvaluation
import logging
import sys

logger = logging.getLogger(__name__)


def main():
    while True:
        try:
            username = input("请输入学号(输入q退出): ")
            if username.lower() == 'q':
                sys.exit(0)

            password = input("请输入密码: ")
            evaluator = SCUEvaluation(username, password)

            if not evaluator.login():
                logger.error("登录失败，请检查学号密码")
                sys.exit(1)

            while True:
                print("1. 课程及时评教")
                print("2. 期末评教")
                print("3. 退出")
                eval_type = input("请选择评教类型(1/2/3): ")
                if eval_type == "3":
                    sys.exit(0)
                flag = "ktjs" if eval_type == "1" else "kt"
                courses = evaluator.get_courses(flag)
                if not courses:
                    logger.info("没有待评教课程")
                    continue_choice = input("\n是否返回主菜单? (y/n): ")
                    if continue_choice.lower() == 'y':
                        continue
                    else:
                        break
                    
                logger.info(f"共有 {len(courses)} 门待评教课程:")
                for i, course in enumerate(courses):
                    print(f"{i}. {course.type_name} {course.name}")
                print(f"{len(courses)}. 一键评教所有课程")
                print(f"{len(courses)+1}. 返回")

                choice = input("\n请输入需要评教的课程编号(空格分隔): ")
                if not choice.strip():
                    logger.error("未输入编号")
                    continue

                choices = list(map(int, choice.split()))
                if choices[0] == len(courses)+1:
                    continue
                elif choices[0] == len(courses):
                    for course in courses:
                        evaluator.evaluate_course(course)
                else:
                    for idx in choices:
                        if 0 <= idx < len(courses):
                            evaluator.evaluate_course(courses[idx])
                        else:
                            logger.warning(f"无效的课程编号: {idx}")
            continue_choice = input("\n是否继续评教其他账号? (y/n): ")
            if continue_choice.lower() != 'y':
                break

        except Exception as e:
            logger.error(f"程序执行出错: {e}")
        finally:
            if 'evaluator' in locals():
                evaluator.session.close()


if __name__ == "__main__":
    main()
