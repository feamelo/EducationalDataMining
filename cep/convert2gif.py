############ Análise de dados educacionais - TCC Fernanda e Luiz ############
# Autores: Fernanda Amaral Melo e Luiz Fernando Araújo 
# Contato: fernanda.amaral.melo@gmail.com e luizfna@gmail.com

# Script usado para inserir o título "semestre/ano" e transformar em gif
# os gráficos de calor gerados pela correlação entre o CEP e o IRA dos 
# alunos de Engenharia de computação da UnB 

from matplotlib import pyplot as plt
import imageio
import numpy as np
import os.path    
from os import path
import cv2

year = 2009
semester = -1
images = []

for i in range(0,33):
    semester = semester + 1
    if semester == 3:
        semester = 0
        year = year + 1
    if path.exists('heatmap_ira/picture/map' + str(i) + '.png'):
        image = cv2.imread('heatmap_ira/picture/map' + str(i) + '.png')
        texted_image =cv2.putText(img=np.copy(image), text= str(year) + '/' + str(semester), org=(100,150),fontFace=3, fontScale=2, color=(0,0,0), thickness=5)
        images.append(texted_image)

imageio.mimsave(os.path.join('heatmap_ira.gif'), images, duration = 0.5)
print("Done")


