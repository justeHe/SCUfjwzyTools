# SCUQuickEvaluation 

本版本仅供交流学习使用，请于下载24小时内删除， 请勿用于任何商业和违法用途。 

<!-- PROJECT SHIELDS --> 

[![Contributors][contributors-shield]][contributors-url] 
[![Forks][forks-shield]][forks-url] 
[![Stargazers][stars-shield]][stars-url] 
[![Issues][issues-shield]][issues-url] 

<!-- PROJECT LOGO --> 
<br /> 

<p align="center"> 
  <a href="https://raw.githubusercontent.com/Narrao/SCUQuickEvaluation/main/SCU.svg"> 
    <img src="https://raw.githubusercontent.com/Narrao/SCUQuickEvaluation/main/SCU.svg" alt="Logo" width="120" height="120"> 
  </a> 


  <h3 align="center">四川大学教务快速评教系统</h3> 
  <p align="center"> 
    一个专为四川大学教务处快速评教设计的工具。通过自动化操作，帮助学生快速完成教学评价。 
    <br /> 
    <a href="https://github.com/Narrao/SCUQuickEvaluation"><strong>探索本项目的文档 »</strong></a> 
    <br /> 
    <br /> 
    <a href="https://github.com/Narrao/SCUQuickEvaluation/releases/tag/release">下载exe</a> 
    · 
    <a href="https://github.com/Narrao/SCUQuickEvaluation/issues">报告Bug</a> 
    · 
    <a href="https://github.com/Narrao/SCUQuickEvaluation/issues">提出新特性</a> 
  </p> 

</p> 

## 目录 

- [功能](#功能) 
- [上手指南](#上手指南) 
  - [使用方式一](#使用方式一) 
  - [使用方式二](#使用方式二) 
- [文件目录说明](#文件目录说明) 
- [贡献者](#贡献者) 
  - [如何参与开源项目](#如何参与开源项目) 
- [版本控制](#版本控制) 

### 功能 

- 自动登录四川大学教务系统
- 获取待评教课程列表
- 一键完成课程评教
- **提示：本项目默认评分为满分，若有其他需求请自行修改代码或手动评教** 

### 上手指南 

#### 使用方式一 

1. 安装依赖：`pip install -r requirements.txt`
2. 运行程序：`python main.py`
3. 输入学号和密码
4. 选择需要评教的课程

#### 使用方式二 

###### **开发前的配置要求** 

1. python 3.8及以上 
1. git 

###### **安装步骤** 

1. 克隆仓库： 

```sh 
git clone https://github.com/Narrao/SCUQuickEvaluation.git 
``` 

2. 进入项目目录： 

```sh 
cd SCUQuickEvaluation 
``` 

3. 安装依赖： 

```sh 
pip install -r requirements.txt 
``` 

4. 运行程序： 

```sh 
python main.py 
``` 

5. 输入学号和密码
6. 选择要评教的科目


### 文件目录说明 

``` 
.gitignore
README.md
config.py
evaluation.py
exceptions.py
main.py
models.py
requirements.txt
utils.py
``` 

### 贡献者 

`https://github.com/Narrao` 

#### 如何参与开源项目 

贡献使开源社区成为一个学习、激励和创造的绝佳场所。你所作的任何贡献都是**非常感谢**的。 


1. Fork the Project
2. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
3. Open a Pull Request

### 版本控制 

该项目使用Git进行版本管理。您可以在repository参看当前可用版本。 

<!-- links --> 

[your-project-path]:Narrao/SCUQuickEvaluation 
[contributors-shield]: https://img.shields.io/github/contributors/Narrao/SCUQuickEvaluation.svg?style=flat-square 
[contributors-url]: https://github.com/Narrao/SCUQuickEvaluation/graphs/contributors 
[forks-shield]: https://img.shields.io/github/forks/Narrao/SCUQuickEvaluation.svg?style=flat-square 
[forks-url]: https://github.com/Narrao/SCUQuickEvaluation/network/members 
[stars-shield]: https://img.shields.io/github/stars/Narrao/SCUQuickEvaluation.svg?style=flat-square 
[stars-url]: https://github.com/Narrao/SCUQuickEvaluation/stargazers 
[issues-shield]: https://img.shields.io/github/issues/Narrao/SCUQuickEvaluation.svg?style=flat-square 
[issues-url]: https://img.shields.io/github/issues/Narrao/SCUQuickEvaluation.svg 
[license-shield]: https://img.shields.io/github/license/Narrao/SCUQuickEvaluation.svg?style=flat-square 
[license-url]: https://github.com/Narrao/SCUQuickEvaluation/blob/master/LICENSE.txt 
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555 
[linkedin-url]: https://linkedin.com/in/shaojintian 

## 注意事项
- 请确保网络连接正常
- 验证码识别可能不准确，可能需要手动输入
