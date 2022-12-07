import functools
import os
import shlex
import subprocess
from pathlib import Path
from textwrap import dedent

from click import edit
from rich.align import Align
from rich.console import Group
from rich.layout import Layout
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.style import Style
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from simpleaudio import WaveObject
from spiel import Slide, Triggers
from spiel.deck import Deck
from spiel.renderables.image import Image

deck = Deck(name=f"pytest")


THIS_DIR = Path(__file__).resolve().parent

IMAGES = THIS_DIR / "images"
SOUNDS = THIS_DIR / "sounds"

EXAMPLES = THIS_DIR / "examples"
EXAMPLES_ASSERTIONS = EXAMPLES / "assertions"
EXAMPLES_FIXTURES = EXAMPLES / "fixtures"
EXAMPLES_PARAMETRIZATION = EXAMPLES / "parametrization"
EXAMPLES_HOOKS = EXAMPLES / "hooks"
EXAMPLES_PLUGINS = EXAMPLES / "plugins"


@functools.lru_cache(2**6)
def run_pytest(
    path: Path, extra_args: tuple[str, ...], code: str, start: float
) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            "pytest",
            str(path),
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


def code_slide(
    paths: list[Path],
    triggers: Triggers,
    extra_args: tuple[str, ...],
) -> Layout:
    main_example = paths[0]
    code = main_example.read_text().rstrip()
    title = str(main_example.relative_to(EXAMPLES))

    if triggers.triggered:
        result = run_pytest(
            main_example, extra_args=extra_args, code=code, start=triggers[0]
        )
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
                title=f"$ pytest {title} {shlex.join(a for a in extra_args if a != '--verbose')}",
                border_style=style,
            )
        ),
    )
    return root


def make_example_slide(
    ex_files: list[Path],
    extra_args: tuple[str, ...] = ("--verbose",),
) -> Slide:
    return Slide(
        title=f"{ex_files[0].parent.stem.title()} - Example {ex_files[0].stem.split('_')[-1]}",
        content=lambda triggers: code_slide(
            paths=ex_files,
            triggers=triggers,
            extra_args=extra_args,
        ),
        bindings={"e": edit_file(ex_files[0])},
    )


def edit_file(path):
    def _(suspend):
        with suspend():
            edit(filename=str(path))

    return _


@deck.slide(title="It's What's For Testing")
def title():
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
def why(triggers: Triggers):
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


@deck.slide(title="How does `pytest` make testing fun?")
def why(triggers: Triggers):
    table = Table.grid(expand=False, padding=1, collapse_padding=True)

    reasons = [
        "- Write and debug complex assertions with no fuss",
        "- Flexibly and efficiently reuse setup/teardown code",
        "- Generate new test cases programmatically",
        "- Customize internal behavior",
        "- Reuse code via plugins",
    ]
    table.add_column(justify="left", width=len(max(reasons, key=len)))

    for trigger_to_display_on, reason in enumerate(reasons, start=2):
        table.add_row(reason if len(triggers) >= trigger_to_display_on else "")

    return Align.center(
        Group(
            Padding(
                Markdown(
                    dedent(
                        f"""\
                        ## How?
                        """
                    ),
                    justify="center",
                ),
                pad=(0, 0, 2, 0),
            ),
            Align.center(table),
        ),
        vertical="middle",
    )


