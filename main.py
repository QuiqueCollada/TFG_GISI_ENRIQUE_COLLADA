from jinja2 import Environment, FileSystemLoader
import pdfkit
from PIL import Image 
import matplotlib.pyplot as plt
import pandas as pd

# SECCIÓN 1. Procesado y recorte de las imágenes producidas por FSLeyes y ANTs para incluirlas en el informe.

# Opens a image in RGB mode 
imT1 = Image.open("./Img_lesion/ImagenT1.png")
imT2 = Image.open("./Img_lesion/ImagenT2.png")
imSWAN = Image.open("./Img_lesion/ImagenSWAN.png")
imFLAIR = Image.open("./Img_lesion/ImagenFLAIR.png")
  
# Setting the points for cropped image 
x1 = 0
y1 = 140
x2 = 798
y2 = 600 - 130
  
# Cropped image of above dimension 
# (It will not change orginal image) 
imT2cr = imT2.crop((x1, y1, x2, y2))
imT2cr.save("./Img_lesion/ImagenT2_crop.png")
imT1cr = imT1.crop((x1, y1, x2, y2))
imT1cr.save("./Img_lesion/ImagenT1_crop.png")
imSWANcr = imSWAN.crop((x1, y1, x2, y2))
imSWANcr.save("./Img_lesion/ImagenSWAN_crop.png")
imFLAIRcr = imFLAIR.crop((x1, y1, x2, y2))
imFLAIRcr.save("./Img_lesion/ImagenFLAIR_crop.png")

# Opens a image in RGB mode
im_mosaicoT1 = Image.open("./Img_lesion/mosaicoT1.png")
im_mosaicoT2 = Image.open("./Img_lesion/mosaicoT2.png")
im_mosaicoFLAIR = Image.open("./Img_lesion/mosaicoFLAIR.png")
im_mosaicoSWAN = Image.open("./Img_lesion/mosaicoSWAN.png")

# Setting the points for cropped image 
x3 = 165
y3 = 0
x4 = 800 - 165
y4 = 600

imMosaicoT1cr = im_mosaicoT1.crop((x3, y3, x4, y4))
imMosaicoT1cr.save("./Img_lesion/MosaicoT1_crop.png")
imMosaicoT2cr = im_mosaicoT2.crop((x3, y3, x4, y4))
imMosaicoT2cr.save("./Img_lesion/MosaicoT2_crop.png")
imMosaicoFLAIRcr = im_mosaicoFLAIR.crop((x3, y3, x4, y4))
imMosaicoFLAIRcr.save("./Img_lesion/MosaicoFLAIR_crop.png")
imMosaicoSWANcr = im_mosaicoSWAN.crop((x3, y3, x4, y4))
imMosaicoSWANcr.save("./Img_lesion/MosaicoSWAN_crop.png")

# SECCIÓN 2. Inclusión de las características topográficas de la lesión en el informe.

# Cargo los datos del paciente de un fichero csv
dfp = pd.read_csv('./Lesion_Segmentation_id023/Topography_Report/outstats_single_subject.txt')

# Cargo en variables las características del paciente sobre el que se genera el informe para incluirlas como variables que pasar al html
volp = dfp['natvol'].iloc[0]
dPCp = dfp['dPC'].iloc[0]
latICLp = dfp['latICL'].iloc[0]
dPCPercp = dfp['dPCPerc'].iloc[0]
dInfACPCp = dfp['dInfACPC'].iloc[0]
VIMoccupiedp = dfp['VIMoccupied'].iloc[0]
LesioninVIMp = dfp['LesioninVIM'].iloc[0]

# SECCIÓN 3. Generación de los gráficos para la comparación estadística con una población de pacientes.

# Leo los ficheros csv con información del otros pacientes
df1 = pd.read_csv('outstats.txt')
df2 = pd.read_excel('bd_pacientes.xlsx')

# Uso la función merge para generar un único fichero haciendo un "outer join"
fichero_unico = pd.merge(df1, df2,
				on='id',
				how='outer')

fichero_unico.to_excel('fichero_unico.xlsx')

# Cargo el fichero único en un nuevo dataframe
df = pd.read_excel('fichero_unico.xlsx')

