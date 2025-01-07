import os

# Create the images directory if it doesn't exist
images_dir = os.path.join('static', 'images')
os.makedirs(images_dir, exist_ok=True)
print(f"Created directory: {images_dir}")
