import os
import pandas as pd

# Leo el fichero csv que contiene las coordenadas del centroide de la lesión y lo cargo en un dataframe
df = pd.read_csv('./Lesion_Segmentation_id023/Topography_Report/outstats_single_subject.txt')

# Cargo las coordenadas del centroide en variables
xT2 = int(df['cenx_T2'].iloc[0])
yT2 = int(df['ceny_T2'].iloc[0])
zT2 = int(df['cenz_T2'].iloc[0])

xT1 = int(df['cenx_T1'].iloc[0])
yT1 = int(df['ceny_T1'].iloc[0])
zT1 = int(df['cenz_T1'].iloc[0])

xF = int(df['cenx_FLAIR'].iloc[0])
yF = int(df['ceny_FLAIR'].iloc[0])
zF = int(df['cenz_FLAIR'].iloc[0])

xS = int(df['cenx_SWAN'].iloc[0])
yS = int(df['ceny_SWAN'].iloc[0])
zS = int(df['cenz_SWAN'].iloc[0])

# Convertimos con fsleyes las imágenes NIFTI en T1, T2, SWAN y FLAIR a PNG aplicando la máscara de la lesión.
os.system(f'fsleyes render --scene ortho --xcentre  0.00000  0.00000 --ycentre  0.00000  0.00000 --zcentre  0.00000  0.00000 --xzoom 1100.0 --yzoom 1100.0 --zzoom 1100.0 --layout horizontal -hl --performance 3 --movieSync --hideCursor --outfile ./Img_lesion/ImagenT2.png --voxelLoc {xT2} {yT2} {zT2} ./Lesion_Segmentation_id023/id023/LesionSegment_New/T2_PO.nii.gz --name "T2_PO.nii.gz" --overlayType volume  --cmap greyscale --displayRange 1.0 1000.0 --cmapResolution 256 --interpolation linear ./Lesion_Segmentation_id023/id023/Rater_Merged/Lesion_T2_PO_1D_W.nii.gz --overlayType mask --maskColour 1.0 0.0 0.0 --outline --interpolation linear')
os.system(f'fsleyes render --scene ortho --xcentre  0.00000  0.00000 --ycentre  0.00000  0.00000 --zcentre  0.00000  0.00000 --xzoom 820.0 --yzoom 820.0 --zzoom 820.0 --layout horizontal -hl --performance 3 --movieSync --hideCursor --outfile ./Img_lesion/ImagenT1.png --voxelLoc {xT1} {yT1} {zT1} ./Lesion_Segmentation_id023/id023/LesionSegment_New/T1_PO.nii.gz --name "T1_PO.nii.gz" --overlayType volume  --cmap greyscale --displayRange 30.0 450.0 --cmapResolution 256 --interpolation linear ./Lesion_Segmentation_id023/id023/Rater_Merged/Lesion_T1_PO_1D_W.nii.gz --overlayType mask --maskColour 1.0 0.0 0.0 --outline --interpolation linear')
os.system(f'fsleyes render --scene ortho --xcentre  0.00000  0.00000 --ycentre  0.00000  0.00000 --zcentre  0.00000  0.00000 --xzoom 820.0 --yzoom 820.0 --zzoom 820.0 --layout horizontal -hl --performance 3 --movieSync --hideCursor --outfile ./Img_lesion/ImagenSWAN.png --voxelLoc {xS} {yS} {zS} ./Lesion_Segmentation_id023/id023/LesionSegment_New/SWI_PO.nii.gz --name "SWI_PO.nii.gz" --overlayType volume  --cmap greyscale --displayRange 2.0 2000.0 --cmapResolution 256 --interpolation linear ./Lesion_Segmentation_id023/id023/Rater_Merged/Lesion_SWI_PO_1D_W.nii.gz --overlayType mask --maskColour 1.0 0.0 0.0 --outline --interpolation linear')
os.system(f'fsleyes render --scene ortho --xcentre  0.00000  0.00000 --ycentre  0.00000  0.00000 --zcentre  0.00000  0.00000 --xzoom 820.0 --yzoom 820.0 --zzoom 820.0 --layout horizontal -hl --performance 3 --movieSync --hideCursor --outfile ./Img_lesion/ImagenFLAIR.png --voxelLoc {xF} {yF} {zF} ./Lesion_Segmentation_id023/id023/LesionSegment_New/FLAIR_PO.nii.gz --name "FLAIR_PO.nii.gz" --overlayType volume  --cmap greyscale --displayRange 20.0 190.0 --cmapResolution 256 --interpolation linear ./Lesion_Segmentation_id023/id023/Rater_Merged/Lesion_FLAIR_PO_1D_W.nii.gz --overlayType mask --maskColour 1.0 0.0 0.0 --outline --interpolation linear')

