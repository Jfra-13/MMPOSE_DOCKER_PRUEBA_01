import argparse
import sys

from config import INPUTS_DIR, OUTPUTS_DIR
from run_realtime import run_realtime
from run_video import run_video


def print_banner():
    banner = """
    ╔═══════════════════════════════════════╗
    ║        POSE ESTIMATION SYSTEM         ║
    ║            Powered by MMPose          ║
    ╚═══════════════════════════════════════╝
    """
    print(banner)


def list_available_videos():
    """Lista videos disponibles en la carpeta inputs"""
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    videos = []

    for ext in video_extensions:
        videos.extend(INPUTS_DIR.glob(f'*{ext}'))
        videos.extend(INPUTS_DIR.glob(f'*{ext.upper()}'))

    if videos:
        print(f"\nVideos disponibles en {INPUTS_DIR}:")
        for i, video in enumerate(videos, 1):
            print(f"  {i}. {video.name}")
    else:
        print(f"\nNo se encontraron videos en {INPUTS_DIR}")
        print("Coloca tus videos en la carpeta 'inputs' o especifica una ruta completa")


def main():
    """Función principal"""
    print_banner()

    parser = argparse.ArgumentParser(
        description="Sistema de Pose Estimation con MMPose",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Ejemplos de uso:
  python main.py --mode realtime
  python main.py --mode video --video_path inputs/mi_video.mp4 --output_name resultado
        """
    )

    parser.add_argument(
        "--mode",
        choices=["realtime", "video"],
        required=True,
        help="Modo de operación: 'realtime' para cámara web, 'video' para procesar archivo"
    )
    parser.add_argument("--video_path", type=str, help="Ruta al archivo de video (requerido en modo video)")
    parser.add_argument("--output_name", type=str, help="Nombre personalizado para el archivo de salida (sin extensión)")
    parser.add_argument("--list_videos", action="store_true", help="Listar videos disponibles en la carpeta inputs")

    args = parser.parse_args()

    if args.list_videos:
        list_available_videos()
        return

    if args.mode == "realtime":
        print("Iniciando modo tiempo real...")
        try:
            run_realtime()
        except KeyboardInterrupt:
            print("\nInterrumpido por el usuario")
        except Exception as e:
            print(f"Error en modo tiempo real: {e}")

    elif args.mode == "video":
        if not args.video_path:
            print("Error: Debes especificar --video_path para procesar un video")
            list_available_videos()
            sys.exit(1)

        print("Iniciando procesamiento de video...")
        try:
            success = run_video(args.video_path, args.output_name)
            if success:
                print(f"\nRevisa tu video procesado en: {OUTPUTS_DIR}")
            else:
                sys.exit(1)
        except KeyboardInterrupt:
            print("\nProcesamiento interrumpido por el usuario")
        except Exception as e:
            print(f"Error durante el procesamiento: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