@deck.slide(title="Assertions")
def assertions():
    return Align.center(
        Markdown(
            dedent(
                f"""\
                ## Making Assertions

                The vast majority of tests will make some kind of *assertion* that tests whether some condition is true.

                `pytest` allows for a clean, flexible assertion style with very little effort by the user.
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
def fixtures():
    return Padding(
        Align.center(
            Markdown(
                dedent(
                    f"""\
                ## Using Fixtures

                *Fixtures* are a way of encapsulating test setup and teardown.

                In the traditional

                **Arrange, Act, Assert**

                pattern for writing unit tests, fixtures primarily help with *arranging* and occasionally *acting*.
                """
                ),
                justify="center",
            ),
            vertical="middle",
        ),
        pad=(0, 5),
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


@deck.slide(title="Parametrization")
def parametrization():
    return Align.center(
        Markdown(
            dedent(
                f"""\
                ## Parametrization

                *Parametrization* is a mechanism for reusing *test logic* with different *test data*.

                Parametrization serves much the same role as extracting a function does in your business logic.

                By separating instructions from data, we get increased flexibility and expressiveness.
                """
            ),
            justify="center",
        ),
        vertical="middle",
    )


@deck.slide(title="Er, isn't that spelled wrong?")
def parametrization_spelling():
    return Align.center(
        Text.from_markup(
            dedent(
                f"""\
                Yes, it's spelled [red underline]parametrization[/red underline],
                              not [cyan underline]paramet[bold]e[/bold]rization[/cyan underline].

                It's the British spelling.

                Yes, people have asked.

                No, they have not added an alias.
                """
            ),
            justify="center",
        ),
        vertical="middle",
    )


deck.add_slides(
    make_example_slide([EXAMPLES_PARAMETRIZATION / "ex_1.py"]),
    make_example_slide([EXAMPLES_PARAMETRIZATION / "ex_2.py"]),
    make_example_slide([EXAMPLES_PARAMETRIZATION / "ex_3.py"]),
    make_example_slide(
        [EXAMPLES_PARAMETRIZATION / "ex_4.py"], extra_args=("--collect-only",)
    ),
    make_example_slide([EXAMPLES_PARAMETRIZATION / "ex_5.py"]),
)


@deck.slide(title="Hooks")
def hooks(triggers: Triggers):
    return Align.center(
        Markdown(
            dedent(
                f"""\
                ## Hooks

                `pytest` provides a wide variety of *hooks* that can change or add to its default behavior.

                Use these with care! `pytest` is complex and indirect enough as-is!
                """
            ),
            justify="center",
        ),
        vertical="middle",
    )


deck.add_slides(
    make_example_slide([EXAMPLES_HOOKS / "ex_1.py"]),
    make_example_slide([EXAMPLES_HOOKS / "ex_2.py", EXAMPLES_HOOKS / "conftest.py"]),
    make_example_slide(
        [EXAMPLES_HOOKS / "ex_2.py", EXAMPLES_HOOKS / "conftest.py"],
        extra_args=("--verbose", "--db", "postgresql"),
    ),
    make_example_slide(
        [EXAMPLES_HOOKS / "ex_2.py", EXAMPLES_HOOKS / "conftest.py"],
        extra_args=("--verbose", "--db", "sqlite", "postgresql"),
    ),
)


@deck.slide(title="Plugins")
def plugins(triggers: Triggers):
    if triggers.triggered and triggers.now == triggers[-1]:
        wave = WaveObject.from_wave_file(str(SOUNDS / "dun_dun.wav"))
        wave.play().wait_done()

    return Align.center(
        Markdown(
            dedent(
                f"""\
                ## Plugins

                `pytest` has a wide variety of plugins available for installation on PyPI.

                They broadly fall into two camps:

                *Fixture providers*, which provide new globally-available fixtures.

                *Hook implementers*, which use the hook system to change `pytest`'s behavior.
                """
            ),
            justify="center",
        ),
        vertical="middle",
    )


deck.add_slides(
    make_example_slide([EXAMPLES_PLUGINS / "ex_1.py"]),
    make_example_slide([EXAMPLES_PLUGINS / "ex_2.py"]),
    make_example_slide([EXAMPLES_PLUGINS / "ex_3.py"], extra_args=()),
    make_example_slide([EXAMPLES_PLUGINS / "ex_3.py"], extra_args=("-n", "4")),
)


@deck.slide(title="What Next?")
def what_next():
    return Align.center(
        Markdown(
            dedent(
                f"""\
                ## What Next?

                The `pytest` docs are excellent and cover both the API
                and a wide variety of questions about potential use cases.

                If you're using a framework, check whether there's a plugin for it
                (`pytest-flask`, `pytest-django`, etc.).

                The `hypothesis` library integrates with `pytest` to do *property testing*
                (think parametrization, but guided by the computer).

                `pytest` can run `unittest` tests, so it possible to migrate gradually.
                """
            ),
            justify="center",
        ),
        vertical="middle",
    )
