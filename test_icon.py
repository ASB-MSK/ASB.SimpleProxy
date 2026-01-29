from PIL import Image, ImageDraw, ImageFont
import os

# Create a simple test image
img = Image.new('RGB', (256, 256), color='black')
d = ImageDraw.Draw(img)

# Draw a simple shape
d.ellipse([(64, 64), (192, 192)], fill='blue', outline='white')

# Save as PNG
img.save('test_icon.png', format='PNG')
print(f"Created test_icon.png: {os.path.getsize('test_icon.png')} bytes")

# Try to open it
img2 = Image.open('test_icon.png')
print(f"Opened test_icon.png: {img2.format}, {img2.size}")
