from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageFilter
import os
import time

def apply_complex_filters(img):
    """Имитация сложной обработки"""
    
    result = img.copy()
    
    
    result.thumbnail((800, 800), Image.Resampling.LANCZOS)
    
    result = result.filter(ImageFilter.SHARPEN)
    result = result.filter(ImageFilter.DETAIL)
    
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(result)
    result = enhancer.enhance(1.2)
    
    time.sleep(0.1)
    
    return result

def optimized_batch_processor(input_folder, output_folder, max_workers=4):
    """Оптимизированная многопоточная версия"""
    
    os.makedirs(output_folder, exist_ok=True)
    
    files = [f for f in os.listdir(input_folder) 
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"Найдено {len(files)} файлов для обработки")
    
    def process_single_file(filename):
        """Обработка одного файла"""
        try:
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"processed_{filename}")
            
            with Image.open(input_path) as img:
                result = apply_complex_filters(img)
                result.save(output_path, optimize=True, quality=85)
            
            return f"Успешно: {filename}"
            
        except Exception as e:
            return f"Ошибка {filename}: {str(e)}"
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(process_single_file, f): f for f in files}
        
        completed_count = 0
        for future in as_completed(future_to_file):
            filename = future_to_file[future]
            try:
                result = future.result()
                completed_count += 1
                print(f"[{completed_count}/{len(files)}] {result}")
            except Exception as e:
                print(f"Ошибка при обработке {filename}: {e}")
    
    end_time = time.time()
    print(f"Обработка завершена за {end_time - start_time:.2f} секунд")
    print(f"Обработано {completed_count} из {len(files)} файлов")

def priority_batch_processor(input_folder, output_folder, max_workers=4):
    """Версия с приоритетной обработкой по размеру файла"""
    
    files = []
    for f in os.listdir(input_folder):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(input_folder, f)
            filesize = os.path.getsize(filepath)
            files.append((filesize, f))
    
    files.sort()
    
    sorted_filenames = [f[1] for f in files]
    
    optimized_batch_processor(input_folder, output_folder, max_workers)
