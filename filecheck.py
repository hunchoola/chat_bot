import os

def check_files():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("=== CURRENT DIRECTORY ===")
    print(current_dir)
    print("\n=== ALL FILES AND FOLDERS ===")
    
    for root, dirs, files in os.walk(current_dir):
        level = root.replace(current_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
    
    print("\n=== CHECKING CRITICAL PATHS ===")
    paths_to_check = [
        os.path.join(current_dir, 'static', 'css', 'style.css'),
        os.path.join(current_dir, 'static', 'js', 'script.js'),
        os.path.join(current_dir, 'templates', 'chat.html')
    ]
    
    for path in paths_to_check:
        exists = os.path.exists(path)
        print(f"{path}: {'✅ EXISTS' if exists else '❌ MISSING'}")

if __name__ == '__main__':
    check_files()