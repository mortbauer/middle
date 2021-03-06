import cProfile
import sys
from enum import Enum
from enum import IntEnum
from enum import unique
from typing import Dict
from typing import List
from typing import Set

# --------------------------------------------------------------- #
# Import boilerplate
# --------------------------------------------------------------- #

try:
    import timy
    import middle
    from cattr import structure
    from cattr import unstructure
except ImportError:
    print(
        "To run this script, you must install these dependencies:",
        file=sys.stderr,
    )
    print("- cattrs", file=sys.stderr)
    print("- middle", file=sys.stderr)
    print("- timy", file=sys.stderr)
    sys.exit(1)

# --------------------------------------------------------------- #
# Fixed variables
# --------------------------------------------------------------- #

TOTAL_LOOPS = 1_000_000

if "short" in sys.argv:
    TOTAL_LOOPS = 1


# --------------------------------------------------------------- #
# Object definition
# --------------------------------------------------------------- #


@unique
class PlatformEnum(str, Enum):
    XBOX1 = "XBOX1"
    PLAYSTATION4 = "PLAYSTATION4"
    PC = "PC"


@unique
class LanguageEnum(IntEnum):
    ENGLISH = 1
    JAPANESE = 2
    SPANISH = 3
    GERMAN = 4
    PORTUGUESE = 5


@unique
class CityRegionEnum(str, Enum):
    TROPICAL = "TROPICAL"
    TEMPERATE = "TEMPERATE"
    BOREAL = "BOREAL"


class City(middle.Model):
    name = middle.field(type=str, description="The city name")
    region = middle.field(
        type=CityRegionEnum, description="The region this city is located"
    )


class Game(middle.Model):
    name: str = middle.field(description="The name of the game")
    platform: PlatformEnum = middle.field(
        description="Which platform it runs on"
    )
    score: float = middle.field(description="The average score of the game")
    resolution_tested: str = middle.field(
        description="The resolution which the game was tested",
        pattern="^\d+x\d+$",
    )
    genre: List[str] = middle.field(
        description="One or more genres this game is part of"
    )
    rating: Dict[str, float] = middle.field(
        description="Ratings given on specialized websites"
    )
    players: Set[str] = middle.field(
        description="Some of the notorious players of this game"
    )
    language: LanguageEnum = middle.field(
        description="The main language of the game"
    )
    awesome_city: City = middle.field(description="One awesome city built")


# --------------------------------------------------------------- #
# Test variable
# --------------------------------------------------------------- #

MODEL_INSTANCE = Game(
    name="Cities: Skylines",
    platform="PC",
    score=9.0,
    resolution_tested="1920x1080",
    genre=["Simulators", "City Building"],
    rating={"IGN": 8.5, "Gamespot": 8.0, "Steam": 4.5},
    players=["Flux", "strictoaster"],
    language=1,
    awesome_city=City(name="Blumenau", region=CityRegionEnum.TEMPERATE),
)

# --------------------------------------------------------------- #
# Test runnable
# --------------------------------------------------------------- #


def test_cattr():
    p = unstructure(MODEL_INSTANCE)
    assert isinstance(p, dict)
    game = structure(p, Game)
    assert isinstance(game, Game)
    assert isinstance(game.awesome_city, City)


def test_middle():
    p = middle.asdict(MODEL_INSTANCE)
    assert isinstance(p, dict)
    game = Game(**p)
    assert isinstance(game, Game)
    assert isinstance(game.awesome_city, City)


# --------------------------------------------------------------- #
# Run tests
# --------------------------------------------------------------- #


def main():
    if "profile" in sys.argv:
        cProfile.run(
            "for i in range({}): test_cattr()".format(TOTAL_LOOPS),
            sort="tottime",
        )
        cProfile.run(
            "for i in range({}): test_middle()".format(TOTAL_LOOPS),
            sort="tottime",
        )
    else:
        timy.timer(ident="cattr", loops=TOTAL_LOOPS)(test_cattr).__call__()
        timy.timer(ident="middle", loops=TOTAL_LOOPS)(test_middle).__call__()


if __name__ == "__main__":
    main()
