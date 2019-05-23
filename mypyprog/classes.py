class Pogresh:
    iskh = []
    x = 0
    y = 0
    z = 0
    dx = 0
    dy = 0
    dz = 0

    def opr(self, pl1):
        self.x = float(pl1[0])
        self.y = float(pl1[1])
        self.z = float(pl1[2])
        self.dx = float(pl1[3].replace(",","."))
        self.dy = float(pl1[4].replace(",","."))
        self.dz = float(pl1[5].replace(",","."))
    def prints(self):
        #print(self.x + " " + self.y + " " + self.z + " " + self.dx + " " + self.dy + " " + self.dz)
        print(self.x,self.y,self.z,self.dx,self.dy,self.dz)

class Measminimizes:
    x = 0.0
    y = 0.0
    z = 0.0

    def ww(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        return 0
    def prints(self):
        print(self.x, self.y, self.z)

