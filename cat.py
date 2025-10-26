from PIL import Image, ImageDraw  
import random

def create_collage_from_folder(folder_path, output_path, rows=2, cols=2):
    """Исправленная функция создания коллажа"""
    
    images = []
    for file in os.listdir(folder_path):
        if file.endswith('.jpg'):
            
            img_path = os.path.join(folder_path, file)
            img = Image.open(img_path)
            images.append(img)
    
    if len(images) < rows * cols:
        print("Недостаточно изображений")
        return
    
    
    thumbnail_size = (200, 200)
    
    collage_width = cols * thumbnail_size[0]
    collage_height = rows * thumbnail_size[1]
    collage = Image.new('RGB', (collage_width, collage_height))
    
    for i in range(rows):
        for j in range(cols):
            index = i * cols + j
            if index < len(images):
                
                img_resized = images[index].copy()
                img_resized.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
                
                x = j * thumbnail_size[0]
                y = i * thumbnail_size[1]
                collage.paste(img_resized, (x, y))
    
    collage.save(output_path)
    print(f"Коллаж сохранен: {output_path}")

def create_smart_gradient(size=(400, 400), start_color=(255,0,0), end_color=(0,0,255)):
    """Исправленная функция создания градиента"""
    img = Image.new('RGB', size, color=start_color)
    draw = ImageDraw.Draw(img)
    
    for x in range(size[0]):
        for y in range(size[1]):
            t = (x + y) / (size[0] + size[1])
            
            r = start_color[0] + (end_color[0] - start_color[0]) * t
            g = start_color[1] + (end_color[1] - start_color[1]) * t
            b = start_color[2] + (end_color[2] - start_color[2]) * t
            
           
            r = max(0, min(255, int(r)))
            g = max(0, min(255, int(g)))
            b = max(0, min(255, int(b)))
            
            draw.point((x, y), fill=(r, g, b))
    
    return img

def create_smart_gradient_optimized(size=(400, 400), start_color=(255,0,0), end_color=(0,0,255)):
    """Оптимизированная версия с использованием numpy-подобного подхода"""
    img = Image.new('RGB', size)
    pixels = img.load()
    
    for x in range(size[0]):
        for y in range(size[1]):
            t = (x + y) / (size[0] + size[1])
            
            r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * t)
            
            pixels[x, y] = (r, g, b)
    
    return img

