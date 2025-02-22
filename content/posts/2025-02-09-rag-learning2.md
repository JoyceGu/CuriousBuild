---
layout: post
title: "RAG 学习笔记 （2）"
date: 2025-02-08
tags: [Learning, Artifical Intelligence, RAG]
---

**RAG系统的核心组件**

1. 向量化模块：用于将文档剪短转换为向量表示，以便后续检索
2. 文档加载与切分模块：负责加载文档并chunk （方式：滑动窗口，根据符号，等等）
3. 数据库模块：用于储存文档片段及其对应的向量表示
4. 检索模块：根据用户输入的查询，检索与其相关的文档片段
5. 生成模块：调用语言模型生成基于检索信息的回答

默认情况下， text-embedding-3-small生成的向量长度为1536， text-embedding-3-large的向量长度为3072。