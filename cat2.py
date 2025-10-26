from PIL import Image, ImageStat
import colorsys

def analyze_dominant_color(image_path):
    """
    Проанализировать изображение и определить:
    - Доминирующий цвет (RGB)
    - Цветовую температуру (теплое/холодное/нейтральное)
    - Яркость изображения (темное/среднее/светлое)
    """
    with Image.open(image_path) as img:
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        
        img_small = img.copy()
        img_small.thumbnail((100, 100), Image.Resampling.LANCZOS)
        
        
        stat = ImageStat.Stat(img_small)
        mean_color = tuple(int(c) for c in stat.mean)
        median_color = tuple(int(c) for c in stat.median)
        
        
        dominant_color = median_color
        
        
        r, g, b = [c/255.0 for c in dominant_color]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        
        
        if 0.0 <= h < 0.1 or h >= 0.9:  
            color_temperature = "теплое"
        elif 0.1 <= h < 0.4: 
            color_temperature = "нейтральное" 
        else: 
            color_temperature = "холодное"
        
        
        brightness = v  
        if brightness < 0.3:
            brightness_level = "темное"
        elif brightness < 0.7:
            brightness_level = "среднее"
        else:
            brightness_level = "светлое"
        
        return {
            'dominant_color_rgb': dominant_color,
            'dominant_color_hex': f"#{dominant_color[0]:02x}{dominant_color[1]:02x}{dominant_color[2]:02x}",
            'color_temperature': color_temperature,
            'brightness': brightness_level,
            'hsv_values': (h, s, v)
        }


def test_color_analysis():
    """Тест анализа цвета на разных изображениях"""
    test_results = []
    
    
    colors_to_test = [
        ((255, 100, 100), "теплый красный"),
        ((100, 100, 255), "холодный синий"), 
        ((100, 200, 100), "нейтральный зеленый"),
        ((50, 50, 50), "темный"),
        ((200, 200, 200), "светлый")
    ]
    
    for color, description in colors_to_test:
        img = Image.new('RGB', (100, 100), color)
        img.save(f"./output/test_{description.replace(' ', '_')}.jpg")
        
        analysis = analyze_dominant_color(f"./output/test_{description.replace(' ', '_')}.jpg")
        test_results.append({
            'description': description,
            'expected_color': color,
            'analysis': analysis
        })
    
    return test_results
