import os
import shutil
import json
from datetime import datetime
import difflib
import filecmp

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

def get_file_preview(file_path, max_lines=5):
    """获取文件内容预览"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:max_lines]
            return ''.join(lines) + ('...' if len(lines) >= max_lines else '')
    except Exception as e:
        return f"无法读取文件内容: {str(e)}"

def get_file_diff(file1, file2, folder_a, folder_b):
    """获取两个文件的差异，并显示具体的文件夹来源"""
    try:
        with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
            diff = difflib.unified_diff(
                f1.readlines(),
                f2.readlines(),
                fromfile=f"文件夹A ({folder_a}): {os.path.basename(file1)}",
                tofile=f"文件夹B ({folder_b}): {os.path.basename(file2)}",
                n=3  # 显示上下文行数
            )
            return ''.join(diff)
    except Exception as e:
        return f"无法比较文件: {str(e)}"

def get_changes_summary(folder_a, folder_b, last_state_a, last_state_b, files_in_a, files_in_b):
    """获取变更摘要"""
    changes = {
        'new_in_a': [],
        'new_in_b': [],
        'modified': [],
        'deleted_from_a': [],
        'deleted_from_b': []
    }
    
    # 检查删除的文件
    deleted_in_a = last_state_a - files_in_a
    deleted_in_b = last_state_b - files_in_b
    changes['deleted_from_a'] = list(deleted_in_a)
    changes['deleted_from_b'] = list(deleted_in_b)

    # 检查新文件和修改的文件
    for rel_path in files_in_a | files_in_b:
        file_in_a = os.path.join(folder_a, rel_path)
        file_in_b = os.path.join(folder_b, rel_path)
        
        is_new_in_a = rel_path in files_in_a and rel_path not in last_state_a
        is_new_in_b = rel_path in files_in_b and rel_path not in last_state_b

        if is_new_in_a and not is_new_in_b:
            changes['new_in_a'].append({
                'path': rel_path,
                'preview': get_file_preview(file_in_a),
                'source': f"文件夹A: {folder_a}"
            })
        elif is_new_in_b and not is_new_in_a:
            changes['new_in_b'].append({
                'path': rel_path,
                'preview': get_file_preview(file_in_b),
                'source': f"文件夹B: {folder_b}"
            })
        elif rel_path in files_in_a and rel_path in files_in_b:
            if not filecmp.cmp(file_in_a, file_in_b, shallow=False):
                time_a = os.path.getmtime(file_in_a)
                time_b = os.path.getmtime(file_in_b)
                changes['modified'].append({
                    'path': rel_path,
                    'diff': get_file_diff(file_in_a, file_in_b, folder_a, folder_b),
                    'newer_version': 'A' if time_a > time_b else 'B',
                    'time_a': datetime.fromtimestamp(time_a).strftime('%Y-%m-%d %H:%M:%S'),
                    'time_b': datetime.fromtimestamp(time_b).strftime('%Y-%m-%d %H:%M:%S')
                })
    
    return changes

def display_file_list(changes):
    """显示可以查看差异的文件列表"""
    print("\n可查看的文件：")
    index = 1
    file_map = {}
    
    # 显示修改过的文件
    if changes['modified']:
        print("\n已修改的文件：")
        for item in changes['modified']:
            print(f"{index}. {item['path']}")
            file_map[str(index)] = {
                'type': 'modified',
                'path': item['path'],
                'folder_a': True,
                'folder_b': True
            }
            index += 1
    
    # 显示新文件
    if changes['new_in_a']:
        print("\n文件夹A中的新文件：")
        for item in changes['new_in_a']:
            print(f"{index}. {item['path']}")
            file_map[str(index)] = {
                'type': 'new',
                'path': item['path'],
                'folder_a': True,
                'folder_b': False
            }
            index += 1
    
    if changes['new_in_b']:
        print("\n文件夹B中的新文件：")
        for item in changes['new_in_b']:
            print(f"{index}. {item['path']}")
            file_map[str(index)] = {
                'type': 'new',
                'path': item['path'],
                'folder_a': False,
                'folder_b': True
            }
            index += 1
    
    return file_map

def view_file_content(file_path, folder_a, folder_b):
    """查看文件内容"""
    try:
        if os.path.exists(os.path.join(folder_a, file_path)):
            print(f"\n文件夹A中的内容 ({folder_a}):")
            with open(os.path.join(folder_a, file_path), 'r', encoding='utf-8') as f:
                print(f.read())
        
        if os.path.exists(os.path.join(folder_b, file_path)):
            print(f"\n文件夹B中的内容 ({folder_b}):")
            with open(os.path.join(folder_b, file_path), 'r', encoding='utf-8') as f:
                print(f.read())
    except Exception as e:
        print(f"读取文件时出错: {str(e)}")

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

    # 获取变更摘要
    changes = get_changes_summary(folder_a, folder_b, last_state_a, last_state_b, files_in_a, files_in_b)
    
    # 显示变更摘要
    print("\n=== 同步变更摘要 ===")
    print(f"\n文件夹 A: {folder_a}")
    print(f"文件夹 B: {folder_b}")
    
    print(f"\n将从文件夹 A 同步到 B 的新文件:")
    for item in changes['new_in_a']:
        print(f"\n  + {item['path']}")
        print(f"    来源: {item['source']}")
        print("    预览内容:")
        print("    " + "\n    ".join(item['preview'].split('\n')))
    
    print(f"\n将从文件夹 B 同步到 A 的新文件:")
    for item in changes['new_in_b']:
        print(f"\n  + {item['path']}")
        print(f"    来源: {item['source']}")
        print("    预览内容:")
        print("    " + "\n    ".join(item['preview'].split('\n')))
    
    print(f"\n需要更新的文件:")
    for item in changes['modified']:
        print(f"\n  ~ {item['path']}")
        print(f"    文件夹A 最后修改时间: {item['time_a']}")
        print(f"    文件夹B 最后修改时间: {item['time_b']}")
        print(f"    较新版本在: 文件夹{item['newer_version']}")
        print("    文件差异:")
        print("    " + "\n    ".join(item['diff'].split('\n')))
    
    print(f"\n将从文件夹 A 中删除的文件:")
    for f in changes['deleted_from_a']:
        print(f"  - [文件夹A] {f}")
    
    print(f"\n将从文件夹 B 中删除的文件:")
    for f in changes['deleted_from_b']:
        print(f"  - [文件夹B] {f}")
    
    # 请求用户确认
    total_changes = (len(changes['new_in_a']) + len(changes['new_in_b']) + 
                    len(changes['modified']) + len(changes['deleted_from_a']) +
                    len(changes['deleted_from_b']))
    
    if total_changes == 0:
        print("\n没有需要同步的变更。")
        return
    
    while True:
        print("\n请选择操作：")
        print("1. 查看特定文件的完整内容")
        print("2. 继续同步")
        print("3. 取消同步")
        
        choice = input("请输入选项 (1/2/3): ").strip()
        
        if choice == '1':
            # 显示可选择的文件列表
            file_map = display_file_list(changes)
            
            if not file_map:
                print("没有可以查看的文件")
                continue
            
            # 选择文件
            file_num = input("\n请输入要查看的文件编号: ").strip()
            if file_num not in file_map:
                print("无效的文件编号")
                continue
            
            selected_file = file_map[file_num]
            
            # 选择查看方式
            print("\n请选择查看方式：")
            options = []
            if selected_file['folder_a']:
                options.append("A")
                print(f"A. 查看文件夹A ({folder_a}) 中的内容")
            if selected_file['folder_b']:
                options.append("B")
                print(f"B. 查看文件夹B ({folder_b}) 中的内容")
            if selected_file['folder_a'] and selected_file['folder_b']:
                options.append("C")
                print("C. 查看两个文件夹的差异对比")
            
            view_choice = input("\n请选择 (输入选项字母): ").strip().upper()
            
            if view_choice not in options:
                print("无效的选择")
                continue
            
            if view_choice == 'A' and selected_file['folder_a']:
                with open(os.path.join(folder_a, selected_file['path']), 'r', encoding='utf-8') as f:
                    print(f"\n文件夹A ({folder_a}) 中的内容:")
                    print(f.read())
            
            elif view_choice == 'B' and selected_file['folder_b']:
                with open(os.path.join(folder_b, selected_file['path']), 'r', encoding='utf-8') as f:
                    print(f"\n文件夹B ({folder_b}) 中的内容:")
                    print(f.read())
            
            elif view_choice == 'C' and selected_file['folder_a'] and selected_file['folder_b']:
                print("\n文件差异:")
                print(get_file_diff(
                    os.path.join(folder_a, selected_file['path']),
                    os.path.join(folder_b, selected_file['path']),
                    folder_a,
                    folder_b
                ))
            
            input("\n按回车键继续...")
            
        elif choice == '2':
            print("\n开始执行同步...")
            break
        elif choice == '3':
            print("同步操作已取消。")
            return
        else:
            print("无效的选择，请重试。")

    # 处理删除操作
    for rel_path in changes['deleted_from_a']:
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


if __name__ == '__main__':
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

    # 同步两个文件夹
    folder_a = '/Users/montylee/Library/Mobile Documents/iCloud~md~obsidian/Documents/Forsertee'
    folder_b = '/Users/montylee/Forsertee/Hexo/source/_posts'

    sync_two_ways(
        folder_a, 
        folder_b,
        ignore_patterns=custom_ignore
    )
