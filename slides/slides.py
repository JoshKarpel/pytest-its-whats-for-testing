import inspect
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


@deck.slide(title="It's What's For Testing")
def image():
    return Image.from_file(Path(__file__).resolve().parent / "pytestblack.png")


@deck.slide(title="What is pytest?")
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


@deck.slide(title="Why use pytest?")
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


@deck.slide(title="Decks and Slides")
def code():
    markup = dedent(
        f"""\
        ## Decks are made of Slides

        Here's the code for `Deck` and `Slide`!
        """
    )
    root = Layout()
    upper = Layout(Markdown(markup, justify="center"), size=len(markup.split("\n")) + 1)
    lower = Layout()
    root.split_column(upper, lower)

    def make_code_panel(obj):
        lines, line_number = inspect.getsourcelines(obj)
        return Panel(
            Syntax(
                "".join(lines),
                lexer="python",
                line_numbers=True,
                start_line=line_number,
            ),
            box=SQUARE,
            border_style=Style(dim=True),
            height=len(lines) + 2,
        )

    lower.split_row(
        Layout(make_code_panel(Deck)),
        Layout(make_code_panel(Slide)),
    )

    return root
