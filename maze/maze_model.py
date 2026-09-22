class MazeModel:
    MOVES = [
        (1, 0, -1),
        (2, 1, 0),
        (4, 0, 1),
        (8, -1, 0)
    ]

    def __init__(self, maze):
        self.walls = maze.maze
        self.height = len(self.walls)
        self.width = len(self.walls[0])

        self.corners = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]
        self.center = (self.width // 2, self.height // 2)

    def has_wall(self, x, y, direction):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        return (self.walls[y][x] & direction) != 0

    def can_move(self, x, y, direction):
        return not self.has_wall(x, y, direction)

    def neighbors(self, x, y):
        res = []
        for direction, dx, dy in self.MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and self.can_move(x, y, direction):
                res.append((nx, ny))
        return res

    def p_neighbors(self, x, y):
        res = []
        for _, dx, dy in self.MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                res.append((nx, ny))
        return res