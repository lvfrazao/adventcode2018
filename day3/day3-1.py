import re


class Claim(object):
    def __init__(self, claim_id: int, pos: tuple, dim: tuple):
        self.id = claim_id
        self.pos = pos
        self.dim = dim
        self._vertices = None
    
    @property
    def vertices(self) -> tuple:
        if self._vertices is not None:
            return self._vertices
        else:
            verts = set()
            for w in range(self.dim[0]):
                for h in range(self.dim[1]):
                    verts.add((self.pos[0] + w, self.pos[1] + h))
            self._vertices = verts
            return verts 
    
    def intersects(self, other):
        if self.vertices & other.vertices:
            return True
        return False

    @classmethod
    def from_string(cls, line):
        regx = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
        match = regx.search(line)
        c_id, x, y, w, h = match.groups()
        return cls(c_id, (int(x), int(y)), (int(w), int(h)))


item_list = [s for s in open("input.txt").read().split("\n") if s]
all_claims = [Claim.from_string(s) for s in item_list]

all_vertices = {}
for claim in all_claims:
    for point in claim.vertices:
        all_vertices[point] = all_vertices.get(point, 0) + 1

print(sum([x > 1 for x in all_vertices.values()]))
