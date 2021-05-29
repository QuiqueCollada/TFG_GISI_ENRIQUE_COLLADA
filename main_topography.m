%--------------------------------------------------------------------------
close all; clear; clc;
%--------------------------------------------------------------------------
src_path = '.';
deps = fullfile(src_path,'dependencies');
addpath(deps);

templatedir = fullfile(deps,'Templates');
fileRefICBM = fullfile(templatedir,'ICBM_T1_2009_brain.nii.gz');

src_path_data = './Lesion_Segmentation_id023';
src_path_data_ants = fullfile(src_path_data,'OnlyANTS');
dst_path = fullfile(src_path_data,'Topography_Report');
if ~exist(dst_path,'dir'); mkdir(dst_path); end
subjs_all = dir([src_path_data ,'/i*']);

% Coordenadas Espaciales Estándard de referencia
ICBM_AC = [97,134,74]; % Coordenadas de la Comisura Anterior ICBM
ICBM_PC = [97,109,77]; % Coordenadas de la Comisura Posterior ICBM
ICBM_ML = [97,118,138]; % MidSagLine ICBM
ACPC_icbm = pdist([ICBM_AC;ICBM_PC]);

% Crear un fichero csv de salida sobre los sujetos
outfilereport = fullfile(dst_path,'outstats_single_subject.txt');
fid = fopen(outfilereport,'w');
fprintf(fid,sprintf('id,natvol,diamx,diamy,diamz,latICL,dPC,dPCPerc,dInfACPC,VIMoccupied,LesioninVIM,cenx_T2,ceny_T2,cenz_T2,cenx_T1,ceny_T1,cenz_T1,cenx_SWAN,ceny_SWAN,cenz_SWAN,cenx_FLAIR,ceny_FLAIR,cenz_FLAIR\n'));
    