# Cargo las características de la lesión que voy a comparar con la mejoría clínica
volumen = df['natvol']
dPC = df['dPC']
latICL = df['latICL']
dPCPerc = df['dPCPerc']
dInfACPC = df['dInfACPC']
VIMoccupied = df['VIMoccupied']
LesioninVIM = df['LesioninVIM']

# Cargo las columnas de mejoría clínica (en unidades absolutas y relativas)
mejoria_abs = df['Mejoria_Abs_HT']
mejoria_rel = df['Mejoria_Rel_HT']

# Creo una figura con 2 subplots, relacionado el volumen con la mejoría relativa y con la absoluta
fig = plt.figure(figsize=(14,6)) # Establezco las dimensiones de la figura con ambos subplots
ax1 = fig.add_subplot(121) # Añado un subplot
ax2 = fig.add_subplot(122)

ax1.title.set_text('Relación volumen - mejoría clínica relativa')
#Establezco los ejes x e y del gráfico
x = volumen
y = mejoria_rel
# Genero el gráfico de dispersión del primer subplot
ax1.scatter(x,y, edgecolor='black',linewidth=1,alpha=0.75,)
ax1.axvline(x=volp, color = 'red') # Dibujo una línea roja en el dato específico del paciente
ax1.set_ylabel('Mejoría (%)') # Añado la etiqueta el eje y
ax1.set_xlabel('Volumen (mm3)') # Añado la etiqueta el eje x

ax2.title.set_text('Relación volumen - mejoría clínica absoluta') # Añado un título al gráfico
y = mejoria_abs # Cambio el eje y para que pase a representar la mejoría clínica en valores absolutos
ax2.scatter(x,y, edgecolor='black',linewidth=1,alpha=0.75,)
ax2.axvline(x=volp, color = 'red')
ax2.set_ylabel('Mejoría')
ax2.set_xlabel('Volumen (mm3)')

# Guardo la figura en una imagen png de alta calidad
plt.savefig('./Graficos/volumen_mejoria.png', dpi=200)

