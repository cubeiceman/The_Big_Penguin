class Text_Box:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = "Type something to continue"

    def __str__(self):
        return self.text
