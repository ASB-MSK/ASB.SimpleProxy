from PIL import Image, ImageDraw, ImageFont
import os

# Create ASB SimpleProxy icon
width, height = 256, 256
img = Image.new('RGBA', (width, height), color=(0, 0, 0, 255))
d = ImageDraw.Draw(img)

# Draw hexagon base
hex_center = (width//2, height//2 - 30)
hex_radius = 60

hex_points = []
for i in range(6):
    angle = (i * 3.14159 / 3) + 3.14159/2  # Start from top
    x = hex_center[0] + hex_radius * 0.8 * (1 if i%2 == 0 else 0.8) * (1 if i < 3 else -1)
    y = hex_center[1] + hex_radius * (1 if i%2 == 0 else 0.8) * (-1 if i < 2 or i == 5 else 1)
    hex_points.append((x, y))

d.polygon(hex_points, fill=(50, 50, 50, 255), outline=(200, 200, 200, 255), width=2)

# Draw abstract "S" shape
path = [
    (hex_center[0] - 30, hex_center[1]),
    (hex_center[0] - 10, hex_center[1] - 20),
    (hex_center[0] + 10, hex_center[1] + 20),
    (hex_center[0] + 30, hex_center[1])
]
d.line(path, fill=(255, 255, 255, 255), width=8)

# Draw pill shape
pill_center = (width//2, height//2 + 20)
pill_width, pill_height = 180, 60

# Left half circle
d.ellipse([(pill_center[0] - pill_width//2, pill_center[1] - pill_height//2), 
           (pill_center[0] - pill_width//2 + pill_height, pill_center[1] + pill_height//2)], 
          fill=(30, 144, 255, 255))

# Middle rectangle
d.rectangle([(pill_center[0] - pill_width//2 + pill_height//2, pill_center[1] - pill_height//2), 
             (pill_center[0] + pill_width//2 - pill_height//2, pill_center[1] + pill_height//2)], 
            fill=(30, 144, 255, 255))

# Right half circle
d.ellipse([(pill_center[0] + pill_width//2 - pill_height, pill_center[1] - pill_height//2), 
           (pill_center[0] + pill_width//2, pill_center[1] + pill_height//2)], 
          fill=(0, 206, 209, 255))

# Draw center circle
d.ellipse([(pill_center[0] - 20, pill_center[1] - 20), 
           (pill_center[0] + 20, pill_center[1] + 20)], 
          fill=(0, 0, 0, 255))

# Draw inner lines
for i in range(5):
    line_y = pill_center[1] - 20 + i * 10
    d.line([(pill_center[0] - 40, line_y), (pill_center[0] - 20, line_y)], 
           fill=(0, 0, 0, 128), width=2)

# Draw "ASB" text
asb_text = "ASB"
asb_font = ImageFont.truetype("arial.ttf", 36) if os.path.exists("arial.ttf") else ImageFont.load_default()
asb_bbox = d.textbbox((0, 0), asb_text, font=asb_font)
asb_text_width = asb_bbox[2] - asb_bbox[0]
asb_text_height = asb_bbox[3] - asb_bbox[1]
asb_text_x = width//2 - asb_text_width//2
asb_text_y = pill_center[1] + pill_height//2 + 10
d.text((asb_text_x, asb_text_y), asb_text, font=asb_font, fill=(255, 255, 255, 255))

# Draw "SimpleProxy" text
sp_text = "SimpleProxy"
sp_font = ImageFont.truetype("arial.ttf", 24) if os.path.exists("arial.ttf") else ImageFont.load_default()
sp_bbox = d.textbbox((0, 0), sp_text, font=sp_font)
sp_text_width = sp_bbox[2] - sp_bbox[0]
sp_text_x = width//2 - sp_text_width//2
sp_text_y = asb_text_y + asb_text_height + 5
d.text((sp_text_x, sp_text_y), sp_text, font=sp_font, fill=(30, 144, 255, 255))

# Save as PNG
img.save('app_icon.png', format='PNG')
print(f"Created app_icon.png: {os.path.getsize('app_icon.png')} bytes")

# Convert to ICO
img.save('app_icon.ico', format='ICO')
print(f"Created app_icon.ico: {os.path.getsize('app_icon.ico')} bytes")

print("Icon generation completed successfully!")
