class Polymer(object):
    def __init__(self, initial):
        self.chemical_formula = initial
        self._reduced = None
    
    def step(self, formula):
        result = list(formula)
        for i, (first, second) in enumerate(zip(formula, formula[1:])):
            if first in [second.upper(), second.lower()] and first != second:
                result = result[:i] + result[i+2:]
                return "".join(result)
            else:
                pass
        return "".join(result)
    
    @property
    def reduced(self):
        # This works, but it is awfully slow
        if self._reduced:
            return self._reduced
        current = self.chemical_formula
        reduced = False

        while not reduced:
            next_step = self.step(current)
            if next_step == current:
                reduced = True
            else:
                current = next_step
        self._reduced = current
        return current


if __name__ == "__main__":
    in_poly = open("input.txt").read()
    p1 = Polymer(in_poly)
    red = p1.reduced
    print(red, len(red), sep='\n')
