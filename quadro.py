#!/usr/bin/env python

# # # # # # # # # # # # # # # # # # # # #
#  _____ _____ _____ ____  _____ _____  #
# |     |  |  |  _  |    \| __  |     | #
# |  |  |  |  |     |  |  |    -|  |  | #
# |__  _|_____|__|__|____/|__|__|_____| #
#    |__|                               #
# # # # # # # # # # # # # # # # # # # # #
# FOREGROUND                            #
# BACKGROUND                            #
# BORDERCOLOR                           #
# CURSORCOLOR                           #
# COLOR0                                #
# COLOR1                                #
# [...]                                 #
# COLOR15                               #
# # # # # # # # # # # # # # # # # # # # #
# 10 	= foreground                    #
# 11 	= background                    #
# 12 	= cursor foregound              #
# 17    = highlight background          #
# 19    = highlight foreground          #
# 708   = border                        #
# # # # # # # # # # # # # # # # # # # # #
# INFO  = https://goo.gl/rPE2Aw         #
# # # # # # # # # # # # # # # # # # # # #

from subprocess import Popen as exec
from subprocess import DEVNULL as null
from os import mkdir, mknod, listdir
from os.path import expanduser, isdir, join
import argparse
from  sys import argv
from glob import glob
from shutil import copyfile, which

def build_colors(COL, SPEC):
    COL = ''.join([("\033]4;%s;%s\033\\" % (i, COL[i])) for i in range(0, len(COL))])
    COL += ("\033\\\033]%s;%s" % (10, SPEC[0]))
    COL += ("\033\\\033]%s;%s" % (11, SPEC[1]))
    COL += ("\033\\\033]%s;%s" % (12, SPEC[3]))
    COL += ("\033\\\033]%s;%s" % (17, SPEC[1]))
    COL += ("\033\\\033]%s;%s" % (19, SPEC[0]))
    COL += ("\033\\\033[s\033[1000H\033[8m\033]%s;%s\033\\\033[u" % (708, SPEC[2]))
    return COL 

def save_theme(COL, SPEC, WALLPAPER, COLOR_SCHEME, SEQ):
    copyfile (WALLPAPER, CURRENT_THEME_WALLPAPER)
    copyfile(COLOR_SCHEME, CURRENT_THEME_COLORS)
    COL = [('*.color%s: %s' % (i, COL[i])) for i in range(0, len(COL))]
    COL.append('*foreground: %s' % (SPEC[0]))
    COL.append('*background: %s' % (SPEC[1]))
    COL.append('*.borderColor: %s' % (SPEC[2]))
    COL.append('*.cursorColor: %s' % (SPEC[3]))
    COL.append('*highlightColor: %s' % (SPEC[1]))
    COL.append('*highlightTextColor: %s' % (SPEC[0]))
    with open(CURRENT_THEME_COLORS_RESOURCE, 'w') as file:
        for C in COL:
            file.writelines(C + '\n')
    with open(join(CURRENT_THEME, 'colors.seq'), 'w') as file:
        file.write(SEQ)
        
def apply(SEQ, WALLPAPER):
    exec(['feh', '--bg-scale', CURRENT_THEME_WALLPAPER])
    exec(['xrdb', '-merge', CURRENT_THEME_COLORS_RESOURCE])
    if which('i3'): exec(['i3-msg','reload'], stdout=null,
                                              stderr=null)
    exec(['pkill', '-USR1', 'polybar'])
    for TERM in glob(TTY):
        with open(TERM, 'w') as T:
            T.write(SEQ)


def get_colors(COLOR_FILE):
    with open(COLOR_SCHEME, 'r') as DATA:
        COLORS = DATA.readlines()
    return COLORS

def get_seq():
    with open(CURRENT_THEME_COLORS_SEQ, 'r') as file:
        SEQ = file.read()
    return SEQ

def get_themes():
    return listdir(THEMES_DIR)

def check_dep():
    for D in DEP:
        if not which(D): print('[ERR] Missing dependency <' + D + '>'); exit(0)

DEP = ['feh', 'polybar']
HOME_DIR = expanduser('~')
CONFIG_DIR = join(HOME_DIR, '.config', 'quadro')
THEMES_DIR = join(CONFIG_DIR, 'themes')
CONFIG_FILE = join(CONFIG_DIR + 'config')
CURRENT_THEME = join(THEMES_DIR, 'current')
CURRENT_THEME_COLORS = join(CURRENT_THEME, 'colors')
CURRENT_THEME_COLORS_RESOURCE = join(CURRENT_THEME, 'colors.x')
CURRENT_THEME_COLORS_SEQ = join(CURRENT_THEME, 'colors.seq')
CURRENT_THEME_WALLPAPER = join(CURRENT_THEME, 'wallpaper.jpg')
TTY = "/dev/pts/[0-9]*"

p = argparse.ArgumentParser()

p.add_argument('-t', '--theme',
                metavar='<theme-name>', required=False,
                    help='theme to load , use -l to see avaiable')

p.add_argument('-l', '--list',
                action='store_true', required=False,
                    help='list all the installed themes')

p.add_argument('-c', '--create-new',
                metavar='<theme-name>' ,required=False,
                    help='allow to create a new theme')

p.add_argument('-a', '--add-new',
                metavar='<theme-name>', required=False,
                    help='allow to import a theme from a folder')

p.add_argument('--last',
                action='store_true', required=False,
                    help='load last selected theme')

args = p.parse_args()


if not isdir(CONFIG_DIR):
    print('[ERR] Missing config folder, please reinstall')

if __name__ == '__main__':
    INSTALLED_THEMES = get_themes()

    check_dep()

    if len(argv) < 2: # ON MISSING ARGS PRINT HELP AND QUIT
            p.print_help()
            exit(0)

    if args.list: # IF ARGS IS '-l' OR '--list'
        [print(t) if t != 'current' else None for t in INSTALLED_THEMES]

    if args.theme: # CHANGE THE CURRERNT THEMES
        SELECTED_THEME = join(THEMES_DIR, args.theme)
        WALLPAPER = join(SELECTED_THEME, 'wallpaper.jpg')
        COLOR_SCHEME = join(SELECTED_THEME, 'colors')
        COLORS = get_colors(COLOR_SCHEME)
        SPECIALS = [C.rstrip() for C in COLORS][:4]
        COLORS = [C.rstrip() for C in COLORS][4:]
        SEQ = build_colors(COLORS, SPECIALS)
        save_theme(COLORS, SPECIALS, WALLPAPER, COLOR_SCHEME, SEQ)
        apply(SEQ, WALLPAPER) 

    if args.last: # LOAD THE LAST SELECTED THEME
        SEQ = get_seq()
        apply(SEQ, CURRENT_THEME_WALLPAPER)        

    if args.create_new:
        print('function<create_new> TO IMPLEMENT')

    if args.add_new:
        print('function<add_new> TO IMPLEMENT')
