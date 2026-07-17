#!/usr/bin/env python3
"""
自动生成 Docsify 侧边栏脚本
扫描 _posts 目录下的所有 .md 文件，按日期倒序生成导航菜单
"""

import os
import re
from datetime import datetime
from pathlib import Path

def extract_title_from_filename(filename):
    """从文件名中提取标题"""
    # 文件名格式: YYYY-MM-DD-标题.md
    match = re.match(r'\d{4}-\d{2}-\d{2}-(.+)\.md$', filename)
    if match:
        return match.group(1)
    return filename.replace('.md', '')

def extract_date_from_filename(filename):
    """从文件名中提取日期"""
    match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return datetime.strptime(match.group(1), '%Y-%m-%d')
    return datetime.min

def generate_sidebar():
    """生成侧边栏"""
    posts_dir = '_posts'
    
    # 检查目录是否存在
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
    
    # 获取所有 .md 文件
    md_files = [f for f in os.listdir(posts_dir) if f.endswith('.md')]
    
    # 按日期倒序排序（最新的在前面）
    md_files.sort(key=extract_date_from_filename, reverse=True)
    
    # 生成侧边栏内容
    sidebar_content = "* [首页](#/)\n"
    sidebar_content += "* [下载安装](download.md)\n"
    sidebar_content += "* [使用指南](guide.md)\n"
    
    # 添加所有文章
    if md_files:
        sidebar_content += "\n<!-- 文章列表 -->\n"
        for md_file in md_files:
            title = extract_title_from_filename(md_file)
            sidebar_content += f"* [{title}](_posts/{md_file})\n"
    
    sidebar_content += "\n* [关于](about.md)\n"
    
    return sidebar_content

if __name__ == '__main__':
    sidebar = generate_sidebar()
    
    with open('_sidebar.md', 'w', encoding='utf-8') as f:
        f.write(sidebar)
    
    print("✅ _sidebar.md 已生成！")
    print("\n生成的内容：\n")
    print(sidebar)
