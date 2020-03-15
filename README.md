# oa_overlay_for_ge

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

## 名词介绍

oa = outdoor assistant from 2bulu

ge = google earth pro

## 背景

想法起源于此项目[Google Earth Map Overlays](http://ge-map-overlays.appspot.com/)
原来 ge 可以叠加这么多资源，对于在国内来说，oa 的资源应该最丰富吧，因此本项目就是 oa 上轨迹的信息加载 到 ge 上。

## 安装

1. 这个项目使用 [python3.8](https://www.python.org/) . 请确保你本地安装了它们。

2. 进入主要目录，使用如下命令安装如下依赖库：

```batch
pip install -r requirements.txt
```

```batch
astroid==2.3.3
certifi==2019.11.28
chardet==3.0.4
colorama==0.4.3
idna==2.9
isort==4.3.21
lazy-object-proxy==1.4.3
lxml==4.5.0
mccabe==0.6.1
pylint==2.4.4
requests==2.23.0
six==1.14.0
urllib3==1.25.8
wrapt==1.11.2
yapf==0.29.0
```

3. 当然还要安装大名鼎鼎的[Google Earth pro](https://www.google.com/earth/versions/#earth-pro)

## 使用说明

1. 进入主目录，运行`launch_oa_overlay_for_ge.bat`
2. 双击`oa_overlay_for_ge.kml`
3. 定位到你感兴趣的点，然后右键 oa_overlay_for_ge 刷新
4. 稍后就会看到你感兴趣的轨迹和标签了

## 维护者

[@scutxd](https://github.com/scutxd).

## 如何贡献

非常欢迎你的加入! [提一个 Issue](https://github.com/scutxd/oa_overlay_for_ge/issues/new) 或者提交一个 Pull R equest.

标准 Readme 遵循 [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) 行为规范.

### 贡献者

## 使用许可

[GPL](LICENSE) © scutxd
