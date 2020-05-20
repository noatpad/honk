
class HonkVM:
  def __init__(self, quads, ranges, ctes):
    self.quads = quads
    self.ranges = ranges

    gSize = ranges[0][4] - ranges[0][0]
    lSize = ranges[1][4] - ranges[1][0]
    tSize = ranges[2][4] - ranges[2][0]
    cSize = ranges[3][4] - ranges[3][0]

    self.Globals = [[None] * gSize]
    self.Locals = [[None] * lSize]
    self.Temps = [[None] * tSize]
    # self.Ctes = [[None] * cSize]
    self.Ctes = ctes

  def execute(self):
    for quad in self.quads:
      # Let it begin. The super-switch case
      op = quad[0]

      if (op in ['+', '-', '/', '*']):
        pass

# def honk(obj):
#   vm = HonkVM
