from PIL import ImageFilter, ImageEnhance
import math

def classify_image_type(img):
    """Классифицирует тип изображения на основе анализа характеристик"""
    
    img_small = img.copy()
    img_small.thumbnail((200, 200), Image.Resampling.LANCZOS)
    
    hsv_img = img_small.convert('HSV')
    hsv_pixels = list(hsv_img.getdata())
    
    hue_values = [p[0] for p in hsv_pixels]
    sat_values = [p[1] for p in hsv_pixels] 
    val_values = [p[2] for p in hsv_pixels]
    
    green_hues = sum(1 for h in hue_values if 40 <= h <= 90)  
    skin_hues = sum(1 for h in hue_values if 0 <= h <= 25 or 160 <= h <= 180)  
    high_saturation = sum(1 for s in sat_values if s > 150) 
    low_brightness = sum(1 for v in val_values if v < 80) 
    high_contrast = max(val_values) - min(val_values)  
    
    total_pixels = len(hue_values)
    
    
    if green_hues / total_pixels > 0.3 and high_saturation / total_pixels > 0.2:
        return "пейзаж"
    elif skin_hues / total_pixels > 0.2:
        return "портрет"
    elif high_contrast > 150 and low_brightness / total_pixels > 0.4:
        return "ночное"
    elif high_contrast > 100 and sum(val_values) / total_pixels < 150:
        return "текст"
    else:
        return "неизвестно"

def smart_processing(image_path, output_path):
    """
    Автоматически определить тип изображения и применить оптимальную обработку
    """
    with Image.open(image_path) as img:
        image_type = classify_image_type(img)
        print(f"Определен тип: {image_type}")
        
        result = img.copy()
        
        if image_type == "портрет":
            
            enhancer = ImageEnhance.Color(result)
            result = enhancer.enhance(1.1)
            
            
            result = result.filter(ImageFilter.GaussianBlur(0.7))
            
           
            result = result.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
            
        elif image_type == "пейзаж":
            
            color_enhancer = ImageEnhance.Color(result)
            result = color_enhancer.enhance(1.3)
            
            contrast_enhancer = ImageEnhance.Contrast(result)  
            result = contrast_enhancer.enhance(1.2)
            
            sharpness_enhancer = ImageEnhance.Sharpness(result)
            result = sharpness_enhancer.enhance(1.5)
            
        elif image_type == "текст":
           
            contrast_enhancer = ImageEnhance.Contrast(result)
            result = contrast_enhancer.enhance(2.0)
            
           
            sharpness_enhancer = ImageEnhance.Sharpness(result)
            result = sharpness_enhancer.enhance(3.0)
            
           
            if result.mode != 'L':
                result = result.convert('L')
                
        elif image_type == "ночное":
            
            result = result.filter(ImageFilter.MedianFilter(size=3))
            
            
            brightness_enhancer = ImageEnhance.Brightness(result)
            result = brightness_enhancer.enhance(1.3)
            
           
            contrast_enhancer = ImageEnhance.Contrast(result)
            result = contrast_enhancer.enhance(1.2)
        
        
        name, ext = os.path.splitext(output_path)
        typed_output_path = f"{name}_{image_type}{ext}"
        result.save(typed_output_path, quality=95)
        
        return {
            'image_type': image_type,
            'output_path': typed_output_path
        }
