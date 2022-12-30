# %%
import json
from pathlib import Path
from typing import Any, Union, cast

import json5
from common import DARK, LIGHT
from theme_types import BothThemesDict, BothThemesTokenColorSettings, SingleThemeDict


def read_json(theme: str) -> SingleThemeDict:
    with Path().resolve().parent.joinpath(
        "dist", f"bertram-{theme}-color-theme.json"
    ).open() as f:
        return json5.load(f)


def to_key(s: Any) -> Union[str, tuple[str, ...]]:
    if not isinstance(s, str):
        s = tuple(s)
    return s


def merge(light: SingleThemeDict, dark: SingleThemeDict) -> BothThemesDict:
    d: BothThemesDict = {"colors": {}, "tokenColors": []}

    colors = d["colors"]

    # iterate keys in order of appearance
    for color in {**light["colors"], **dark["colors"]}:
        colors[color] = {
            LIGHT: light["colors"][color].lower(),
            DARK: dark["colors"][color].lower(),
        }

    # merge token colors
    token_colors_temp: dict[tuple[str, ...], Any] = {}
    for (theme, theme_dict) in [(LIGHT, light), (DARK, dark)]:
        for token_color_dict in theme_dict["tokenColors"]:
            settings_single = token_color_dict["settings"].copy()
            fg_color = settings_single.pop("foreground", None)
            bg_color = settings_single.pop("background", None)

            settings = cast(
                BothThemesTokenColorSettings,
                settings_single,
            )

            settings = cast(
                BothThemesTokenColorSettings,
                token_colors_temp.setdefault(to_key(token_color_dict["scope"]), {}),
            )
            settings.update(settings_single)

            for (key, color) in [("foreground", fg_color), ("background", bg_color)]:
                if color is None:
                    continue

                settings.setdefault(key, {}).update({theme: color.lower()})

    d["tokenColors"] = [
        {"scope": scope, "settings": settings}
        for (scope, settings) in token_colors_temp.items()
    ]

    return d


def main():
    with open("themes_light_dark.json", "w") as f:
        d = merge(read_json("light"), read_json("dark"))
        json.dump(d, f, indent="\t")


if __name__ == "__main__":
    main()
