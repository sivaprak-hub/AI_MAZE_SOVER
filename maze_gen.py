import random, sys, time
from PIL import Image, ImageDraw

class Maze:
    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.walls = [[{'N':True,'S':True,'E':True,'W':True} for _ in range(cols)] for _ in range(rows)]
        self.generate(0, 0, set())

    def generate(self, r, c, visited):
        visited.add((r, c))
        dirs = [(-1,0,'N','S'), (1,0,'S','N'), (0,1,'E','W'), (0,-1,'W','E')]
        random.shuffle(dirs)
        for dr, dc, d, opp in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and (nr, nc) not in visited:
                self.walls[r][c][d] = self.walls[nr][nc][opp] = False
                self.generate(nr, nc, visited)

    def get_neighbors(self, r, c):
        nbrs = []
        for dr, dc, d in [(-1,0,'N'), (1,0,'S'), (0,1,'E'), (0,-1,'W')]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and not self.walls[r][c][d]:
                nbrs.append((nr, nc))
        return nbrs

    def draw(self, path, filename):
        scale = 20
        img = Image.new('RGB', (self.cols*scale, self.rows*scale), 'white')
        draw = ImageDraw.Draw(img)
        for r in range(self.rows):
            for c in range(self.cols):
                x, y = c*scale, r*scale
                if self.walls[r][c]['N']: draw.line([(x,y), (x+scale,y)], fill='black', width=2)
                if self.walls[r][c]['W']: draw.line([(x,y), (x,y+scale)], fill='black', width=2)
        #path solution
        if path:
            pts = [(c*scale + scale//2, r*scale + scale//2) for r, c in path]
            draw.line(pts, fill='red', width=3)
        img.save(filename)