#!/usr/bin/env python3
"""Setup ESP32-C3 SuperMini board in xiaozhi-esp32 project"""

import sys
import os

def update_cmakelists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_board = '''elseif(CONFIG_BOARD_TYPE_ESP32C3_SUPERMINI)
    set(BOARD_TYPE "esp32c3-supermini")
    set(BUILTIN_TEXT_FONT font_puhui_basic_14_1)
    set(BUILTIN_ICON_FONT font_awesome_14_1)
'''
    
    lines = content.split('\n')
    for i in range(len(lines)-1, -1, -1):
        if lines[i].strip() == 'endif()':
            lines.insert(i, new_board.rstrip())
            break
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('CMakeLists.txt updated')

def update_kconfig(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_option = '''    config BOARD_TYPE_ESP32C3_SUPERMINI
        bool "ESP32-C3 SuperMini (MAX98357A + INMP441 + ST7789)"
        depends on IDF_TARGET_ESP32C3
'''
    
    marker = 'config BOARD_TYPE_HU_087'
    if marker in content:
        idx = content.find(marker)
        rest = content[idx:]
        lines = rest.split('\n')
        insert_pos = idx
        for i, line in enumerate(lines[1:], 1):
            if line.strip().startswith('config ') or line.strip() == 'endchoice':
                insert_pos = idx + sum(len(l)+1 for l in lines[:i])
                break
        content = content[:insert_pos] + new_option + content[insert_pos:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Kconfig.projbuild updated')

if __name__ == '__main__':
    base_path = sys.argv[1] if len(sys.argv) > 1 else 'xiaozhi-esp32/main'
    update_cmakelists(os.path.join(base_path, 'CMakeLists.txt'))
    update_kconfig(os.path.join(base_path, 'Kconfig.projbuild'))
