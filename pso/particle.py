class Particle:
    def __init__(self, intersection):
        self.position = []  # list of integers representing the time duration for each state
        self.velocity = 0
        self.fitness = 0
        self.bestPosition = ""
        self.BestFitness = 0

    # the numbers of cars that had reached their destination in a simulation time of t squared minus the number of those
    #  who haven't
    def evaluate(self):
        return 0

    def update(self, particle):
        #update velocity
        #update position
        return 0
