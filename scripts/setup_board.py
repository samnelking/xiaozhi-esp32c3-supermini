#!/usr/bin/env python3
"""Setup ESP32-C3 SuperMini board in xiaozhi-esp32 project"""
# 这是一个用于在xiaozhi-esp32项目中设置ESP32-C3 SuperMini开发板的Python脚本
# 它会自动更新CMakeLists.txt和Kconfig.projbuild文件，将新开发板配置添加到项目中

import sys
import os

def update_cmakelists(filepath):
    """更新CMakeLists.txt文件，添加ESP32-C3 SuperMini开发板配置"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经添加了ESP32-C3 SuperMini配置
    if 'CONFIG_BOARD_TYPE_ESP32C3_SUPERMINI' in content:
        print('CMakeLists.txt already contains ESP32C3_SUPERMINI, skipping')
        return  # 如果已存在，跳过更新
    
    # 定义要添加的新开发板配置内容
    new_board = '''elseif(CONFIG_BOARD_TYPE_ESP32C3_SUPERMINI)
    set(BOARD_TYPE "esp32c3-supermini")
    set(BUILTIN_TEXT_FONT font_puhui_basic_14_1)
    set(BUILTIN_ICON_FONT font_awesome_14_1)
'''
    # 注意：这是一个CMake条件语句块，当选择ESP32C3_SUPERMINI开发板类型时，
    # 设置BOARD_TYPE变量为"esp32c3-supermini"，并指定文本字体和图标字体
    
    # 查找最后一个开发板配置项（例如CONFIG_BOARD_TYPE_HU_087）并在其后插入新配置
    marker = 'elseif(CONFIG_BOARD_TYPE_HU_087)'
    if marker in content:
        # 找到标记位置
        idx = content.find(marker)
        # 获取标记后的内容
        rest = content[idx:]
        # 将剩余内容按行分割
        lines = rest.split('\n')
        insert_line = 0
        # 遍历行，找到结束标记endif()
        for i, line in enumerate(lines):
            if line.strip() == 'endif()' and i > 0:
                # 计算绝对插入位置
                # 将前i行的总长度（包括换行符）相加，得到在原始内容中的位置
                insert_pos = idx + sum(len(l)+1 for l in lines[:i])
                # 在endif()之前插入新的开发板配置
                content = content[:insert_pos] + new_board + content[insert_pos:]
                break
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('CMakeLists.txt updated')

def update_kconfig(filepath):
    """更新Kconfig.projbuild文件，添加ESP32-C3 SuperMini开发板选项"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经添加了ESP32-C3 SuperMini选项
    if 'BOARD_TYPE_ESP32C3_SUPERMINI' in content:
        print('Kconfig.projbuild already contains ESP32C3_SUPERMINI, skipping')
        return  # 如果已存在，跳过更新
    
    # 定义要添加的新Kconfig选项
    new_option = '''    config BOARD_TYPE_ESP32C3_SUPERMINI
        bool "ESP32-C3 SuperMini (MAX98357A + INMP441 + ST7789)"
        depends on IDF_TARGET_ESP32C3
'''
    # 这是一个Kconfig配置选项，用于在menuconfig中显示开发板选择
    # bool表示这是一个布尔选项（是/否）
    # 描述字符串会显示在menuconfig界面中
    # depends on指定此选项仅在目标为ESP32C3时可用
    
    # 查找现有的开发板配置标记
    marker = 'config BOARD_TYPE_HU_087'
    if marker in content:
        idx = content.find(marker)
        rest = content[idx:]
        lines = rest.split('\n')
        insert_pos = idx
        # 遍历后续行，找到合适的位置插入新选项
        # 通常Kconfig中的选项是连续定义的，我们找到下一个config或endchoice的位置
        for i, line in enumerate(lines[1:], 1):
            if line.strip().startswith('config ') or line.strip() == 'endchoice':
                # 计算插入位置
                insert_pos = idx + sum(len(l)+1 for l in lines[:i])
                break
        # 在找到的位置插入新选项
        content = content[:insert_pos] + new_option + content[insert_pos:]
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Kconfig.projbuild updated')

if __name__ == '__main__':
    # 主程序入口
    # 允许通过命令行参数指定基础路径，默认为'xiaozhi-esp32/main'
    base_path = sys.argv[1] if len(sys.argv) > 1 else 'xiaozhi-esp32/main'
    
    # 更新CMakeLists.txt文件
    update_cmakelists(os.path.join(base_path, 'CMakeLists.txt'))
    # 更新Kconfig.projbuild文件
    update_kconfig(os.path.join(base_path, 'Kconfig.projbuild'))
