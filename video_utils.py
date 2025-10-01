import os
import cv2
import time
from pathlib import Path


def validate_video_path(video_path: str) -> bool:
    """Valida si el archivo de video existe y es legible."""
    if not os.path.exists(video_path):
        print(f"Error: El archivo {video_path} no existe.")
        return False
    if not os.path.isfile(video_path):
        print(f"Error: {video_path} no es un archivo válido.")
        return False
    return True


def get_video_properties(video_path: str) -> dict:
    """Obtiene propiedades básicas del video (fps, resolución, frames totales)."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: No se pudo abrir el video {video_path}")
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0

    cap.release()

    return {
        "fps": fps,
        "width": width,
        "height": height,
        "total_frames": total_frames,
        "duration": duration
    }


def create_video_writer(output_path: str, fps: float, width: int, height: int, codec: str = 'mp4v'):
    """Crea un writer de OpenCV para guardar el video procesado."""
    fourcc = cv2.VideoWriter_fourcc(*codec)
    return cv2.VideoWriter(output_path, fourcc, fps, (width, height))


def print_progress(current: int, total: int):
    """Imprime progreso del procesamiento en porcentaje."""
    percent = (current / total) * 100 if total > 0 else 0
    print(f"\rProcesando frames: {current}/{total} ({percent:.2f}%)", end="")
