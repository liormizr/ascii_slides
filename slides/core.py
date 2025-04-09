"""
This Will be a Python Terminal base Slide Show for future Geeky Talks & lectures
"""
import re
import sys
from time import sleep
from os import PathLike
from inspect import getsource
from collections import namedtuple
from itertools import cycle, islice
from functools import cached_property

from colorama import Fore, Back, Style

from bpython import translations
from bpython.repl import extract_exit_value
from bpython.curtsies import FullCurtsiesRepl
from bpython.config import default_config_path, Config
from bpython.curtsiesfrontend.repl import key_dispatch
from bpython.curtsiesfrontend.coderunner import SystemExitFromCodeRunner


__all__ = [
    'main',
    'BaseSlide',
    'SlidesConfig',
    'SlidesRepl',
]


class BaseSlide:
    title: str | None = None
    body: str | None = None
    image: PathLike | None = None
    draft: bool = False

    def code_snippet(self):
        raise NotImplementedError


class _SlidesController:
    _STRATEGY = namedtuple('STRATEGY', ['direction', 'in_progress'])

    def __init__(self, slides):
        self.slides = slides
        self.current = None

    def __repr__(self):
        return f'{type(self).__name__}({self.current=})'

    @cached_property
    def _iterator(self):
        return cycle(self.slides)

    @cached_property
    def _jump_to_previous(self):  # todo: Find a better Name
        jump_to_previous = len(self.slides) - 2
        if jump_to_previous < 0:
            return 0
        return jump_to_previous

    def next(self):
        self.current = next(self._iterator)
        return self.current

    def previous(self):
        prev = next(islice(self._iterator, self._jump_to_previous, None))
        self.current = prev
        return self.current


class SlidesConfig(Config):
    slides_control = {
        'next_slide': '<PAGEUP>',
        'back_slide': '<PAGEDOWN>',
    }


class SlidesRepl(FullCurtsiesRepl):
    _TITLE_REGEX = re.compile(r'(?<!^)(?=[A-Z])')

    def __init__(self, *args, slides: dict[str, BaseSlide], config: SlidesConfig, locals_, **kwargs):
        locals_ = locals_ or {}
        locals_.update(repl=self)
        super().__init__(*args, config=config, locals_=locals_, **kwargs)
        self.slides_controller = _SlidesController(slides=slides)

    def process_event_and_paint(self, event) -> None:
        if event in self.config.slides_control.values():
            if event == self.config.slides_control['next_slide']:
                slide = self.slides_controller.next()
            elif event == self.config.slides_control['back_slide']:
                slide = self.slides_controller.previous()
            return self._process_next_slide(slide)
        return super().process_event_and_paint(event)

    def _process_next_slide(self, slide):
        clear_screen, *_ = key_dispatch[self.config.clear_screen_key]
        left_key, *_ = key_dispatch[self.config.left_key]

        self.process_event_and_paint(clear_screen)

        title = self._TITLE_REGEX.sub(' ', slide.__name__).title()
        text = f'+\n| {Style.BRIGHT}{Fore.CYAN}{title}:\n'
        doc = slide.__doc__.format(Style=Style, Fore=Fore, Back=Back)
        for line in doc.splitlines():
            text += f'| {line}\n'
        text += '|\n+\n'
        self.send_to_stdouterr(text)
        self.process_event_and_paint(left_key)

        code_snippet_text = getsource(slide.code_snippet)
        if 'NotImplementedError' in code_snippet_text:
            return
        for line in code_snippet_text.splitlines()[1:]:
            for character in line[8:]:
                sleep(0.02)
                self.process_event_and_paint(character)
        self.on_enter()


def main(slides, *, locals=None, banner=None):
    """
    banner is displayed directly after the version information.
    welcome_message is passed on to Repl and displayed in the statusbar.
    """
    translations.init()
    config = SlidesConfig(default_config_path())

    exit_value = ()
    sys.path.insert(0, "")
    sys.stdout.write(banner)

    repl = SlidesRepl(
        slides=slides,
        config=config,
        locals_=locals)
    try:
        with repl.input_generator:
            with repl.window as window:
                with repl:
                    repl.height, repl.width = window.t.height, window.t.width
                    repl.mainloop()
    except (SystemExitFromCodeRunner, SystemExit) as error:
        exit_value = error.args
    return extract_exit_value(exit_value)
