from PIL import Image, ImageEnhance
import random as rd
import csv
import matplotlib.pyplot as plt
import numpy as np

# definition of image size and number of classes
image_size = 30
n, m = (image_size, image_size)
p = 43
vandalized_proportion = 0.7

# color mapping
color_map = {
    'red': [255, 0, 0],
    'blue': [0, 0, 255],
    'green': [0, 255, 0],
    'yellow': [255, 255, 0],
    'orange': [255, 165, 0],
    'purple': [128, 0, 128],
    'white': [255, 255, 255],
    'black': [0, 0, 0]
}
colors = list(color_map.keys())

shapes = ['square', 'triangle', 'rectangle', 'circle']

def modifyTrafficSigns(rootpath):
    modified_count = 0  # counter for modified images
    for c in range(0, p):
        print(f"Début de la modification pour la classe {c}...")
        prefix = rootpath + '/' + format(c, '05d') + '/'
        gtFile = open(prefix + 'GT-' + format(c, '05d') + '.csv')
        gtReader = csv.reader(gtFile, delimiter=';')
        next(gtReader)
        
        for row in gtReader:
            vand_sign = rd.random()
            if vand_sign < vandalized_proportion :
                image_path = prefix + row[0]

                # Visual image modification
                image_pil = Image.open(image_path)
                x, y = image_pil.size
                [x1, y1, x2, y2] = map(int, row[3:7])
                # print(f"Image size : {x} x {y}")
                # print(f"x1 = {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}")
                
                cache_size = rd.randint((x2 - x1) // 10, (x2 - x1) // 3)
                cache_shape = np.random.choice(shapes)
                random_color = rd.choice(colors)

                cache_x = rd.randint(x1 + cache_size, x2 - 2*cache_size)
                cache_y = rd.randint(y1 + round(0.5*cache_size), y2 - round(1.5*cache_size))
                # print(f"Cache add of color {random_color} and {cache_shape} shape.")

                if cache_shape == 'square':
                    for x in range(cache_x, cache_x + cache_size):
                        for y in range(cache_y, cache_y + cache_size):
                            if x < image_pil.width and y < image_pil.height:
                                # image_pil.putpixel((x, y), tuple(color_map[random_color]))
                                random_color = (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))
                                image_pil.putpixel((x, y), random_color)

                elif cache_shape == 'triangle':
                    for x in range(cache_x, cache_x + cache_size):
                        for y in range(cache_y, cache_y + cache_size):
                            if x < image_pil.width and y < image_pil.height and y < cache_y + cache_size - (x - cache_x):
                                # image_pil.putpixel((x, y), tuple(color_map[random_color]))
                                random_color = (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))
                                image_pil.putpixel((x, y), random_color)

                elif cache_shape == 'rectangle':
                    cache_height = rd.randint((x2 - x1) // 10, (x2 - x1) // 3)
                    for x in range(cache_x, cache_x + cache_size):
                        for y in range(cache_y, cache_y + cache_height):
                            if x < image_pil.width and y < image_pil.height:
                                # image_pil.putpixel((x, y), tuple(color_map[random_color]))
                                random_color = (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))
                                image_pil.putpixel((x, y), random_color)
                    
                elif cache_shape == 'circle':
                    for x in range(cache_x - cache_size, cache_x + cache_size):
                        for y in range(cache_y - cache_size, cache_y + cache_size):
                            if x < image_pil.width and y < image_pil.height and (x - cache_x) ** 2 + (y - cache_y) ** 2 <= cache_size ** 2:
                                # image_pil.putpixel((x, y), tuple(color_map[random_color]))
                                random_color = (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))
                                image_pil.putpixel((x, y), random_color)

            image_pil = image_pil.resize((n, m))
            
            # modify brightness, color and contrast in the image
            enhancer = ImageEnhance.Brightness(image_pil)
            image_pil = enhancer.enhance(rd.uniform(0.3, 1.7))
            enhancer = ImageEnhance.Color(image_pil)
            image_pil = enhancer.enhance(rd.uniform(0.3, 1.7))
            enhancer = ImageEnhance.Contrast(image_pil)
            image_pil = enhancer.enhance(rd.uniform(0.3, 1.7))
                
            # save image
            image_pil.save(image_path)

            # plt.imshow(image_pil)
            # plt.show()
                
            modified_count += 1
            if modified_count % 1000 == 0:  # message every 1000 modifications
                print(f"{modified_count} images modifiées...")
        
        gtFile.close()
    print(f"Modification terminée. Total d'images modifiées : {modified_count}.")

# access path
rootpath = "F:/R&D/BDDs/GTSRB_random_0.7/Final_Training/Images"
modifyTrafficSigns(rootpath)
