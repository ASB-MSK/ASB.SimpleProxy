from PIL import Image
import io
import os

# Path to the downloaded image
input_path = "app_icon.ico"
output_path = "app_icon.ico"

# Check if the file exists
if not os.path.exists(input_path):
    print(f"File {input_path} not found!")
    exit(1)

# Try to open with PIL
print(f"Opening image: {input_path}")
try:
    # Open the image
    img = Image.open(input_path)
    print(f"Original format: {img.format}")
    print(f"Original size: {img.size}")
    
    # Convert to PNG first (to ensure compatibility)
    png_buffer = io.BytesIO()
    img.save(png_buffer, format='PNG')
    png_buffer.seek(0)
    
    # Create a new image with ICO format
    print(f"Converting to ICO format...")
    ico_img = Image.open(png_buffer)
    
    # Save as ICO
    ico_img.save(output_path, format='ICO')
    print(f"Successfully converted to ICO format: {output_path}")
    print(f"File size: {os.path.getsize(output_path)} bytes")
    
except Exception as e:
    print(f"Error: {e}")
