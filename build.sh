clear
echo "Construyendo el contenedor..."
docker build -t tfgecollada .
echo "Eliminando los procesos docker (si los hay)..."
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
echo "Iniciando el contenedor"
echo "Generando informe clínico..."
docker run tfgecollada
echo "Copiando report.pdf al directorio output_files"
docker cp $(docker ps -a -q):/usr/src/app/report.pdf output_files
echo "Proceso completado"
echo "Parando procesos docker..."
docker stop $(docker ps -a -q)
echo "Eliminando procesos docker..."
docker rm $(docker ps -a -q)
echo "Eliminando imágenes docker"
docker rmi $(docker images -q)
echo "Para eliminar la cache del docker, introduzca por teclado y/n"
docker builder prune
echo "Ya puede consultar su informe clínico"