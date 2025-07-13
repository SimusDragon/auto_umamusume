import win32gui

base_resolution  = (1920, 1080)
window_name = "Umamusume"

class Screen:
    def __init__(self):
        self.last_resolution = (0, 0)
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        windows = []
        def enum_handler(h, ctx):
            if win32gui.IsWindowVisible(h):
                title = win32gui.GetWindowText(h)
                if title == window_name:
                    ctx.append(h)
        win32gui.EnumWindows(enum_handler, windows)
        hwnd = windows[0]

        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        width = right - left
        height = bottom - top

        if (width, height) != self.last_resolution:
            self.last_resolution = (width, height)
            self.scale_x = width / base_resolution[0]
            self.scale_y = height / base_resolution[1]

        self.offset_x, self.offset_y = win32gui.ClientToScreen(hwnd, (0, 0))

    def scale_point(self, x, y):
        self.update()
        return int(x * self.scale_x) + self.offset_x, int(y * self.scale_y) + self.offset_y

    def scale_offset_x(self, x):
        self.update()
        return int(x * self.scale_x)

    def scale_offset_y(self, y):
        self.update()
        return int(y * self.scale_y)

    def scale_region(self, x, y, w, h):
        self.update()
        sx, sy = self.scale_point(x, y)
        sw = int(w * self.scale_x)
        sh = int(h * self.scale_y)
        return (sx, sy, sw, sh)
