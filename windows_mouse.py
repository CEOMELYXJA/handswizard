import ctypes

class WindowsMouse:
    def __init__(self):
        self.user = ctypes.windll.user32
        self.user.SetProcessDPIAware()
    def moveRel(self, dx, dy, duration=0):
        p = ctypes.wintypes.POINT()
        self.user.GetCursorPos(ctypes.byref(p))
        self.user.SetCursorPos(p.x + dx, p.y + dy)
    def mouseDown(self, button): self.user.mouse_event(2 if button == 'left' else 8, 0, 0, 0, 0)
    def mouseUp(self, button): self.user.mouse_event(4 if button == 'left' else 16, 0, 0, 0, 0)
    def click(self, button):
        self.mouseDown(button)
        self.mouseUp(button)
    def scroll(self, n): self.user.mouse_event(0x800, 0, 0, n * 120, 0)
