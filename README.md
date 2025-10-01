MMPose – Dockerized Runtime (CUDA 12.1, PyTorch 2.4)

Este repositorio empaqueta un entorno reproducible para correr estimación de pose con MMPose dentro de Docker, aprovechando GPU NVIDIA (CUDA 12.1).
La imagen clona MMPose dentro del contenedor y lo instala, así que no necesitas instalarlo en tu host.

Probado en Windows 11 + Docker Desktop (WSL2) con GPU NVIDIA.

Contenidos

Requisitos

Estructura del proyecto

Construir la imagen Docker

Arrancar el contenedor y verificar

Ejecutar con vídeos pregrabados

Ejecutar en tiempo real (opcional)

Notas sobre Windows / terminales

Solución de problemas

FAQ

Requisitos

Windows 11 con Docker Desktop y backend WSL2.

GPU NVIDIA con drivers recientes (soporte CUDA).

Docker con acceso a GPU (en Docker Desktop, Settings → Resources → GPU debe estar habilitado).

Git para clonar este repositorio.

⚠️ No necesitas conda/miniconda en el host. Todo corre dentro del contenedor.

Estructura del proyecto
.
├─ Dockerfile
├─ README.md
├─ config.py                 # tu configuración de modelo/visualización
├─ main.py                   # script principal (batch)
├─ run_video.py              # demo para vídeos pregrabados
├─ run_realtime.py           # demo en tiempo real (cámara/rtsp)
├─ video_utils.py
├─ environment.yml           # (informativo) no se usa en Docker
├─ checkpoints/              # coloca aquí los .pth de modelos
├─ inputs/                   # tus vídeos de entrada .mp4 / .avi
└─ outputs/                  # resultados procesados


Importante: los checkpoints (.pth) no se suben a Git. Descárgalos y colócalos en checkpoints/ en tu máquina.

Construir la imagen Docker

Abre PowerShell en la carpeta raíz del repo (donde está el Dockerfile) y ejecuta:

docker build -t mmpose:cuda12.1 .


Notas:

La primera build descarga CUDA, PyTorch, MMPose, etc. Puede tardar y ocupar ~20 GB.

Siguientes builds serán más rápidas por caché.

El Dockerfile clona MMPose dentro de la imagen y lo instala (editable o importable), por lo que no necesitas clonar MMPose en tu host.

Arrancar el contenedor y verificar
Montar tu proyecto dentro del contenedor

Según la terminal que uses, el parámetro -v cambia:

PowerShell (recomendado):

docker run --gpus all --shm-size=8g -it -v ${PWD}:/workspace mmpose:cuda12.1


CMD clásico:

docker run --gpus all --shm-size=8g -it -v %cd%:/workspace mmpose:cuda12.1


Git Bash / MINGW64:

docker run --gpus all --shm-size=8g -it -v "$(pwd)":/workspace mmpose:cuda12.1


Tras entrar, tu repo quedará montado en /workspace.
MMPose está disponible en el contenedor. Si la imagen lo instaló en modo editable, podrás importar mmpose sin más. Si prefieres, puedes exportar PYTHONPATH=/mmpose.

Verificaciones rápidas (dentro del contenedor)
python3 -c "import torch; print(torch.__version__, torch.cuda.is_available())"
# salida esperada: 2.4.x True

python3 -c "import mmpose; print('MMPose OK')"
# salida esperada: MMPose OK

Ejecutar con vídeos pregrabados

Copia un video a inputs/, por ejemplo inputs/sample.mp4.

Dentro del contenedor:

cd /workspace
python3 run_video.py --input inputs/sample.mp4 --output outputs/sample_out.mp4


El resultado se guardará en outputs/.

Si tu script lee config.py o necesita un checkpoint concreto, asegúrate de tener el .pth en checkpoints/ y que la ruta en tu script/config apunte ahí.

Ejecutar en tiempo real (opcional)

La captura directa de cámara Windows → contenedor Linux puede ser compleja. Dos caminos:

A) (Recomendado) Simular webcam con un RTSP desde el host

(Host / Windows) Instala FFmpeg (si no lo tienes).
Confirmación:

ffmpeg -version
ffplay -version


(Host / Windows) Lista tu cámara:

ffmpeg -list_devices true -f dshow -i dummy


Ubica el nombre, por ejemplo: ROG EYE S.

