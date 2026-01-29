from PIL import Image
import struct
import os

def create_proper_ico(png_path, ico_path):
    """Создает качественный ICO файл с оптимальными размерами для всех режимов просмотра Windows."""
    img = Image.open(png_path)
    
    # Убедимся, что изображение квадратное
    if img.width != img.height:
        size = max(img.width, img.height)
        new_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        x = (size - img.width) // 2
        y = (size - img.height) // 2
        new_img.paste(img, (x, y))
        img = new_img
    
    # Создаем изображения разных размеров
    sizes = [16, 32, 48, 64, 96, 128, 256]
    icon_images = []
    
    print("Создание изображений разных размеров:")
    for size in sizes:
        # Используем LANCZOS для лучшего качества при уменьшении
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        icon_images.append(resized)
        print(f"  ✓ {size}x{size}")
    
    # Конвертируем каждое изображение в PNG данные
    png_data_list = []
    for icon_img in icon_images:
        from io import BytesIO
        png_buffer = BytesIO()
        icon_img.save(png_buffer, format='PNG')
        png_data_list.append(png_buffer.getvalue())
    
    # Создаем ICO файл вручную
    print(f"\nСоздание ICO файла...")
    
    with open(ico_path, 'wb') as f:
        # ICO Header (6 bytes)
        f.write(struct.pack('<H', 0))  # Reserved
        f.write(struct.pack('<H', 1))  # Type: 1 (ICO)
        f.write(struct.pack('<H', len(sizes)))  # Count
        
        # Directory Entries (16 bytes each)
        data_offset = 6 + len(sizes) * 16
        for i, size in enumerate(sizes):
            png_data = png_data_list[i]
            png_size = len(png_data)
            
            # Width (0 for 256)
            f.write(struct.pack('B', size if size < 256 else 0))
            # Height (0 for 256)
            f.write(struct.pack('B', size if size < 256 else 0))
            # Colors (0 for >8bpp)
            f.write(struct.pack('B', 0))
            # Reserved
            f.write(struct.pack('B', 0))
            # Color planes (1 or 0)
            f.write(struct.pack('<H', 1))
            # Bits per pixel (32 for RGBA)
            f.write(struct.pack('<H', 32))
            # Size of image data
            f.write(struct.pack('<I', png_size))
            # Offset to image data
            f.write(struct.pack('<I', data_offset))
            
            data_offset += png_size
        
        # Image Data (PNG data)
        for png_data in png_data_list:
            f.write(png_data)
    
    file_size = os.path.getsize(ico_path)
    print(f"\n✓ ICO файл создан: {ico_path}")
    print(f"  Размер файла: {file_size:,} байт ({file_size/1024:.2f} KB)")
    print(f"  Включенные размеры: {sizes}")
    
    # Проверяем, что файл имеет разумный размер
    if file_size < 5000:
        print(f"\n⚠ Внимание: Размер файла подозрительно маленький ({file_size} байт)")
        print(f"  Это может указывать на проблему с созданием ICO файла")
        print(f"  Рекомендуется проверить результат в Windows")
    else:
        print(f"\n✓ Размер файла выглядит нормально")

if __name__ == "__main__":
    create_proper_ico("app_icon.png", "app_icon.ico")
