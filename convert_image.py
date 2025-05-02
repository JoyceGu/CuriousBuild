#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import os
import sys
from PIL import Image
import io

def image_to_base64(image_path):
    """
    将图片文件转换为base64编码
    
    参数:
        image_path: 图片文件路径
        
    返回:
        base64编码的字符串
    """
    try:
        # 打开图片
        img = Image.open(image_path)
        
        # 创建内存文件
        buffer = io.BytesIO()
        
        # 保存图片到内存文件
        img.save(buffer, format=img.format)
        
        # 获取base64编码
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # 构建data URI
        mime_type = f"image/{img.format.lower()}" if img.format else "image/jpeg"
        data_uri = f"data:{mime_type};base64,{img_base64}"
        
        return data_uri
    except Exception as e:
        print(f"转换失败: {e}")
        return None

def save_to_file(base64_string, output_file):
    """
    将base64字符串保存到文件
    
    参数:
        base64_string: base64编码的字符串
        output_file: 输出文件路径
    """
    try:
        with open(output_file, 'w') as f:
            f.write(base64_string)
        print(f"Base64编码已保存至: {output_file}")
    except Exception as e:
        print(f"保存失败: {e}")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python convert_image.py <图片文件路径> [输出文件路径]")
        return
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"错误: 文件 '{image_path}' 不存在")
        return
    
    base64_string = image_to_base64(image_path)
    
    if base64_string:
        print("转换成功!")
        
        # 如果指定了输出文件，则保存到文件
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
            save_to_file(base64_string, output_file)
        else:
            print("\nBase64编码:")
            print(base64_string[:100] + "..." if len(base64_string) > 100 else base64_string)
            print("\n要在HTML中使用此图片，请使用以下代码:")
            print(f'<img src="{base64_string[:50]}..." alt="Base64 encoded image" />')
            print("\n要在CSS中使用此图片，请使用以下代码:")
            print(f'background-image: url("{base64_string[:50]}...");')

if __name__ == "__main__":
    main() 