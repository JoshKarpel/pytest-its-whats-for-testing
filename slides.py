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
EXAMPLES_ASSERTIONS = EXAMPLES / "assertions"
EXAMPLES_FIXTURES = EXAMPLES / "fixtures"
EXAMPLES_PARAMETRIZATION = EXAMPLES / "parametrization"
EXAMPLES_PLUGINS = EXAMPLES / "plugins"


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


@functools.lru_cache(maxsize=2**6)
def run_pytest(
    path: Path, code: str, extra_args: tuple[str]
) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            "pytest",
            str(path),
            "--verbose",
            "--no-header",
            *extra_args,
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


def code_slide(paths: list[Path], run: bool, extra_args: tuple[str]) -> Layout:
    main_example = paths[0]
    code = main_example.read_text().rstrip()
    title = str(main_example.relative_to(EXAMPLES))

    if run:
        result = run_pytest(main_example, code, extra_args)
        style = Style(color="green" if result.returncode == 0 else "red")
        out = Text("\n", no_wrap=False).join(
            Text.from_ansi(line.rstrip(), no_wrap=True)
            for line in result.stdout.splitlines()
        )
    else:
        style = Style()
        out = Text("")

    root = Layout()

    example_panels = []
    max_width = 0
    for path in paths:
        ex_code = path.read_text().rstrip()
        ex_title = path.relative_to(EXAMPLES)

        example_panels.append(
            Panel(
                Syntax(
                    ex_code,
                    lexer="python",
                    line_numbers=False,
                ),
                border_style=Style(color="magenta"),
                title=f"$ cat {ex_title}",
            ),
        )
        max_width = max(max(len(line) for line in ex_code.splitlines()) + 4, max_width)

    files_layout = Layout(Group(*example_panels), size=max_width)

    root.split_row(
        files_layout,
        Layout(
            Panel(
                out,
                title=f"$ pytest {title}",
                border_style=style,
            )
        ),
    )
    return root


def make_example_slide(
    ex_files: list[Path], extra_args: tuple[str] | None = None
) -> Slide:
    return Slide(
        title=f"{ex_files[0].parent.stem.title()} - Example {ex_files[0].stem.split('_')[-1]}",
        content=lambda triggers: code_slide(
            paths=ex_files, run=triggers.triggered, extra_args=extra_args or ()
        ),
        edit_target=ex_files[0],
    )


@deck.slide(title="Assertions")
def assertions():
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


deck.add_slides(
    make_example_slide([EXAMPLES_ASSERTIONS / "ex_1.py"]),
    make_example_slide([EXAMPLES_ASSERTIONS / "ex_2.py"]),
    make_example_slide([EXAMPLES_ASSERTIONS / "ex_3.py"]),
)


@deck.slide(title="Fixtures")
def assertions():
    return Align.center(
        Markdown(
            dedent(
                f"""\
                ## Using Fixtures
                """
            ),
            justify="center",
        ),
        vertical="middle",
    )


deck.add_slides(
    make_example_slide([EXAMPLES_FIXTURES / "ex_1.py"]),
    make_example_slide([EXAMPLES_FIXTURES / "ex_2.py"]),
    make_example_slide(
        [EXAMPLES_FIXTURES / "ex_3.py", EXAMPLES_FIXTURES / "conftest.py"]
    ),
    make_example_slide([EXAMPLES_FIXTURES / "ex_4.py"]),
    make_example_slide([EXAMPLES_FIXTURES / "ex_5.py"], extra_args=("--setup-plan",)),
    make_example_slide([EXAMPLES_FIXTURES / "ex_6.py"]),
)
