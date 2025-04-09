from pathlib import Path
from importlib import import_module

from click import command, option

from . import BaseSlide, main


def _collect_slides(slides_path: Path):
    """
    Collects slides from the given path.

    Args:
        slides_path (Path): Path to the slides directory or file.
    """
    if not slides_path.exists():
        raise ValueError(f'Path does not exist: {slides_path}')
    if slides_path.is_dir():
        raise ValueError(f'Path need to be a file: {slides_path}')
    talk = import_module(slides_path.stem)
    slides = []

    for obj in vars(talk).values():
        if isinstance(obj, type) and obj is not BaseSlide and issubclass(obj, BaseSlide):
            slides.append(obj)
    return talk.__doc__, [
        obj
        for obj in vars(talk).values()
        if isinstance(obj, type)
        if obj is not BaseSlide
        if issubclass(obj, BaseSlide)
    ]


@command()
@option('-s', '--slides-path', type=Path, default=Path('./talk.py'), help='Path to the slides directory/file')
def present(slides_path):
    banner, slides = _collect_slides(slides_path)
    main(slides=slides, banner=banner)


if __name__ == '__main__':
    present()

