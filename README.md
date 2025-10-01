# MMPose – Dockerized Runtime

![CUDA](https://img.shields.io/badge/CUDA-12.1-76B900?logo=nvidia)
![PyTorch](https://img.shields.io/badge/PyTorch-2.4-EE4C2C?logo=pytorch)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)

Entorno reproducible y listo para usar que ejecuta **estimación de pose con MMPose** dentro de Docker, aprovechando GPU NVIDIA con CUDA 12.1.

> ✨ **Todo incluido**: MMPose se clona e instala automáticamente dentro del contenedor. No necesitas instalaciones locales.

**Probado en**: Windows 11 + Docker Desktop (WSL2) con GPU NVIDIA

---

## 📋 Tabla de Contenidos

- [Preparación del Entorno (GPU + Docker)](#-preparación-del-entorno-gpu--docker)
  - [1. Verificar tu GPU](#1️⃣-verificar-tu-gpu)
  - [2. Instalar Drivers NVIDIA y CUDA](#2️⃣-instalar-drivers-nvidia-y-cuda)
  - [3. Instalar Docker con Soporte GPU](#3️⃣-instalar-docker-con-soporte-gpu)
  - [4. Verificar que Docker Detecta la GPU](#4️⃣-verificar-que-docker-detecta-la-gpu)
  - [5. Flujo Recomendado](#5️⃣-flujo-recomendado-antes-de-correr-el-proyecto)
- [Requisitos del Proyecto](#-requisitos-del-proyecto)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Guía Rápida de Inicio](#-guía-rápida-de-inicio)
  - [1. Construir la Imagen](#1-construir-la-imagen)
  - [2. Iniciar el Contenedor](#2-iniciar-el-contenedor)
  - [3. Verificar Instalación](#3-verificar-instalación)
- [Uso: Procesamiento de Videos](#-uso-procesamiento-de-videos)
- [Uso: Tiempo Real (Cámara)](#-uso-tiempo-real-cámara)
- [Solución de Problemas](#-solución-de-problemas)
- [Preguntas Frecuentes](#-preguntas-frecuentes)

---

## 🚀 Preparación del Entorno (GPU + Docker)

Este proyecto requiere **aceleración por GPU** para un rendimiento óptimo en la estimación de poses.  
A continuación se detallan los pasos previos necesarios antes de clonar y ejecutar el repositorio.

---

### 1️⃣ Verificar tu GPU

Abre **PowerShell** o **CMD** en Windows y ejecuta:

```bash
nvidia-smi
```

Si tu tarjeta gráfica es detectada, verás algo similar a esto:

```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.146   Driver Version: 535.146   CUDA Version: 12.2          |
| GPU Name        Persistence-M| Bus-Id ... Memory-Usage ...                 |
+-----------------------------------------------------------------------------+
```

✅ Esto confirma que tienes drivers NVIDIA funcionando.

---

### 2️⃣ Instalar Drivers NVIDIA y CUDA

1. **Descarga los drivers oficiales NVIDIA**:  
   👉 https://www.nvidia.com/Download/index.aspx

2. **Descarga e instala CUDA Toolkit** (elige la versión que coincida con tu GPU y drivers):  
   👉 https://developer.nvidia.com/cuda-downloads

3. Durante la instalación marca **"Include Driver"** si no lo tienes actualizado.

4. **Verifica CUDA** con:
   ```bash
   nvcc --version
   ```

---

### 3️⃣ Instalar Docker con Soporte GPU

1. **Descarga e instala Docker Desktop**:  
   👉 https://www.docker.com/products/docker-desktop/

2. Activa la opción **"Use WSL 2 based engine"** en configuración de Docker.

3. **Instala el NVIDIA Container Toolkit** (permite que Docker acceda a la GPU):

   Abre **PowerShell (Admin)** y ejecuta:
   ```powershell
   wsl --update
   wsl --install
   ```

   Luego, dentro de WSL, instala el toolkit:
   ```bash
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
   sudo apt-get update
   sudo apt-get install -y nvidia-container-toolkit
   sudo systemctl restart docker
   ```

---

### 4️⃣ Verificar que Docker Detecta la GPU

Ejecuta en PowerShell o CMD:

```bash
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
```

👉 Si todo está bien, deberías ver la misma salida que con `nvidia-smi`.

---

### 5️⃣ Flujo Recomendado Antes de Correr el Proyecto

Antes de continuar con la instalación del proyecto, asegúrate de:

- ✅ Verificar tu **GPU** con `nvidia-smi`
- ✅ Instalar/actualizar **drivers NVIDIA y CUDA**
- ✅ Instalar **Docker Desktop** con **WSL2**
- ✅ Configurar el **NVIDIA Container Toolkit**
- ✅ Probar `docker run --rm --gpus all ...` para confirmar que Docker ve la GPU

⚡ **Una vez completados estos pasos, ya puedes continuar con:**

1. Clonar **MMPose**
2. Clonar **este repositorio dentro de la carpeta de MMPose**
3. Construir y levantar el contenedor Docker
4. Ejecutar scripts (`run_video.py`, `run_realtime.py`, etc.)

---

## 🔧 Requisitos del Proyecto

Una vez completada la preparación del entorno, verifica que tengas:

- ✅ **Windows 11** con Docker Desktop configurado con backend WSL2
- ✅ **GPU NVIDIA** con drivers actualizados (soporte CUDA)
- ✅ **Acceso a GPU en Docker**: Ve a Docker Desktop → `Settings` → `Resources` → `GPU` y actívalo
- ✅ **Git** para clonar este repositorio

> ⚠️ **Nota importante**: No necesitas instalar conda, miniconda ni Python localmente. Todo se ejecuta dentro del contenedor.

---

## 📁 Estructura del Proyecto

```
.
├── Dockerfile              # Configuración de la imagen Docker
├── README.md              
├── config.py               # Configuración de modelos y visualización
├── main.py                 # Script principal de procesamiento por lotes
├── run_video.py            # Demo para videos pregrabados
├── run_realtime.py         # Demo para cámara en tiempo real
├── video_utils.py          # Utilidades auxiliares
├── environment.yml         # (Referencia) Dependencias conda
├── checkpoints/            # 📦 Coloca aquí tus archivos .pth
├── inputs/                 # 🎥 Tus videos de entrada (.mp4, .avi)
└── outputs/                # 📤 Resultados procesados
```

> 💡 **Importante**: Los archivos `.pth` de checkpoints no se incluyen en el repositorio. Debes descargarlos manualmente y colocarlos en la carpeta `checkpoints/`.

---

## 🚀 Guía Rápida de Inicio

### 1. Construir la Imagen

Abre **PowerShell** en la carpeta raíz del repositorio y ejecuta:

```powershell
docker build -t mmpose:cuda12.1 .
```

**Notas importantes:**
- ⏱️ La primera construcción puede tardar varios minutos y ocupar ~20 GB
- 🔄 Las siguientes construcciones serán mucho más rápidas gracias al caché
- 📦 El Dockerfile clona e instala MMPose automáticamente

---

### 2. Iniciar el Contenedor

Según tu terminal, usa el comando apropiado:

**PowerShell** (Recomendado):
```powershell
docker run --gpus all --shm-size=8g -it -v ${PWD}:/workspace mmpose:cuda12.1
```

**CMD**:
```cmd
docker run --gpus all --shm-size=8g -it -v %cd%:/workspace mmpose:cuda12.1
```

**Git Bash / MINGW64**:
```bash
docker run --gpus all --shm-size=8g -it -v "$(pwd)":/workspace mmpose:cuda12.1
```

Tu proyecto quedará montado en `/workspace` dentro del contenedor.

---

### 3. Verificar Instalación

Una vez dentro del contenedor, ejecuta estas verificaciones:

**Verificar GPU y PyTorch:**
```bash
python3 -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```
✅ Salida esperada: `2.4.x True`

**Verificar MMPose:**
```bash
python3 -c "import mmpose; print('MMPose OK')"
```
✅ Salida esperada: `MMPose OK`

---

## 🎥 Uso: Procesamiento de Videos

### Paso 1: Preparar el Video

Copia tu video a la carpeta `inputs/`:
```
inputs/sample.mp4
```

### Paso 2: Procesar

Dentro del contenedor, ejecuta:

```bash
cd /workspace
python3 run_video.py --input inputs/sample.mp4 --output outputs/sample_out.mp4
```

### Paso 3: Obtener Resultados

El video procesado estará disponible en `outputs/sample_out.mp4`

> 💡 **Tip**: Asegúrate de que tu archivo `config.py` apunte correctamente al checkpoint en `checkpoints/`

---

## 📹 Uso: Tiempo Real (Cámara)

La captura directa de cámara Windows → contenedor Linux puede ser compleja. Te presentamos dos métodos:

### Método A: RTSP (Recomendado)

Este método usa un servidor RTSP para transmitir tu cámara al contenedor.

#### **En el Host (Windows)**

**1. Verificar FFmpeg:**
```powershell
ffmpeg -version
ffplay -version
```

**2. Listar cámaras disponibles:**
```powershell
ffmpeg -list_devices true -f dshow -i dummy
```
Anota el nombre de tu cámara, por ejemplo: `ROG EYE S`

**3. Iniciar servidor RTSP:**

Abre una terminal y ejecuta:
```powershell
docker run --rm --name mediamtx -p 8554:8554 bluenviron/mediamtx:latest
```
⚠️ Deja esta terminal abierta

**4. Transmitir cámara al servidor:**

En otra terminal, ejecuta:
```powershell
ffmpeg -f dshow -rtbufsize 256M -framerate 30 -video_size 1280x720 -i video="ROG EYE S" ^
  -vf "format=yuv420p" -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p -g 30 ^
  -f rtsp -rtsp_transport tcp rtsp://127.0.0.1:8554/cam
```

**5. (Opcional) Verificar transmisión:**
```powershell
ffplay rtsp://127.0.0.1:8554/cam
```

#### **En el Contenedor (Linux)**

```bash
cd /workspace
python3 run_realtime.py --input rtsp://host.docker.internal:8554/cam
```

> 🔑 **Clave**: Usa `host.docker.internal` para que el contenedor acceda a servicios del host

---

### Método B: Usar Video como Simulación

Para pruebas rápidas, usa un archivo de video:

```bash
python3 run_realtime.py --input inputs/sample.mp4
```

---

## 🔍 Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'mmdet'`

Algunas versiones de MMPose requieren mmdet. Instálalo dentro del contenedor:

```bash
pip install mmdet
```

---

### La cámara no se abre con `cv2.VideoCapture()`

- ✅ Usa el método RTSP con `host.docker.internal`
- ✅ Verifica que MediaMTX esté corriendo
- ✅ Confirma que FFmpeg está transmitiendo correctamente

---

### Frames perdidos en FFmpeg

Si ves muchos `frame dropped`:

- 📉 Reduce resolución: `-video_size 640x480`
- 🐌 Baja fps: `-framerate 25` o `-framerate 15`
- ❌ Cierra otras aplicaciones que usen la webcam

---

### GPU no detectada (`False` en `torch.cuda.is_available()`)

1. Activa GPU en Docker Desktop: `Settings` → `Resources` → `GPU`
2. Verifica que uses `--gpus all` al iniciar el contenedor
3. Actualiza los drivers NVIDIA en Windows
4. Revisa la sección [Preparación del Entorno](#-preparación-del-entorno-gpu--docker) para validar la instalación completa

---

### Problemas con rutas de checkpoints

- Coloca los archivos `.pth` en `checkpoints/` del host
- Verifica que `config.py` apunte correctamente a estas rutas
- Las rutas dentro del contenedor serán: `/workspace/checkpoints/`

---

## ❓ Preguntas Frecuentes

<details>
<summary><strong>¿Necesito instalar conda o miniconda?</strong></summary>

No. Docker incluye Python y todas las dependencias necesarias. El archivo `environment.yml` es solo referencia.
</details>

<details>
<summary><strong>¿Dónde coloco los archivos de checkpoints (.pth)?</strong></summary>

En la carpeta `checkpoints/` de tu host. Se montarán automáticamente en `/workspace/checkpoints` dentro del contenedor.
</details>

<details>
<summary><strong>¿Puedo usar mi cámara sin RTSP?</strong></summary>

El acceso directo Windows → contenedor Linux es complicado. RTSP es el método más robusto. Alternativamente, usa archivos de video para pruebas.
</details>

<details>
<summary><strong>¿Puedo usar una versión específica de MMPose?</strong></summary>

Sí. En el `Dockerfile`, modifica el comando `git clone` para usar un tag o commit específico:

```dockerfile
RUN git clone --branch <tag-version> https://github.com/open-mmlab/mmpose.git
```

**Versiones probadas:**
- Python 3.8
- CUDA 12.1
- PyTorch 2.4.1+cu121
- mmcv 2.1.0
- mmengine 0.10.7
- mmdet 3.3.0
</details>

---

## 📝 Comandos de Referencia Rápida

**Construir imagen:**
```bash
docker build -t mmpose:cuda12.1 .
```

**Iniciar contenedor (PowerShell):**
```bash
docker run --gpus all --shm-size=8g -it -v ${PWD}:/workspace mmpose:cuda12.1
```

**Verificar GPU:**
```bash
python3 -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

**Procesar video:**
```bash
cd /workspace
python3 run_video.py --input inputs/sample.mp4 --output outputs/sample_out.mp4
```

**Tiempo real (RTSP):**
```bash
python3 run_realtime.py --input rtsp://host.docker.internal:8554/cam
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias y mejoras.

---

<div align="center">

⭐ Si este proyecto te fue útil, considera darle una estrella

</div>
