from PIL import Image, ImageDraw
import numpy as np

def create_textured_background(width=1920, height=1080, base_color=(237, 237, 237), noise_intensity=5):
    # 创建基础图像 - 使用完全相同的背景色
    image = Image.new('RGB', (width, height), base_color)
    
    # 创建非常轻微的噪声
    noise = np.random.normal(0, 0.5, (height, width)) * noise_intensity
    
    # 将噪声应用到整个图像
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            noise_value = int(noise[y, x])
            
            # 确保颜色变化非常细微
            blend_factor = 0.95  # 95% 原始颜色
            new_r = int(r * blend_factor + min(255, r + noise_value) * (1 - blend_factor))
            new_g = int(g * blend_factor + min(255, g + noise_value) * (1 - blend_factor))
            new_b = int(b * blend_factor + min(255, b + noise_value) * (1 - blend_factor))
            
            pixels[x, y] = (new_r, new_g, new_b)
    
    return image

if __name__ == "__main__":
    # 创建更柔和的背景图
    background = create_textured_background(noise_intensity=5)
    
    # 保存图像
    background.save('background.png')
    print("背景图片已生成：background.png")
