# QUADRO

**quadro** is a theme manager for i3/bspwm/etc.../polybar/rofi

## What it can do?
**quadro** can change:
- terminal colorscheme

- polybar colorscheme

- rofi colorscheme [TODO]

- wm colors [TODO] (support only for i3 right now, will add others later)

## Todo:
- check for actuall program in system [DONE]

- rofi colorscheme

- wm colorscheme

- other wm support

- create_new function

- add_new function

## Dependencies:
- i3

- feh

- rofi [TODO]

- polybar

## Usage:
```quadro -l/--list list all the installed themes```

```quadro -t/--theme <theme-name> set a theme```

```quadro --last load last selected theme```


## Theme Creation:
to create a theme go in ```~/.config/quadro/themes/``` and make a folder for your theme
inside the folder add a file called ```colors``` and your wallpaper called ```wallpaper.jpg```
the file ```colors``` need this format to work properly (otherwise the colors will get scrambled)

```
FOREGROUND
BACKGROUND
BORDERCOLOR
CURSORCOLOR
COLOR0
COLOR1
[...]
COLOR15
```

## Autostart:
just add ```quadro --last``` to you startup script

## Preview:
[youtube](https://www.youtube.com/watch?v=sVwUd4f1DnY)
