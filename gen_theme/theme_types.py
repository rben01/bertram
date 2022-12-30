from typing import TypedDict, Union


class AbstractTokenColor(TypedDict):
    scope: Union[list[str], str]


class SingleThemeTokenColorSettings(TypedDict, total=False):
    foreground: str
    background: str


class SingleThemeTokenColor(AbstractTokenColor):
    settings: SingleThemeTokenColorSettings


class SingleThemeDict(TypedDict):
    colors: dict[str, str]
    tokenColors: list[SingleThemeTokenColor]


class ColorPair(TypedDict):
    light: str
    dark: str


class BothThemesTokenColorSettings(TypedDict, total=False):
    foreground: ColorPair
    background: ColorPair


class BothThemesTokenColors(AbstractTokenColor):
    settings: BothThemesTokenColorSettings


class BothThemesDict(TypedDict):
    colors: dict[str, ColorPair]
    tokenColors: list[BothThemesTokenColors]
