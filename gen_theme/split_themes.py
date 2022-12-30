# %%
import json
from pathlib import Path
from typing import Literal, TypedDict
from common import LIGHT, DARK

from theme_types import (
    BothThemesDict,
    SingleThemeDict,
)

_ThemeDict = TypedDict(
    "_ThemeDict",
    {
        "name": str,
        "$schema": Literal["vscode://schemas/color-theme"],
        "type": Literal["light", "dark"],
    },
)


class ThemeDict(SingleThemeDict, _ThemeDict):
    pass


_SplitTheme = TypedDict("_SplitTheme", {LIGHT: ThemeDict, DARK: ThemeDict})  # type: ignore


class SplitTheme(_SplitTheme):
    pass


def load_dict() -> BothThemesDict:
    with open("./themes_light_dark.json") as f:
        return json.load(f)


def split_dict(d: BothThemesDict) -> SplitTheme:
    def base_dict(theme: str) -> ThemeDict:
        return {
            "name": f"Bertram {theme.title()}",
            "$schema": "vscode://schemas/color-theme",
            "type": theme,
            "colors": {},
            "tokenColors": [],
        }

    splitted = {LIGHT: base_dict("light"), DARK: base_dict("dark")}

    for (color, light_dark) in d["colors"].items():
        for theme in [LIGHT, DARK]:
            splitted[theme]["colors"][color] = light_dark[theme]

    for token_color in d["tokenColors"]:
        for theme in [LIGHT, DARK]:
            tc = {"scope": token_color["scope"], "settings": {}}
            for (key, value) in token_color["settings"].items():
                if key in ("foreground", "background"):
                    value = value[theme]

                tc["settings"][key] = value

            splitted[theme]["tokenColors"].append(tc)

    return splitted


def main():
    d = split_dict(load_dict())
    for (k, theme) in [(LIGHT, "light"), (DARK, "dark")]:
        with Path().resolve().parent.joinpath(
            "dist", f"bertram-{theme}-color-theme.json"
        ).open("w") as f:
            json.dump(d[k], f, indent="\t")


if __name__ == "__main__":
    main()