for i_s = 1:length(subjs_all)
    
    % Coge el nombre del sujeto y define el path
    subj = subjs_all(i_s).name;
    subjfolder = fullfile(src_path_data,subj);
    mrifolder = fullfile(subjfolder,'LesionSegment_New');
    segmentfolder = fullfile(subjfolder,'Rater_Merged');
    antsfolder = fullfile(src_path_data_ants,subj,'ants_Reg'); % Carpera para almacenar las imágenes T1 normalizadas al Espacio Estándar ICBM2009c
    if ~exist(antsfolder,'dir')
        ants2bedone = 1;
        mkdir(fullfile(src_path_data_ants,subj));
        mkdir(antsfolder);
    else
        ants2bedone = 0;
    end
    
    % Lee la lesión
    fileIn = 'Lesion_T2_PO_1D_W.nii.gz';
    fileInPath = fullfile(segmentfolder,fileIn);
    if ~exist(fileInPath,'file')
        fileInPath = fullfile(subjfolder,'Rater_01',fileIn);
    end
    hdr = load_nifti(fileInPath); % Carga la lesión
    MDATA.natvol = sum(hdr.vol(:) > 0) * prod(hdr.pixdim(2:4)); % Obtiene el volumen
    
    % Coge medidas T2
    msnts2 = regionprops(hdr.vol,'Centroid'); 
    MDATA.T2_Centroid = [msnts2.Centroid(2),msnts2.Centroid(1),msnts2.Centroid(3)]; % Invert second and first dimensions
    
    % Coge medidas T1
    fileInT1 = 'Lesion_T1_PO_1D_W.nii.gz';
    fileInPathT1 = fullfile(segmentfolder,fileInT1);
    if ~exist(fileInPathT1,'file')
        fileInPathT1 = fullfile(subjfolder,'Rater_01',fileInT1);
    end
    hdr1 = load_nifti(fileInPathT1);
    MDATA.natvol1 = sum(hdr1.vol(:) > 0) * prod(hdr1.pixdim(2:4));
    msnts1 = regionprops(hdr1.vol,'Centroid'); 
    MDATA.T1_Centroid = [msnts1.Centroid(2),msnts1.Centroid(1),msnts1.Centroid(3)]; % Invert second and first dimensions
    
     % Coge medidas SWAN
    fileInSWI = 'Lesion_SWI_PO_1D_W.nii.gz';
    fileInPathSWI = fullfile(segmentfolder,fileInSWI);
    if ~exist(fileInPathSWI,'file')
        fileInPathSWI = fullfile(subjfolder,'Rater_01',fileInSWI);
    end
    hdr2 = load_nifti(fileInPathSWI);
    MDATA.natvolSWI = sum(hdr2.vol(:) > 0) * prod(hdr2.pixdim(2:4));
    msnts2 = regionprops(hdr2.vol,'Centroid'); 
    MDATA.SWI_Centroid = [msnts2.Centroid(2),msnts2.Centroid(1),msnts2.Centroid(3)]; % Invert second and first dimensions
    
    % Coge medidas FLAIR
    fileInF = 'Lesion_FLAIR_PO_1D_W.nii.gz';
    fileInPathF = fullfile(segmentfolder,fileInF);
    if ~exist(fileInPathF,'file')
        fileInPathF = fullfile(subjfolder,'Rater_01',fileInF);
    end
    hdr3 = load_nifti(fileInPathF);
    MDATA.natvolF = sum(hdr3.vol(:) > 0) * prod(hdr3.pixdim(2:4));
    msnts3 = regionprops(hdr3.vol,'Centroid'); 
    MDATA.FLAIR_Centroid = [msnts3.Centroid(2),msnts3.Centroid(1),msnts3.Centroid(3)]; % Invert second and first dimensions
    
    
    % Normalización ICBM (si no existe)
    if ants2bedone
        fileIn = fullfile(mrifolder,'T1_BL_brain.nii.gz');
        fprintf('ANTs Normalization (affine+syn) to standar space\n');
        fprintf('Using ICBM 2009 Brain Template\n')
        fileTrx = fullfile(antsfolder,'transforms_');
        sentence = sprintf ('ANTS 3 -m CC[%s,%s,1,2] -t SyN[0.25] -i 50x50x30 -o %s',fileRefICBM,fileIn,fileTrx);
        [st,res] = system(sentence);
        if st; error(res); end
        
        fileOut = fullfile(antsfolder,'T12MNI.nii.gz');
        Antstransform = sprintf('-R %s %s %s',fileRefICBM,fullfile(antsfolder,'transforms_Warp.nii.gz'),fullfile(antsfolder,'transforms_Affine.txt'));
        sentence = sprintf('WarpImageMultiTransform 3 %s %s %s',fileIn,fileOut,Antstransform);
        [st,res] = system(sentence);
        if st; error(res); end
    end
    
    % Establecemos los ficheros de salida de las transformaciones
    filePathAnts_warp = fullfile(antsfolder,'transforms_Warp.nii.gz');
    filePathAnts_affine = fullfile(antsfolder,'transforms_Affine.mat');
    if ~exist(filePathAnts_affine,'file')
        filePathAnts_affine = fullfile(antsfolder,'transforms_Affine.txt');
    end
    filePathAnts_affinerigid_T22T1BL = fullfile(mrifolder,'T2_PO_toBLAffine.txt');
    
    % Transformamos la lesión al espacio ICBM usando interpolación por vecinos cercanos
    fileOut = fullfile(dst_path,[subj '_Lesion_T2_1D_W_inICBM.nii.gz']);
    if ~exist(fileOut,'file')
        Antstransform = sprintf('-R %s %s %s %s --use-NN',fileRefICBM,filePathAnts_warp,filePathAnts_affine,filePathAnts_affinerigid_T22T1BL);
        sentence = sprintf('/Users/enrique/ANTs_Main/install/bin/WarpImageMultiTransform 3 %s %s %s',fileInPath,fileOut,Antstransform);
        [status,res] = system(sentence);
        if status; error(res); end
    end
    lesion_in_ICBM = fileOut;
    
    % ------------------------------------------------------------------------
    % Extraemos volumen, diametros y centroides
    fprintf('Extracting Volume Diameters and Centroids from lesion masks\n');
    hdr_icbm = load_nifti(fileRefICBM); vol_icbm = hdr_icbm.vol;
    vol_icbm = vol_icbm.*0;
    
    % Coordenadas ROIs
    hdr_lesion_icbm = load_nifti(lesion_in_ICBM);
    hdr_vim = load_nifti(fullfile(templatedir,'LVLpv_icbm.nii.gz')); roi_vim = hdr_vim.vol;
    
    % Volumen en el espacio MNI con voxels representando tejido de la lesión
    vol_icbm(hdr_lesion_icbm.vol > 0) = 1;
    
    % Diámentros/Centroide en el espacio ACPC
    msnts = regionprops(vol_icbm,'BoundingBox');
    MDATA.Diameters_icbm = msnts.BoundingBox(4:end);
    
    % Centoride en el espacio ICBM
    msnts = regionprops(vol_icbm,'Centroid');
    MDATA.ICBM_Centroid = [msnts.Centroid(2),msnts.Centroid(1),msnts.Centroid(3)]; % Invierte la segunda y la primera dimensiones
    MDATA.ICBM_Centroid_ras(1,1:4) = [-1 1 1 1]' .* ([-1 -1 -1 0]' + hdr_lesion_icbm.vox2ras * [MDATA.ICBM_Centroid 1]');
    MDATA.ICBM_Centroid_ras = MDATA.ICBM_Centroid_ras(1:3);
    
    AC_ras  = [-1 1 1 1]' .* ([-1 -1 -1 0]' + hdr_lesion_icbm.vox2ras * [ICBM_AC 1]');
    PC_ras  = [-1 1 1 1]' .* ([-1 -1 -1 0]' + hdr_lesion_icbm.vox2ras * [ICBM_PC 1]');
    
    MDATA.ICBM_dPC = MDATA.ICBM_Centroid_ras(2) - PC_ras(2);
    MDATA.ICBM_dPC_perc = (MDATA.ICBM_Centroid_ras(2) - PC_ras(2)) ./ sqrt(sum((ICBM_AC - ICBM_PC).^2));
    MDATA.ICBM_dInfACPC = MDATA.ICBM_Centroid_ras(3);
    MDATA.ICBM_dICL = MDATA.ICBM_Centroid_ras(1);
        
    % Porcentaje del VIM ocupado
    MDATA.ICBM_VIMOccupied = sum(vol_icbm(:).*roi_vim(:))./sum(roi_vim(:));
    % Porcentaje de la lesión dentro del VIM
    MDATA.ICBM_LesInVIM = sum(vol_icbm(:).*roi_vim(:))./sum(vol_icbm(:));
    
    str = sprintf('%s,%0.4f,%d,%d,%d',subjs_all(i_s).name(end-2:end),MDATA.natvol,MDATA.Diameters_icbm);
    str = sprintf('%s,%0.4f,%0.4f,%0.4f,%0.4f',str,MDATA.ICBM_dICL,MDATA.ICBM_dPC,100*MDATA.ICBM_dPC_perc,MDATA.ICBM_dInfACPC);
    str = sprintf('%s,%0.4f,%0.4f',str,100*MDATA.ICBM_VIMOccupied,100*MDATA.ICBM_LesInVIM);
    str = sprintf('%s,%0.4f,%0.4f,%0.4f',str,MDATA.T2_Centroid);
    str = sprintf('%s,%0.4f,%0.4f,%0.4f',str,MDATA.T1_Centroid);
    str = sprintf('%s,%0.4f,%0.4f,%0.4f',str,MDATA.SWI_Centroid);
    str = sprintf('%s,%0.4f,%0.4f,%0.4f\n',str,MDATA.FLAIR_Centroid);
    fprintf(fid,str);
    clear MDATA;
end
fclose(fid);
    
