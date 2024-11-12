# Trabajo práctico #2

### Para correr este programa:

- Clonar el repositorio
- Instalar las dependencias con `pip install -r requirements.txt`
- Correr el servidor sincronico con `python -m server_sync.server`
- Correr servidor asincrono con `python main.py -i 127.0.0.1 -p 8080`
- Enviar una imagen al servidor con `curl -X POST -F "image=@/ruta/a/la/imagen.jpeg" http://127.0.0.1:8080/process`
- Para conocer el estado de la solicitud: `curl http://127.0.0.1:8080/status/\{task_id\}`

curl -X POST -F "image=@/home/dino/PycharmProjects/compu2/tp2/fallout.jpeg" http://127.0.0.1:8080/process --output processed_image.jpg

