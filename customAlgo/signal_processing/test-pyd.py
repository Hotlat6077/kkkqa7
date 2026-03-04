# test_envlop_import.py
import sys
import os

print(f"当前目录: {os.getcwd()}")
print(f"Python 版本: {sys.version}")

try:
    print("尝试导入 envlop_xiao...")
    from envlop_xiao import env

    print("成功导入 envlop_xiao!")
    print(f"env 函数: {env}")
except ImportError as e:
    print(f"导入失败: {e}")

    # 检查是否有原始的 .py 文件
    if os.path.exists("envlop_xiao.py"):
        print("发现原始的 .py 文件，尝试从 .py 导入...")
        # 临时重命名 .pyd 文件
        if os.path.exists("envlop_xiao.pyd"):
            os.rename("envlop_xiao.pyd", "envlop_xiao.pyd.backup")
        try:
            from envlop_xiao import env

            print("从 .py 文件成功导入!")
        except Exception as py_error:
            print(f"从 .py 文件导入也失败: {py_error}")
        finally:
            # 恢复 .pyd 文件名
            if os.path.exists("envlop_xiao.pyd.backup"):
                os.rename("envlop_xiao.pyd.backup", "envlop_xiao.pyd")