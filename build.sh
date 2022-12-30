#!/usr/bin/env bash

(
	code --uninstall-extension 'rltb.bertram' || :
	cd gen_theme && python split_themes.py && cd .. && vsce package && code --install-extension bertram-0.4.1.vsix
)
