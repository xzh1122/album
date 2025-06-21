# 数字生活档案——相册 项目

## 项目简介
数字生活档案是一个基于 FastAPI + 原生前端的个人生活记录与智能相册系统。支持多种内容上传，自动按时间和标签整理，便于回顾和管理生活点滴。

## 主要功能
- 动态记录：支持文字、照片、视频、语音等多种形式内容上传。
- 智能分类：自动识别内容标签，图片支持智能分类。
- 相册浏览：照片按日期分组展示，每张照片带有分类标签。

## 技术栈
- 后端：FastAPI
- 前端：原生 HTML + JavaScript
- 智能分类：HuggingFace ViT 模型（可选）
- 存储：本地文件系统

## 目录结构
- main.py：后端主程序
- static/index.html：上传页面
- static/album.html：相册浏览页面
- uploads/：所有上传的文件
- docs/：需求、开发、测试、功能介绍等文档

## 快速开始
1. 安装依赖：`pip install -r requirements.txt`
2. 启动服务：`python main.py`
3. 用浏览器打开 `static/index.html` 上传照片，`static/album.html` 浏览相册

## 文档
- docs/需求分析文档.md
- docs/开发和部署文档.md
- docs/测试文档.md
- docs/功能介绍文档.md

## 说明
- 上传目录需有写权限。
- 若需图片智能分类，需提前下载好模型权重。
- 支持本地和 Docker 部署。
