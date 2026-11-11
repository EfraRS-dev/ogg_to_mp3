from pathlib import Path
import subprocess
import sys


def get_ffmpeg_path() -> str:
    try:
        import imageio_ffmpeg
    except ImportError:
        print(
            "Error: the FFmpeg dependency is missing. Install it with "
            "'python -m pip install -r requirements.txt'.",
            file=sys.stderr,
        )
        raise

    return imageio_ffmpeg.get_ffmpeg_exe()


def main() -> int:
    root = Path(__file__).resolve().parent
    output_dir: Path | str = root / "output"
    ogg_files = sorted(
        file_path
        for file_path in root.iterdir()
        if file_path.is_file() and file_path.suffix.lower() == ".ogg"
    )

    if not ogg_files:
        print(f"No OGG files found in {root}")
        return 0

    try:
        ffmpeg_path: str = get_ffmpeg_path()
    except (ImportError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 1

    output_dir.mkdir(exist_ok=True)
    failed: bool = False

    for ogg_file in ogg_files:
        mp3_file: Path = output_dir / f"{ogg_file.stem}.mp3"
        print(f"Converting {ogg_file.name} -> output\\{mp3_file.name}")
        result = subprocess.run(
            [
                ffmpeg_path,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(ogg_file),
                "-codec:a",
                "libmp3lame",
                "-q:a",
                "2",
                str(mp3_file),
            ],
            check=False,
        )
        if result.returncode != 0:
            print(f"Failed to convert {ogg_file.name}", file=sys.stderr)
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())