class MazeModel:
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
        return self.walls[y][x] & direction != 0

    def can_move(self, x, y, direction):
        return not self.has_wall(x, y, direction)

    def neighbors(self, x, y):
        res = []
        if 0 <= x < self.width and 0 <= y - 1 < self.height:
            if self.can_move(x, y, 1):
                res.append((x, y - 1))
        if 0 <= x + 1 < self.width and 0 <= y < self.height:
            if self.can_move(x + 1, y, 2):
                res.append((x + 1, y))
        if 0 <= x < self.width and 0 <= y + 1 < self.height:
            if self.can_move(x, y + 1, 4):
                res.append((x, y + 1))
        if 0 <= x - 1 < self.width and 0 <= y < self.height:
            if self.can_move(x - 1, y, 8):
                res.append((x - 1, y))
        return res

    def p_neighbors(self, x, y):
        res = []
        if 0 <= x < self.width and 0 <= y - 1 < self.height:
            res.append((x, y - 1))
        if 0 <= x + 1 < self.width and 0 <= y < self.height:
            res.append((x + 1, y))
        if 0 <= x < self.width and 0 <= y + 1 < self.height:
            res.append((x, y + 1))
        if 0 <= x - 1 < self.width and 0 <= y < self.height:
            res.append((x - 1, y))
        return res


# # MazeModel
# # │
# # ├── walls
# # ├── width
# # ├── height
# # ├── corners
# # ├── center
# # └── methods
# #     ├── has_wall()
# #     ├── can_move()
# #     └── neighbors()