# Figura 2: relación entre la lateralidad y la mejoría
fig = plt.figure(figsize=(14,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.title.set_text('Relación lateralidad - mejoría clínica relativa')
x = latICL
y = mejoria_rel
ax1.scatter(x,y, edgecolor='black',linewidth=1,alpha=0.75,)
ax1.axvline(x=latICLp, color = 'red') # Dibujo una línea roja en el dato específico del paciente
ax1.set_ylabel('Mejoría (%)')
ax1.set_xlabel('Lateralidad (mm)')

ax2.title.set_text('Relación lateralidad - mejoría clínica absoluta')
y = mejoria_abs
ax2.scatter(x,y, edgecolor='black',linewidth=1,alpha=0.75,)
ax2.axvline(x=latICLp, color = 'red')
ax2.set_ylabel('Mejoría')
ax2.set_xlabel('Lateralidad (mm)')

plt.savefig('./Graficos/lateralidad_mejoria.png', dpi=200)

# Figura 3: relación entre la distancia PC y la mejoría
fig = plt.figure(figsize=(14,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.title.set_text('Relación distancia comisura posterior - mejoría clínica relativa')
x = dPC
y = mejoria_rel
ax1.scatter(x,y, edgecolor='black',linewidth=1,alpha=0.75,)
ax1.axvline(x=dPCp, color = 'red') # Dibujo una línea roja en el dato específico del paciente
ax1.set_ylabel('Mejoría (%)')
ax1.set_xlabel('Distancia PC (mm)')

ax2.title.set_text('Relación distancia comisura posterior - mejoría clínica absoluta')
y = mejoria_abs
ax2.scatter(x,y, edgecolor='black',linewidth=1,alpha=0.75,)
ax2.axvline(x=dPCp, color = 'red')
ax2.set_ylabel('Mejoría')
ax2.set_xlabel('Distancia PC (mm)')

plt.savefig('./Graficos/dPC_mejoria.png', dpi=200)

# Figura 4: relación entre dPCPerc y la mejoría
fig = plt.figure(figsize=(14,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.title.set_text('Porcentaje del segmento comisura anterior-posterior - mejoría relativa')
x = dPCPerc
y = mejoria_rel
ax1.scatter(x,y, edgecolor='black',linewidth=1,alpha=0.75,)
ax1.axvline(x=dPCPercp, color = 'red') # Dibujo una línea roja en el dato específico del paciente
ax1.set_ylabel('Mejoría (%)')
ax1.set_xlabel('Porcentaje segmento entre comisuras (%)')

ax2.title.set_text('Porcentaje del segmento comisura anterior-posterior - mejoría absoluta')
y = mejoria_abs
ax2.scatter(x,y, edgecolor='black',linewidth=1,alpha=0.75,)
ax2.axvline(x=dPCPercp, color = 'red')
ax2.set_ylabel('Mejoría')
ax2.set_xlabel('Porcentaje segmento entre comisuras (%)')

plt.savefig('./Graficos/dPCperc_mejoria.png', dpi=200)

# Figura 5: relación entre la distancia inferior al plano AC-PC y la mejoría
fig = plt.figure(figsize=(14,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.title.set_text('Relación distancia inferior al plano AC-PC - mejoría clínica relativa')
x = dInfACPC
y = mejoria_rel
ax1.scatter(x,y, edgecolor='black',linewidth=1,alpha=0.75,)
ax1.axvline(x=dInfACPCp, color = 'red') # Dibujo una línea roja en el dato específico del paciente
ax1.set_ylabel('Mejoría (%)')
ax1.set_xlabel('Distancia inferior al plano AC-PC (mm)')

ax2.title.set_text('Relación distancia inferior al plano AC-PC - mejoría clínica absoluta')
y = mejoria_abs
ax2.scatter(x,y, edgecolor='black',linewidth=1,alpha=0.75,)
ax2.axvline(x=dInfACPCp, color = 'red')
ax2.set_ylabel('Mejoría')
ax2.set_xlabel('Distancia inferior al plano AC-PC (mm)')

plt.savefig('./Graficos/dInfACPC_mejoria.png', dpi=200)

# Figura 6: relación entre el porcentaje de VIM ocupado por la lesión y la mejoría
fig = plt.figure(figsize=(14,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.title.set_text('Relación VIM ocupado - mejoría clínica relativa')
x = VIMoccupied
y = mejoria_rel
ax1.scatter(x,y, edgecolor='black',linewidth=1,alpha=0.75,)
ax1.axvline(x=VIMoccupiedp, color = 'red') # Dibujo una línea roja en el dato específico del paciente
ax1.set_ylabel('Mejoría (%)')
ax1.set_xlabel('VIM ocupado (%)')

ax2.title.set_text('Relación VIM ocupado - mejoría clínica absoluta')
y = mejoria_abs
ax2.scatter(x,y, edgecolor='black',linewidth=1,alpha=0.75,)
ax2.axvline(x=VIMoccupiedp, color = 'red')
ax2.set_ylabel('Mejoría')
ax2.set_xlabel('VIM ocupado (%)')

plt.savefig('./Graficos/VIMoccupied_mejoria.png', dpi=200)

# Figura 7: relación entre el porcentaje de lesión en el VIM por la lesión y la mejoría
fig = plt.figure(figsize=(14,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.title.set_text('Relación lesión en VIM - mejoría clínica relativa')
x = LesioninVIM
y = mejoria_rel
ax1.scatter(x,y, edgecolor='black',linewidth=1,alpha=0.75,)
ax1.axvline(x=LesioninVIMp, color = 'red') # Dibujo una línea roja en el dato específico del paciente
ax1.set_ylabel('Mejoría (%)')
ax1.set_xlabel('Lesión en VIM (%)')

ax2.title.set_text('Relación lesión en VIM - mejoría clínica absoluta')
y = mejoria_abs
ax2.scatter(x,y, edgecolor='black',linewidth=1,alpha=0.75,)
ax2.axvline(x=LesioninVIMp, color = 'red')
ax2.set_ylabel('Mejoría')
ax2.set_xlabel('Lesión en VIM (%)')

plt.savefig('./Graficos/LesioninVIM_mejoria.png', dpi=200)

# Comparo las características de la lesión con la aparición de ataxia y parestesia a los 3 meses

df_atax = df[(df['Atax_3M'] == 1)] # Filtro por aquellos que tienen Ataxia
df_natax = df[(df['Atax_3M'] == 0)] # Filtro por aquellos que NO tienen Ataxia
df_pares = df[(df['Pares_3M'] == 1)] # Filtro por aquellos que tienen Ataxia
df_npares = df[(df['Pares_3M'] == 0)] # Filtro por aquellos que NO tienen Ataxia

# Figura 8: relación entre el volumen de la lesión y la aparición de ataxia y parestesia

vol_atax = df_atax['natvol'].dropna()  # Extraigo el volumen de aquellos que tienen ataxia y elimino los valores NaN        
vol_natax = df_natax['natvol'].dropna()
vol_pares = df_pares['natvol'].dropna()  # Extraigo el volumen de aquellos que tienen ataxia y elimino los valores NaN        
vol_npares = df_npares['natvol'].dropna()
vol_ap = [vol_natax,vol_atax,vol_npares,vol_pares]
  
fig = plt.figure(figsize =(10, 7))
plt.boxplot(vol_ap)
plt.title("Relación entre el volumen de la lesión y la aparición de ataxia y parestesia")
plt.ylabel('Volumen (mm3)')
plt.axhline(y=volp, color = 'red')
plt.xticks([1, 2, 3, 4], ['Sin ataxia', 'Con ataxia', 'Sin parestesia', 'Con parestesia'])

plt.savefig('./Graficos/volumen_ataxia_parestesia.png', dpi=200)

# Figura 9: relación entre la lateralidad y la aparición de ataxia y parestesia

latICL_atax = df_atax['latICL'].dropna()       
latICL_natax = df_natax['latICL'].dropna()
latICL_pares = df_pares['latICL'].dropna()        
latICL_npares = df_npares['latICL'].dropna()
latICL_ap = [latICL_natax,latICL_atax,latICL_npares,latICL_pares]
  
fig = plt.figure(figsize =(10, 7))
plt.boxplot(latICL_ap)
plt.title("Relación entre la lateralidad de la lesión y la aparición de ataxia y parestesia")
plt.ylabel('Lateralidad (mm)')
plt.axhline(y=latICLp, color = 'red')
plt.xticks([1, 2, 3, 4], ['Sin ataxia', 'Con ataxia', 'Sin parestesia', 'Con parestesia'])

plt.savefig('./Graficos/latICL_ataxia_parestesia.png', dpi=200)

# Figura 10: relación entre la distancia PC y la aparición de ataxia y parestesia

dPC_atax = df_atax['dPC'].dropna()       
dPC_natax = df_natax['dPC'].dropna()
dPC_pares = df_pares['dPC'].dropna()        
dPC_npares = df_npares['dPC'].dropna()
dPC_ap = [dPC_natax,dPC_atax,dPC_npares,dPC_pares]
  
fig = plt.figure(figsize =(10, 7))
plt.boxplot(dPC_ap)
plt.title("Relación entre la distancia PC y la aparición de ataxia y parestesia")
plt.ylabel('Distancia PC (mm)')
plt.axhline(y=dPCp, color = 'red')
plt.xticks([1, 2, 3, 4], ['Sin ataxia', 'Con ataxia', 'Sin parestesia', 'Con parestesia'])

plt.savefig('./Graficos/dPC_ataxia_parestesia.png', dpi=200)

# Figura 11: relación entre la distancia PC (%) y la aparición de ataxia y parestesia

dPCPerc_atax = df_atax['dPCPerc'].dropna()       
dPCPerc_natax = df_natax['dPCPerc'].dropna()
dPCPerc_pares = df_pares['dPCPerc'].dropna()        
dPCPerc_npares = df_npares['dPCPerc'].dropna()
dPCPerc_ap = [dPCPerc_natax,dPCPerc_atax,dPCPerc_npares,dPCPerc_pares]
  
fig = plt.figure(figsize =(10, 7))
plt.boxplot(dPCPerc_ap)
plt.title("Relación entre la distancia PC (%) y la aparición de ataxia y parestesia")
plt.ylabel('Distancia PC (%)')
plt.axhline(y=dPCPercp, color = 'red')
plt.xticks([1, 2, 3, 4], ['Sin ataxia', 'Con ataxia', 'Sin parestesia', 'Con parestesia'])

plt.savefig('./Graficos/dPCPerc_ataxia_parestesia.png', dpi=200)

# Figura 12: relación entre la distancia inferior al plano AC-PC y la aparición de ataxia y parestesia

dInfACPC_atax = df_atax['dInfACPC'].dropna()       
dInfACPC_natax = df_natax['dInfACPC'].dropna()
dInfACPC_pares = df_pares['dInfACPC'].dropna()        
dInfACPC_npares = df_npares['dInfACPC'].dropna()
dInfACPC_ap = [dInfACPC_natax,dInfACPC_atax,dInfACPC_npares,dInfACPC_pares]
  
fig = plt.figure(figsize =(10, 7))
plt.boxplot(dInfACPC_ap)
plt.title("Relación entre la distancia inferior al plano AC-PC y la aparición de ataxia y parestesia")
plt.ylabel('Distancia inferior AC-PC (mm)')
plt.axhline(y=dInfACPCp, color = 'red')
plt.xticks([1, 2, 3, 4], ['Sin ataxia', 'Con ataxia', 'Sin parestesia', 'Con parestesia'])

plt.savefig('./Graficos/dInfACPC_ataxia_parestesia.png', dpi=200)

# Figura 13: relación entre el VIM ocupado y la aparición de ataxia y parestesia

VIMoccupied_atax = df_atax['VIMoccupied'].dropna()       
VIMoccupied_natax = df_natax['VIMoccupied'].dropna()
VIMoccupied_pares = df_pares['VIMoccupied'].dropna()        
VIMoccupied_npares = df_npares['VIMoccupied'].dropna()
VIMoccupied_ap = [VIMoccupied_natax,VIMoccupied_atax,VIMoccupied_npares,VIMoccupied_pares]
  
fig = plt.figure(figsize =(10, 7))
plt.boxplot(VIMoccupied_ap)
plt.title("Relación entre el VIM ocupado y la aparición de ataxia y parestesia")
plt.ylabel('VIM ocupado (%)')
plt.axhline(y=VIMoccupiedp, color = 'red')
plt.xticks([1, 2, 3, 4], ['Sin ataxia', 'Con ataxia', 'Sin parestesia', 'Con parestesia'])

plt.savefig('./Graficos/VIMoccupied_ataxia_parestesia.png', dpi=200)

# Figura 14: relación entre la porción de lesión en el VIM y la aparición de ataxia y parestesia

LesioninVIM_atax = df_atax['LesioninVIM'].dropna()       
LesioninVIM_natax = df_natax['LesioninVIM'].dropna()
LesioninVIM_pares = df_pares['LesioninVIM'].dropna()        
LesioninVIM_npares = df_npares['LesioninVIM'].dropna()
LesioninVIM_ap = [LesioninVIM_natax,LesioninVIM_atax,LesioninVIM_npares,LesioninVIM_pares]
  
fig = plt.figure(figsize =(10, 7))
plt.boxplot(LesioninVIM_ap)
plt.title("Relación entre la lesión en el VIM y la aparición de ataxia y parestesia")
plt.ylabel('Lesión en VIM (%)')
plt.axhline(y=LesioninVIMp, color = 'red')
plt.xticks([1, 2, 3, 4], ['Sin ataxia', 'Con ataxia', 'Sin parestesia', 'Con parestesia'])

plt.savefig('./Graficos/LesioninVIM_ataxia_parestesia.png', dpi=200)


# Creación de los ficheros html y pdf

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("myreport.html")

# Pasamos las variables a la plantilla html
template_vars = {"volumen": volp, "dPC": dPCp,"dPCPerc": dPCPercp, "latICL": latICLp,"dInfACPC": dInfACPCp,"VIMoccupied": VIMoccupiedp,"LesioninVIM": LesioninVIMp, "document_title": "Informe automatizado de topografía de la lesión talámica mediante ultrasonido focal de alta intensidad","Autor" : "Enrique"}

html_out = template.render(template_vars)
Html_file = open("report.html","w")
Html_file.write(html_out)
Html_file.close()

options = {'enable-local-file-access': None, 'footer-center': '[page]'}
pdfkit.from_file('report.html', 'report.pdf',options = options)