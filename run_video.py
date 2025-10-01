"""
Procesamiento de videos con estimación de poses
"""
import time
from pathlib import Path

import cv2
from mmpose.apis import init_model, inference_topdown
from mmpose.utils import register_all_modules
from mmpose.visualization import PoseLocalVisualizer

from config import (
    CONFIG, CHECKPOINT, DEVICE, OUTPUTS_DIR,
    KEYPOINT_THRESHOLD, DEFAULT_VIDEO_CODEC, VISUALIZER_CONFIG
)
from video_utils import (
    validate_video_path, get_video_properties,
    create_video_writer, print_progress
)


def run_video(video_path: str, output_name: str = None) -> bool:
    """Procesa un video aplicando estimación de poses"""
    print("Iniciando procesamiento de video...")
    print(f"Dispositivo: {DEVICE}")

    if not validate_video_path(video_path):
        return False

    video_props = get_video_properties(video_path)
    if not video_props:
        return False

    print(f"Video: {video_props['width']}x{video_props['height']}")
    print(f"FPS: {video_props['fps']}, Frames: {video_props['total_frames']}")
    print(f"Duración: {video_props['duration']} segundos")

    input_name = Path(video_path).stem
    output_filename = f"{output_name}.mp4" if output_name else f"processed_{input_name}.mp4"
    output_path = OUTPUTS_DIR / output_filename
    print(f"Archivo de salida: {output_path}")

    register_all_modules()
    try:
        print("Cargando modelo...")
        model = init_model(CONFIG, CHECKPOINT, device=DEVICE)
        print("Modelo cargado exitosamente")
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        return False

    visualizer = PoseLocalVisualizer(**VISUALIZER_CONFIG)
    visualizer.set_dataset_meta(model.dataset_meta)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: No se pudo abrir el video {video_path}")
        return False

    out = create_video_writer(
        str(output_path),
        video_props['fps'],
        video_props['width'],
        video_props['height'],
        DEFAULT_VIDEO_CODEC
    )

    frame_count = 0
    start_time = time.time()
    print("Iniciando procesamiento de frames...")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = inference_topdown(model, frame)
            if results:
                visualizer.set_image(frame)
                vis_img = visualizer.add_datasample(
                    'pose_result',
                    frame,
                    data_sample=results[0],
                    draw_gt=False,
                    draw_heatmap=False,
                    show=False,
                    kpt_thr=KEYPOINT_THRESHOLD
                )
                frame = vis_img[..., ::-1]

            out.write(frame)
            frame_count += 1
            print_progress(frame_count, video_props['total_frames'])

    except Exception as e:
        print(f"Error durante el procesamiento: {e}")
        return False

    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    end_time = time.time()
    processing_time = end_time - start_time
    fps_processed = frame_count / processing_time if processing_time > 0 else 0

    print(f"\nProcesamiento completado!")
    print(f"Frames procesados: {frame_count}")
    print(f"Tiempo total: {processing_time:.2f} segundos")
    print(f"Velocidad: {fps_processed:.2f} FPS")
    print(f"Video guardado en: {output_path}")

    return True


if __name__ == "__main__":
    video_path = input("Ingresa la ruta del video: ").strip().strip('"')
    run_video(video_path)
