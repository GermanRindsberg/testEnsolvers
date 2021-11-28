# testEnsolvers
Repositorio que contiene un test realizado para la empresa Ensolvers. El mismo contiene una webapp de tipo SPA, desarrollada en Angular para la parte del frontEnd y Flask(python) como backEnd

1- Clonar repositorio.

2 -Ejecutar runApp.sh


Si tiene problemas con el puerto 4200 de angular ejecutar lo siguiente:

Windows: 
1- Ejecutar cmd
2- Ejecutar el siguiente comando: "netstat -a -n -o"
3- Buscar el PID que este usando el puerto 4200.
4- Ejecutar el siguiente comando: "taskkill -f /pid 'el numero de pid donde se ejecuta el puerto 4200' "

Linux:
1-sudo kill $(sudo lsof -t -i:4200) 
O
2-sudo kill `sudo lsof -t -i:4200` 
O
3-sudo lsof -t -i tcp:4200 | xargs kill -9



