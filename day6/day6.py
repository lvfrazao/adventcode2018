class Grid(object):
    def __init__(self, points):
        self.points = points
        self._bounds = None
        self._area_points = None
        for point in self.points:
            self.is_infinite(point)

    @property
    def bounds(self):
        if self._bounds is not None:
            pass
        else:
            xs = [point.x for point in self.points]
            ys = [point.y for point in self.points]
            leftmost = min(xs)
            rightmost = max(xs)
            uppermost = max(ys)
            lowermost = min(ys)
            self._bounds = (leftmost, rightmost, uppermost, lowermost)
        return self._bounds
    
    def is_edge(self, point):
        leftmost, rightmost, uppermost, lowermost = self.bounds
        if any([
            point.x == leftmost,
            point.x == rightmost,
            point.y == uppermost,
            point.y == lowermost]
        ):
            return True
    
    @property
    def in_area_points(self):
        if self._area_points is not None:
            pass
        else:
            leftmost, rightmost, uppermost, lowermost = self.bounds
            x_len = rightmost - leftmost
            y_len = uppermost - lowermost
            points = []
            for x in range(x_len + 1):
                for y in range(y_len + 1):
                    points.append(Point((leftmost + x, lowermost + y)))
            self._area_points = points
        return self._area_points
    
    def is_infinite(self, point):
        if point.infinite is not None:
            pass
        else:
            leftmost, rightmost, uppermost, lowermost = self.bounds
            if any(
                [
                    point.x <= leftmost,
                    point.x >= rightmost,
                    point.y >= uppermost,
                    point.y <= lowermost
                ]):
                point.infinite = True
            else:
                point.infinite = False
        return point.infinite
    
    def areas(self):
        areas = {(point.x, point.y): 0 for point in self.points}
        self.point_distances = {}
        areas[None] = 0
        for point in self.in_area_points:
            closest = None
            closest_distance = (self.bounds[1] - self.bounds[0]) * (self.bounds[2] - self.bounds[3])
            for location in self.points:
                cur_dist = location.distance(point)
                self.point_distances[point] = self.point_distances.get(point, 0) + cur_dist 
                if cur_dist == closest_distance:
                    closest = None
                elif cur_dist < closest_distance:
                    closest = location
                    closest_distance = cur_dist
            if closest is not None:
                areas[(closest.x, closest.y)] = areas.get((closest.x, closest.y), 0) + 1
                if self.is_edge(point):
                    i = self.points.index(closest)
                    self.points[i].infinite = True
            else:
                areas[None] += 1

        results = {}
        for point in areas:
            if point is None:
                continue
            point = Point(point)
            i = self.points.index(point)
            if not self.points[i].infinite:
                results[(point.x, point.y)] = areas[(point.x, point.y)]
        return results


class Point(object):
    def __init__(self, coord):
        self.x, self.y = coord
        self.infinite = None

    def distance(self, other):
        dist = abs(self.x - other.x) + abs(self.y - other.y)
        return dist
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        else:
            return NotImplemented
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self):
        return f"Point(({self.x}, {self.y}))"


def ingest(text):
    text_list = text.split("\n")
    coords = [
        (int(s.split(", ")[0]), int(s.split(", ")[1])) for s in text_list
    ]
    return coords


text = open("input.txt").read()
points = [Point(s) for s in ingest(text)]
grid = Grid(points)
area_by_point = grid.areas()

highest_finite_point = sorted([t for t in area_by_point.items() if t[0]], key=lambda x: x[1], reverse=True)[0][0]
highest_finite_area = area_by_point[highest_finite_point]
print(
    f"The point with the largest finite area is {highest_finite_point}",
    f"with {highest_finite_area} area"
)

points_under_10k_dist = {point: dist for point, dist in grid.point_distances.items() if dist < 10000}
print(len(points_under_10k_dist), "points have combined distance of less than 10k")
