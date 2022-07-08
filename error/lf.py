class LineInfo:
    line: int
    col: int
    file: str

    def __init__(self, file: str, line: int, col: int):
        self.file = file
        self.line = line
        self.col = col