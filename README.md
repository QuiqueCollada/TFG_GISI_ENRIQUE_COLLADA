MANUAL DE EJECUCIÓN

IMPORTANTE: PARA PODER REALIZAR LOS SIGUIENTES PASOS DEBE TENER INSTALADO UN GESTOR DE CONTENEDORES DOCKER.

Si utiliza macOS o Linux

	1. Abra el Terminal y, en el directorio del proyecto, ejecute el comando "sh build.sh". Este script construirá la imagen docker y la ejecutará, extrayendo los ficheros report.pdf y report.html del entorno virtual a su máquina. Al final de su ejecución deberá introducir por teclado "y" o "n" si desea eliminar la caché de docker.

	2. Cumpruebe y abra el informe clínico que se encuentra en "output_files/report.pdf".

Si utiliza Windows

	En este caso, deberá abrir una terminal de línea de comandos PowerShell y seguir los pasos descritos a continuación:

	1. Asegúrese de que no hay procesos docker activos:

		docker ps -a -q

	1.1. En caso de haberlos, el anterior comando le devolverá los CONTAINER ID. Pare cada uno de ellos utilizando los siguientes comandos:

		docker stop <CONTAINER ID>
		docker rm <CONTAINER ID>

	2. Desde el directorio del proyecto, cree la imagen docker y ejecútela:

		docker build -t tfgecollada .
		docker run tfgecollada

	3. Consulte el ID de su contenedor:

		docker ps -a -q

	4. Copie el CONTAINER ID, introdúzcalo en el siguiente comando y ejecútelo:

		docker cp <CONTAINER ID>:/usr/src/app/report.pdf output_files

	5. Pare y elimine todos los procesos, imágenes y caché de docker:

		docker stop <CONTAINER ID>
		docker rm <CONTAINER ID>
		docker images -q -a
		docker rmi <IMAGE ID>
		docker builder prune

	6. Compruebe y abra el informe clínico que se encuentra en "output_files/report.pdf".


(INFORMACIÓN EXTRA AL ENTREGABLE EVALUABLE)

MANUAL AVANZADO PARA LA VISUALIZACIÓN Y EXTRACCIÓN DE CARACTERÍSTICAS DE FICHEROS NIFTI

Para ejecutar los siguientes scripts, deberá tener instalado Matlab y FSL en su ordenador, además de contar con los ficheros NIFTI de resonancia magnética de un paciente.

1. Procesar los ficheros nifti de la lesión con el ejecutable de matlab "main_topography.m"

2. Ejecutar "nifti_to_png.py" para producir las imágenes con el contorno de la lesión.

3. Ejecutar "main.py" para generar el informe clínico, que se llamará "report.pdf" y "report.html"

4. Abrir "report.pdf" o "report.html" para ver el resultado final.

