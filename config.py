"""
Configuraciones centralizadas para el proyecto de Pose Estimation
"""
from pathlib import Path
import torch

# Carpeta base del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Configuración del modelo
CONFIG_PATH = BASE_DIR / "mmpose" / "configs" / "wholebody_2d_keypoint" / "topdown_heatmap" / "coco-wholebody" / "td-hm_hrnet-w48_dark-8xb32-210e_coco-wholebody-384x288.py"
CHECKPOINT_PATH = "checkpoints/hrnet_w48_coco_wholebody_384x288-6e061c6a_20200922.pth"

# Convertir a string para MMPose
CONFIG = str(CONFIG_PATH)
CHECKPOINT = str(CHECKPOINT_PATH)

# Configuraciones de dispositivo
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# Configuraciones de video
DEFAULT_VIDEO_CODEC = 'mp4v'
KEYPOINT_THRESHOLD = 0.3

# Carpetas del proyecto
INPUTS_DIR = BASE_DIR / "inputs"
OUTPUTS_DIR = BASE_DIR / "outputs" 
CHECKPOINTS_DIR = BASE_DIR / "checkpoints"

# Crear carpetas si no existen
INPUTS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)
CHECKPOINTS_DIR.mkdir(exist_ok=True)

# Configuración del visualizador
VISUALIZER_CONFIG = {
    'radius': 4,
    'line_width': 2,
    'kpt_color': 'red',
    'link_color': 'blue',
    'vis_backends': None,
    'save_dir': str(OUTPUTS_DIR)
}