#Creamos una imagen en mosaico en T1, T2, FLAIR y SWAN.
os.system(f'fsleyes render --scene lightbox --zaxis 2 --sliceSpacing 6.219999999324791 --zrange 32.619983627262215 163.6599188131839 --ncols 4 --nrows 5 --bgColour 0.0 0.0 0.0 --fgColour 0.0 0.0 0.0 --movieSync --hideCursor --outfile ./Img_lesion/mosaicoT2.png ./Lesion_Segmentation_id023/id023/LesionSegment_New/T2_PO.nii.gz --name "T2_PO.nii.gz" --overlayType volume  --cmap greyscale --displayRange 1.0 1000.0 --cmapResolution 256 --interpolation linear ./Lesion_Segmentation_id023/id023/Rater_Merged/Lesion_T2_PO_1D_W.nii.gz --overlayType mask --maskColour 1.0 0.0 0.0 --outline --interpolation linear')
os.system(f'fsleyes render --scene lightbox --zaxis 2 --sliceSpacing 6.219999999324791 --zrange 32.619983627262215 163.6599188131839 --ncols 4 --nrows 5 --bgColour 0.0 0.0 0.0 --fgColour 0.0 0.0 0.0 --movieSync --hideCursor --outfile ./Img_lesion/mosaicoT1.png ./Lesion_Segmentation_id023/id023/LesionSegment_New/T1_PO.nii.gz --name "T1_PO.nii.gz" --overlayType volume  --cmap greyscale --displayRange 30.0 450.0 --cmapResolution 256 --interpolation linear ./Lesion_Segmentation_id023/id023/Rater_Merged/Lesion_T1_PO_1D_W.nii.gz --overlayType mask --maskColour 1.0 0.0 0.0 --outline --interpolation linear')
os.system(f'fsleyes render --scene lightbox --zaxis 2 --sliceSpacing 6.219999999324791 --zrange 32.619983627262215 163.6599188131839 --ncols 4 --nrows 5 --bgColour 0.0 0.0 0.0 --fgColour 0.0 0.0 0.0 --movieSync --hideCursor --outfile ./Img_lesion/mosaicoFLAIR.png ./Lesion_Segmentation_id023/id023/LesionSegment_New/FLAIR_PO.nii.gz --name "FLAIR_PO.nii.gz" --overlayType volume  --cmap greyscale --displayRange 20.0 190.0 --cmapResolution 256 --interpolation linear ./Lesion_Segmentation_id023/id023/Rater_Merged/Lesion_FLAIR_PO_1D_W.nii.gz --overlayType mask --maskColour 1.0 0.0 0.0 --outline --interpolation linear')
os.system(f'fsleyes render --scene lightbox --zaxis 2 --sliceSpacing 6.219999999324791 --zrange 32.619983627262215 163.6599188131839 --ncols 4 --nrows 5 --bgColour 0.0 0.0 0.0 --fgColour 0.0 0.0 0.0 --movieSync --hideCursor --outfile ./Img_lesion/mosaicoSWAN.png ./Lesion_Segmentation_id023/id023/LesionSegment_New/SWI_PO.nii.gz --name "SWI_PO.nii.gz" --overlayType volume  --cmap greyscale --displayRange 2.0 2000.0 --cmapResolution 256 --interpolation linear ./Lesion_Segmentation_id023/id023/Rater_Merged/Lesion_SWI_PO_1D_W.nii.gz --overlayType mask --maskColour 1.0 0.0 0.0 --outline --interpolation linear')