import os
import shutil
import json
from datetime import datetime

def get_relative_paths(folder, ignore_patterns):
    """获取文件夹中所有文件的相对路径"""
    relative_paths = set()
    for root, dirs, files in os.walk(folder):
        # 过滤需要忽略的目录
        dirs[:] = [d for d in dirs if not should_ignore(d, ignore_patterns)]
        
        for file in files:
            if not should_ignore(file, ignore_patterns):
                # 获取相对路径
                rel_path = os.path.relpath(os.path.join(root, file), folder)
                relative_paths.add(rel_path)
    return relative_paths

def should_ignore(path, ignore_patterns):
    """检查文件或目录是否应该被忽略"""
    name = os.path.basename(path)
    # 检查是否匹配任何忽略模式
    for pattern in ignore_patterns:
        # 简单的通配符匹配
        if pattern.startswith('*') and name.endswith(pattern[1:]):
            return True
        elif pattern.endswith('*') and name.startswith(pattern[:-1]):
            return True
        elif pattern == name:
            return True
    return False

def load_last_state(state_file):
    """加载上次同步状态"""
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return set(json.load(f))
    return set()

def save_current_state(state_file, files):
    """保存当前同步状态"""
    with open(state_file, 'w') as f:
        json.dump(list(files), f)

def sync_two_ways(folder_a, folder_b, ignore_patterns=None):
    if ignore_patterns is None:
        # 默认忽略的文件和目录
        ignore_patterns = [
            '.DS_Store',        # macOS 系统文件
            'Thumbs.db',        # Windows 缩略图文件
            '.git',             # Git 目录
            '.gitignore',       # Git 忽略文件
            '__pycache__',      # Python 缓存目录
            '*.tmp',            # 临时文件
            '*.temp',           # 临时文件
            # '.obsidian',        # Obsidian 配置目录
            '.trash',            # 垃圾箱目录
            'workspace.json',    # 工作区配置文件
            '.sync_state'        # 添加状态文件到忽略列表
        ]

    # 状态文件路径
    state_file_a = os.path.join(folder_a, '.sync_state')
    state_file_b = os.path.join(folder_b, '.sync_state')

    print(f"\n开始同步 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"源文件夹 A: {folder_a}")
    print(f"源文件夹 B: {folder_b}")
    # print(f"忽略文件: {', '.join(ignore_patterns)}")
    
    files_synced = 0
    files_ignored = 0
    files_deleted = 0
    
    # 获取上次的状态和当前的文件列表
    last_state_a = load_last_state(state_file_a)
    last_state_b = load_last_state(state_file_b)
    files_in_a = get_relative_paths(folder_a, ignore_patterns)
    files_in_b = get_relative_paths(folder_b, ignore_patterns)

    # 确定删除的文件
    deleted_in_a = last_state_a - files_in_a
    deleted_in_b = last_state_b - files_in_b

    # 处理删除操作
    for rel_path in deleted_in_a | deleted_in_b:
        file_in_a = os.path.join(folder_a, rel_path)
        file_in_b = os.path.join(folder_b, rel_path)
        
        if os.path.exists(file_in_a):
            os.remove(file_in_a)
            print(f"删除文件 (A): {rel_path}")
            files_deleted += 1
        
        if os.path.exists(file_in_b):
            os.remove(file_in_b)
            print(f"删除文件 (B): {rel_path}")
            files_deleted += 1

    # 重新获取文件列表（因为可能已经删除了一些文件）
    files_in_a = get_relative_paths(folder_a, ignore_patterns)
    files_in_b = get_relative_paths(folder_b, ignore_patterns)

    # 处理新增和更新的文件
    for rel_path in files_in_a | files_in_b:
        file_in_a = os.path.join(folder_a, rel_path)
        file_in_b = os.path.join(folder_b, rel_path)
        
        # 如果是新文件（在任一目录中不存在于上次状态）
        is_new_in_a = rel_path in files_in_a and rel_path not in last_state_a
        is_new_in_b = rel_path in files_in_b and rel_path not in last_state_b

        if is_new_in_a and not is_new_in_b:
            # A中的新文件，复制到B
            os.makedirs(os.path.dirname(file_in_b), exist_ok=True)
            shutil.copy2(file_in_a, file_in_b)
            print(f"新增文件 (B): {rel_path}")
            files_synced += 1
        elif is_new_in_b and not is_new_in_a:
            # B中的新文件，复制到A
            os.makedirs(os.path.dirname(file_in_a), exist_ok=True)
            shutil.copy2(file_in_b, file_in_a)
            print(f"新增文件 (A): {rel_path}")
            files_synced += 1
        elif rel_path in files_in_a and rel_path in files_in_b:
            # 更新已存在的文件（使用最新的版本）
            time_a = os.path.getmtime(file_in_a)
            time_b = os.path.getmtime(file_in_b)
            
            if time_a > time_b:
                shutil.copy2(file_in_a, file_in_b)
                print(f"更新文件 (B): {rel_path}")
                files_synced += 1
            elif time_b > time_a:
                shutil.copy2(file_in_b, file_in_a)
                print(f"更新文件 (A): {rel_path}")
                files_synced += 1

    # 保存当前状态
    save_current_state(state_file_a, files_in_a)
    save_current_state(state_file_b, files_in_b)

    print(f"\n同步完成:")
    print(f"- 同步文件数: {files_synced}")
    print(f"- 删除文件数: {files_deleted}")
    print(f"- 忽略文件数: {files_ignored}")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# 使用示例
# 可以自定义忽略的文件和目录
custom_ignore = [
    '.DS_Store',
    '.obsidian',
    'Thumbs.db',
    '*.tmp',
    '*.temp',
    '.git',
    '.gitignore',
    '__pycache__',
    '.trash',
    '.sync_state'  # 添加状态文件到忽略列表
]

sync_two_ways(
    '/Users/montylee/Library/Mobile Documents/iCloud~md~obsidian/Documents/Forsertee', 
    '/Users/montylee/Forsertee/Hexo/source/_posts',
    ignore_patterns=custom_ignore
)
