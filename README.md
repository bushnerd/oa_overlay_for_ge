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

2. 当然还要安装大名鼎鼎的[Google Earth pro](https://www.google.com/earth/versions/#earth-pro)

## 使用说明

1. 进入主目录，运行`launch_oa_overlay_for_ge.bat`
2. 双击`oa_overlay_for_ge.kml`
3. 定位到你感兴趣的点，然后右键 `oa_overlay_for_ge` 刷新
4. 稍后就会看到你感兴趣的轨迹和标签了

## 关于 ge 的版本的问题

[See notes on Google Earth releases - Google Earth Help](https://support.google.com/earth/answer/40901?hl=en)

[Download a Google Earth Pro direct installer](https://support.google.com/earth/answer/168344?hl=en)
Google 的大部分桌面产品都采用静默安装，这里提供了离线版的安装文件，可以自定义选择安装目录,同时也提供了部分老版本的下载。

目前最新版本 v7.3.3 去掉了一些图层，并且出现搜索功能不走的代理的情况，经过采用 fiddler 抓包查看，判断问题应该是出在 ge 自己身上。

从老版本的链接中下载目前能用的版本为 googleearth-win-pro-7.1.8.3036，因此上传到库中作为备份。

## 维护者

[@scutxd](https://github.com/scutxd).

## 如何贡献

非常欢迎你的加入! [提一个 Issue](https://github.com/scutxd/oa_overlay_for_ge/issues/new) 或者提交一个 Pull R equest.

标准 Readme 遵循 [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) 行为规范.

### 贡献者

## 使用许可

[GPL](LICENSE) © scutxd
