#!/usr/bin/env bash

version="$1"
(
	code --uninstall-extension 'rltb.bertram' || :
	cd gen_theme && python split_themes.py && cd .. && vsce package && code --install-extension bertram-"$version".vsix
)
