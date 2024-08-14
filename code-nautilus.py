# VSCode and VSCode Insiders Nautilus Extension
#
# Place me in ~/.local/share/nautilus-python/extensions/,
# ensure you have python-nautilus package, restart Nautilus, and enjoy :)
#
# This script is released to the public domain.

from gi.repository import Nautilus, GObject
from subprocess import call
import os

# paths to vscode and vscode insiders
VSCODE = 'code'
VSCODE_INSIDERS = 'code-insiders'

# what names do you want to see in the context menu?
VSCODENAME = 'Code'
VSCODENAME_INSIDERS = 'Code Insiders'

# always create new window?
NEWWINDOW = False


class VSCodeExtension(GObject.GObject, Nautilus.MenuProvider):

    def launch_vscode(self, menu, files, editor):
        safepaths = ''
        args = ''

        for file in files:
            filepath = file.get_location().get_path()
            safepaths += '"' + filepath + '" '

            # If one of the files we are trying to open is a folder
            # create a new instance of vscode
            if os.path.isdir(filepath) and os.path.exists(filepath):
                args = '--new-window '

        if NEWWINDOW:
            args = '--new-window '

        call(editor + ' ' + args + safepaths + '&', shell=True)

    def get_file_items(self, *args):
        files = args[-1]

        item_code = Nautilus.MenuItem(
            name='VSCodeOpen',
            label='Open in ' + VSCODENAME,
            tip='Opens the selected files with VSCode'
        )
        item_code.connect('activate', self.launch_vscode, files, VSCODE)

        item_code_insiders = Nautilus.MenuItem(
            name='VSCodeInsidersOpen',
            label='Open in ' + VSCODENAME_INSIDERS,
            tip='Opens the selected files with VSCode Insiders'
        )
        item_code_insiders.connect('activate', self.launch_vscode, files, VSCODE_INSIDERS)

        return [item_code, item_code_insiders]

    def get_background_items(self, *args):
        file_ = args[-1]

        item_code = Nautilus.MenuItem(
            name='VSCodeOpenBackground',
            label='Open in ' + VSCODENAME,
            tip='Opens the current directory in VSCode'
        )
        item_code.connect('activate', self.launch_vscode, [file_], VSCODE)

        item_code_insiders = Nautilus.MenuItem(
            name='VSCodeInsidersOpenBackground',
            label='Open in ' + VSCODENAME_INSIDERS,
            tip='Opens the current directory in VSCode Insiders'
        )
        item_code_insiders.connect('activate', self.launch_vscode, [file_], VSCODE_INSIDERS)

        return [item_code, item_code_insiders]
