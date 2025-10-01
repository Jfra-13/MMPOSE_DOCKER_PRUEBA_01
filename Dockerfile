# Imagen base con CUDA 12.1 y Ubuntu 20.04
FROM nvidia/cuda:12.1.0-runtime-ubuntu20.04

# Evitar prompts interactivos (ej. selección de zona horaria)
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Establecer directorio de trabajo
WORKDIR /workspace

# Instalar dependencias del sistema + Python 3.8 + pip
RUN apt-get update && apt-get install -y \
    tzdata \
    python3.8 python3.8-dev python3.8-distutils python3-pip \
    wget git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 libgl1-mesa-glx \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Asegurar que python3.8 sea el predeterminado
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

# Actualizar pip, setuptools y wheel
RUN python3 -m pip install --upgrade pip setuptools wheel

# Instalar openmim
RUN pip install openmim

# Instalar PyTorch + CUDA 12.1 (versión compatible)
RUN pip install torch==2.4.1+cu121 torchvision==0.19.1+cu121 torchaudio==2.4.1 \
    --index-url https://download.pytorch.org/whl/cu121

# Instalar mmengine y mmcv
RUN mim install mmengine
RUN mim install "mmcv>=2.0.0,<2.2.0"

# Instalar MMPose desde el repositorio oficial
RUN git clone https://github.com/open-mmlab/mmpose.git /mmpose
WORKDIR /mmpose
RUN pip install -r requirements.txt
RUN pip install -v -e .

# Crear carpeta para datos compartidos
RUN mkdir -p /workspace/data

# Comando por defecto al entrar al contenedor
CMD ["bash"]
