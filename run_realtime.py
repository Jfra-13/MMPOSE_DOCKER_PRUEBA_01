import cv2
import torch
from mmpose.apis import init_model, inference_topdown
from mmpose.utils import register_all_modules
from mmpose.visualization import PoseLocalVisualizer

from config import CONFIG, CHECKPOINT, DEVICE, OUTPUTS_DIR, VISUALIZER_CONFIG


def run_realtime():
    """Función para ejecutar pose estimation en tiempo real"""
    register_all_modules()

    model = init_model(CONFIG, CHECKPOINT, device=DEVICE)
    visualizer = PoseLocalVisualizer(**VISUALIZER_CONFIG)
    visualizer.set_dataset_meta(model.dataset_meta)

    cap = cv2.VideoCapture("udp://127.0.0.1:8554")
    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return

    print("Cámara en vivo. Presiona 'q' para salir.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = inference_topdown(model, frame)

            if results:
                visualizer.set_image(frame)
                vis_img = visualizer.add_datasample(
                    'result',
                    frame,
                    data_sample=results[0],
                    draw_gt=False,
                    draw_heatmap=False,
                    show=False
                )
                frame = vis_img[..., ::-1]

            cv2.imshow("Pose Estimation (Real Time)", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario")
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    run_realtime()
