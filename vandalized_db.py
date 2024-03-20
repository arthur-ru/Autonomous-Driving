import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
from PIL import ImageEnhance, Image as im
import random as rd

n, m = (80, 80)  # taille des images
p = 43  # nombre de classes

def readTrafficSigns(rootpath):
    '''Reads traffic sign data for German Traffic Sign Recognition Benchmark.'''
    images = []  # images
    labels = []  # corresponding labels
    for c in range(0, p):
        prefix = rootpath + '/' + format(c, '05d') + '/'  # subdirectory for class
        gtFile = open(prefix + 'GT-' + format(c, '05d') + '.csv')  # annotations file
        gtReader = csv.reader(gtFile, delimiter=';')  # csv parser for annotations file
        next(gtReader)  # skip header
        for row in gtReader:
            images.append(plt.imread(prefix + row[0]))  # the 1th column is the filename
            labels.append(row[7])  # the 8th column is the label
        gtFile.close()
    return images, labels

data = readTrafficSigns("F:/R&D/GTSRB_Final_Training_Images/GTSRB/Final_Training/Images")

# Création du DataFrame
df = pd.DataFrame({'data': data[0], 'target': data[1]})

# Définition des couleurs en format RGB
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

for i in range(len(df)):
    varimage = df.loc[i, 'data']
    image_pil = im.fromarray(varimage).resize((n, m))
    
    # Appliquez un cache de couleur aléatoire comme précédemment
    cache_size = np.random.randint(n // 10, n // 3)
    random_color = np.random.choice(colors)
    cache_x = np.random.randint((n//2 - cache_size), (n//2 + cache_size))
    cache_y = np.random.randint((m//2 - cache_size), (m//2 + cache_size))
    for x in range(cache_x, cache_x + cache_size):
        for y in range(cache_y, cache_y + cache_size):
            if x < image_pil.width and y < image_pil.height:
                image_pil.putpixel((x, y), tuple(color_map[random_color]))

    # Ajustez la luminosité
    enhancer = ImageEnhance.Brightness(image_pil)
    image_pil = enhancer.enhance(rd.uniform(0.3, 1.7)) 

    # Ajustez la saturation
    enhancer = ImageEnhance.Color(image_pil)
    image_pil = enhancer.enhance(rd.uniform(0.3, 1.7))

    # Ajustez le contraste
    enhancer = ImageEnhance.Contrast(image_pil)
    image_pil = enhancer.enhance(rd.uniform(0.3, 1.7)) 

    # Convertissez l'image PIL modifiée en un tableau numpy pour la stocker ou l'afficher
    varimage_modified = np.array(image_pil)
    
    # Mise à jour de l'image dans le DataFrame
    df.loc[i, 'data'] = np.ndarray.flatten(varimage_modified)  # Si nécessaire

    # Affichage de l'image modifiée
    plt.imshow(varimage_modified)
    plt.show()

