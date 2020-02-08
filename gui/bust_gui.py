from gui.frames import GuiFrames
from gui.gui_defs import GuiGlobals
from gui.menus import GuiMenus


class BustGui:
    def __init__(self):
        pass

    def setup_bust_gui(self):
        GuiMenus().cfg()
        guiframes = GuiFrames()
        guiframes.cfg()


if __name__ == "__main__":
    BustGui().setup_bust_gui()
    GuiGlobals().root.mainloop()
