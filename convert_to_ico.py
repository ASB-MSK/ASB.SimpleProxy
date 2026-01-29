from PIL import Image
import sys

def png_to_ico(png_path, ico_path):
    """Конвертирует PNG в ICO с несколькими размерами."""
    img = Image.open(png_path)
    
    # Убедимся, что изображение квадратное
    if img.width != img.height:
        size = max(img.width, img.height)
        new_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        # Центрируем изображение
        x = (size - img.width) // 2
        y = (size - img.height) // 2
        new_img.paste(img, (x, y))
        img = new_img
    
    # Создаём иконку с несколькими размерами для лучшего отображения
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(ico_path, format='ICO', sizes=sizes)
    print(f"✓ Создан: {ico_path}")

if __name__ == "__main__":
    png_to_ico("app_icon.png", "app_icon.ico")
