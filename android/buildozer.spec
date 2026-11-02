[app]
title = PokeStat Challenge
package.name = pokestatchallenge
package.domain = fr.pokestat
source.dir = .
source.include_exts = py,png,jpg,jpeg,json,kv,ttf
icon.filename = assets/pokestat_icon.png
version = 1.0
requirements = python3,kivy,certifi
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 36
android.minapi = 24
android.ndk = 28c
p4a.branch = develop
android.release_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
