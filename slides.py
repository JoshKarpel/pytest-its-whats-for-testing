import functools
import inspect
import os
import shlex
import subprocess
from pathlib import Path
from textwrap import dedent

from rich.align import Align
from rich.box import SQUARE
from rich.console import Group
from rich.layout import Layout
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text
from spiel import Slide, Triggers
from spiel.deck import Deck
from spiel.renderables.image import Image

deck = Deck(name=f"pytest")


THIS_DIR = Path(__file__).resolve().parent
IMAGES = THIS_DIR / "images"
EXAMPLES = THIS_DIR / "examples"


@deck.slide(title="It's What's For Testing")
def image():
    return Align.center(
        Image.from_file(IMAGES / "logo.png"),
        width=86,  # image is exactly 86 wide, 70 tall
        height=70,
    )


@deck.slide(title="What is `pytest`?")
def what():
    return Padding(
        Align.center(
            Markdown(
                dedent(
                    """\
                    ## What?

                    > The `pytest` framework makes it easy to write small, readable tests,
                    > and can scale to support complex functional testing for applications and libraries.
                    """
                ),
                justify="center",
            ),
            vertical="middle",
        ),
        pad=(0, 5),
    )


@deck.slide(title="Why use `pytest`?")
def what(triggers: Triggers):
    return Align.center(
        Markdown(
            dedent(
                f"""\
                ## Why?

                `pytest` makes writing tests _fun_!
                """
            ),
            justify="center",
        ),
        vertical="middle",
    )


@deck.slide(title="Assertions")
def what(triggers: Triggers):
    return Align.center(
        Markdown(
            dedent(
                f"""\
                ## Making Assertions
                """
            ),
            justify="center",
        ),
        vertical="middle",
    )


@functools.lru_cache(maxsize=2**6)
def run_pytest(path: Path, code: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            "pytest",
            str(path),
            "--verbose",
            "--no-header",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=os.environ
        | {
            "FORCE_COLOR": "true",
            "COLUMNS": str(40),
        },
        cwd=EXAMPLES,
    )


def code_slide(path: Path, run: bool) -> Layout:
    code = path.read_text().rstrip()
    title = str(path.relative_to(EXAMPLES))

    if run:
        result = run_pytest(path, code)
        style = Style(color="green" if result.returncode == 0 else "red")
        out = Text("\n", no_wrap=False).join(
            Text.from_ansi(line.rstrip(), no_wrap=True)
            for line in result.stdout.splitlines()
        )
    else:
        style = Style()
        out = Text("")

    root = Layout()

    root.split_row(
        Layout(
            Panel(
                Syntax(
                    code,
                    lexer="python",
                    line_numbers=False,
                ),
                border_style=Style(color="magenta"),
                title=f"$ cat {title}",
            ),
            size=max(len(line) for line in code.splitlines()) + 4,
        ),
        Layout(
            Panel(
                out,
                title=f"$ pytest {title}",
                border_style=style,
            )
        ),
    )
    return root


def make_slide(ex_dir: Path, ex_file: Path):
    @deck.slide(
        title=f"{ex_dir.stem.title()} - Example {ex_file.stem.split('_')[-1]}",
        edit_target=ex_file,
    )
    def ex(triggers: Triggers):
        return code_slide(
            path=ex_file,
            run=triggers.triggered,
        )


for ex_dir in [EXAMPLES / "assertions", EXAMPLES / "fixtures"]:
    for ex_file in sorted(
        (path for path in ex_dir.iterdir() if path.stem.startswith("ex"))
    ):
        make_slide(ex_dir, ex_file)
