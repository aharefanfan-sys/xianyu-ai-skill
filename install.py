#!/usr/bin/env python3
"""
跨平台 Skill 安装脚本
自动将 Skill 安装到目标平台的指定目录
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
import json

SCRIPT_DIR = Path(__file__).parent
DIST_DIR = SCRIPT_DIR / "dist"


def get_platform_path(platform):
    """获取目标平台的 Skill 目录路径"""
    
    home = Path.home()
    
    platforms = {
        "opencode": {
            "global": home / ".config" / "opencode" / "skills" / "xianyu-ai",
            "project": ".opencode" / "skills" / "xianyu-ai"
        },
        "claude": {
            "global": home / ".claude" / "skills" / "xianyu-ai",
            "project": ".claude" / "skills" / "xianyu-ai"
        },
        "openclaw": {
            "global": home / ".openclaw" / "skills" / "xianyu-ai",
            "project": "skills" / "xianyu-ai"
        }
    }
    
    return platforms.get(platform, {})


def install_to_platform(platform, global_install=False):
    """安装 Skill 到指定平台"""
    
    paths = get_platform_path(platform)
    
    if not paths:
        print(f"未知平台: {platform}")
        return False
    
    target = paths["global"] if global_install else paths["project"]
    
    print(f"\n安装到 {platform}: {target}")
    print(f"全局安装: {global_install}")
    
    # 创建目标目录
    target.mkdir(parents=True, exist_ok=True)
    
    # 复制文件
    files_to_copy = [
        "SKILL.md",
        "prompts",
        "scripts",
        "data"
    ]
    
    for item in files_to_copy:
        src = SCRIPT_DIR / item
        dst = target / item
        
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"  ✓ 复制目录: {item}")
        elif src.is_file():
            shutil.copy2(src, dst)
            print(f"  ✓ 复制文件: {item}")
    
    print(f"\n✅ 安装成功！")
    return True


def create_package():
    """创建可分发包"""
    
    output_file = DIST_DIR / "xianyu-ai-skill.zip"
    
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(SCRIPT_DIR):
            # 跳过 dist 目录自身
            if 'dist' in Path(root).parts:
                continue
            
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(SCRIPT_DIR)
                zipf.write(file_path, arcname)
    
    print(f"\n📦 打包完成: {output_file}")
    return str(output_file)


def main():
    """主函数"""
    
    print("=" * 50)
    print("闲鱼 AI 助手 - 跨平台安装脚本")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("\n用法:")
        print("  python install.py opencode       # 安装到当前项目 (OpenCode)")
        print("  python install.py claude         # 安装到当前项目 (Claude)")
        print("  python install.py openclaw       # 安装到当前项目 (OpenClaw)")
        print("  python install.py --global opencode  # 全局安装")
        print("  python install.py --package      # 创建分发包")
        print("\n示例:")
        print("  python install.py opencode")
        print("  python install.py --global claude")
        sys.exit(1)
    
    # 解析参数
    global_install = False
    platform = None
    
    for arg in sys.argv[1:]:
        if arg == "--global":
            global_install = True
        elif arg == "--package":
            create_package()
            return
        elif arg in ["opencode", "claude", "openclaw"]:
            platform = arg
    
    if platform:
        install_to_platform(platform, global_install)
    else:
        print("请指定目标平台: opencode, claude, openclaw")


if __name__ == "__main__":
    main()
