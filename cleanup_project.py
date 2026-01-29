import os
import shutil

def cleanup_project():
    """Очищает проект от временных и ненужных файлов."""
    
    files_to_delete = [
        # Временные файлы для конвертации иконки (оставляем только convert_to_ico_proper.py)
        'convert_to_ico.py',
        'convert_to_ico_advanced.py',
        'convert_to_ico_correct.py',
        'convert_to_ico_final.py',
        'convert_to_ico_improved.py',
        'convert_to_ico_pillow.py',
        'convert_to_ico_working.py',
        
        # Тестовые файлы
        'debug_test.py',
        'generate_icon.py',
        'test_icon.png',
        'test_icon.py',
        
        # Старый архив
        'ASB SimpleProxy_Portable.zip',
        
        # Документация (если не нужна)
        'implementation_plan.md',
    ]
    
    directories_to_delete = [
        # Временные папки
        '.trae/documents',
    ]
    
    print("Очистка проекта от временных и ненужных файлов...\n")
    
    # Удаление файлов
    deleted_files = []
    for file in files_to_delete:
        if os.path.exists(file):
            try:
                os.remove(file)
                deleted_files.append(file)
                print(f"✓ Удален файл: {file}")
            except Exception as e:
                print(f"✗ Ошибка при удалении {file}: {e}")
        else:
            print(f"  Файл не найден: {file}")
    
    # Удаление папок
    deleted_dirs = []
    for dir_path in directories_to_delete:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                deleted_dirs.append(dir_path)
                print(f"✓ Удалена папка: {dir_path}")
            except Exception as e:
                print(f"✗ Ошибка при удалении {dir_path}: {e}")
        else:
            print(f"  Папка не найдена: {dir_path}")
    
    print(f"\nОчистка завершена!")
    print(f"Удалено файлов: {len(deleted_files)}")
    print(f"Удалено папок: {len(deleted_dirs)}")
    
    # Проверяем, остались ли временные файлы иконок
    temp_icon_files = [f for f in os.listdir('.') if f.startswith('temp_') or f.startswith('icon_')]
    if temp_icon_files:
        print(f"\n⚠ Найдены временные файлы иконок: {temp_icon_files}")
        print("  Рекомендуется удалить их вручную")
    
    return len(deleted_files) + len(deleted_dirs) > 0

if __name__ == "__main__":
    cleanup_project()