(Host / Windows) Publica la cámara como RTSP con un servidor de streaming:

Arranca MediaMTX (servidor RTSP) en un terminal:

docker run --rm --name mediamtx -p 8554:8554 bluenviron/mediamtx:latest


Deja esta ventana abierta.

En otra ventana (Host), empuja tu cámara al servidor:

ffmpeg -f dshow -rtbufsize 256M -framerate 30 -video_size 1280x720 -i video="ROG EYE S" ^
  -vf "format=yuv420p" -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p -g 30 ^
  -f rtsp -rtsp_transport tcp rtsp://127.0.0.1:8554/cam


Si ves que duplica o pierde frames, baja a -video_size 640x480 o pon -framerate 25.

(Opcional) Validar vista desde el host:

ffplay rtsp://127.0.0.1:8554/cam


(Contenedor / Linux) Consume el RTSP:

cd /workspace
# Si tu script espera leer desde cv2.VideoCapture, pásale la URL:
python3 run_realtime.py --input rtsp://host.docker.internal:8554/cam


En Docker Desktop (Windows), usa host.docker.internal para que el contenedor alcance el servicio RTSP del host.

Si tu script no acepta --input, edita internamente la fuente a:
cv2.VideoCapture("rtsp://host.docker.internal:8554/cam").

B) Alternativa simple: usar un archivo como “cámara”

Mientras pruebas, puedes usar un video como si fuera cámara:

python3 run_realtime.py --input inputs/sample.mp4

Notas sobre Windows / terminales

No mezcles sintaxis de PowerShell con CMD.

PowerShell usa ${PWD}

CMD usa %cd%

Git Bash usa $(pwd)

Si ves: "%cd%" includes invalid characters… es porque ejecutaste un comando de CMD dentro de PowerShell. Usa la variante correcta para tu terminal.

Solución de problemas

ModuleNotFoundError: No module named 'mmdet'
Tu script/versión de MMPose puede requerir mmdet. Dentro del contenedor:

pip install mmdet


(Puedes integrarlo en el Dockerfile si tu flujo lo necesita siempre.)

cv2.VideoCapture(...) no abre la cámara

Desde contenedor usa RTSP con host.docker.internal (ver sección tiempo real).

Si usas RTSP y ves Connection refused: revisa que MediaMTX está corriendo y que FFmpeg está publicando (cam).

Muchos frame dropped en FFmpeg (Windows)

Reduce resolución: -video_size 640x480

Baja fps: -framerate 25 o -framerate 15

Asegúrate de cerrar apps que usen simultáneamente la webcam.

GPU no detectada (False en torch.cuda.is_available())

En Docker Desktop habilita GPU.

Lanza contenedor con --gpus all.

Actualiza drivers NVIDIA en Windows.

Rutas de checkpoints/config

Coloca .pth en checkpoints/ y asegúrate de que config.py o tus scripts apunten correctamente.

FAQ

¿Necesito conda/miniconda?
No. Docker ya incluye Python y todas las dependencias. El environment.yml queda solo como referencia.

¿Dónde pongo los checkpoints (.pth)?
En checkpoints/ (del host). Se montan dentro del contenedor en /workspace/checkpoints.

¿Puedo usar mi propia cámara sin RTSP?
Directamente no, porque Windows → contenedor Linux complica el acceso al dispositivo. La vía robusta es RTSP (A) o probar con archivos (B).

¿Puedo fijar una versión específica de MMPose?
Sí. En el Dockerfile puedes clonar un tag/commit estable (por ejemplo usando --branch <tag>). Este repo ya trae una configuración que funcionó con:

Python 3.8

CUDA 12.1

torch 2.4.1+cu121

mmcv 2.1.0

mmengine 0.10.7

mmdet 3.3.0 (si tu script lo requiere)

Comandos “de bolsillo”

Build:

docker build -t mmpose:cuda12.1 .


Run (PowerShell):

docker run --gpus all --shm-size=8g -it -v ${PWD}:/workspace mmpose:cuda12.1


Verificar GPU dentro del contenedor:

python3 -c "import torch; print(torch.__version__, torch.cuda.is_available())"


Demo con video:

cd /workspace
python3 run_video.py --input inputs/sample.mp4 --output outputs/sample_out.mp4


Demo tiempo real (RTSP desde host):

python3 run_realtime.py --input rtsp://host.docker.internal:8554/cam
