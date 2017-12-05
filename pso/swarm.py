from particle import Particle


class Swarm:
    def __init__(self, c1, c2, no, intersection):
        self.c1 = c1
        self.c2 = c2
        self.particles = []
        self.numberOfParticles = no

        for i in range(0, no):
            self.particles.append(Particle(intersection))

        for par in self.particles:
            par.evaluate(self.get_best_particle())


    # def get_best_neighbour(self, particle):
    #   # for now: the range of particles that differ only with a maximum of 3-5 seconds for each state
    #    return Particle()

    def get_best_particle(self):
        sorted(self.particles, key=lambda particle: particle.fitness, reverse=True)
        return self.particles[0]

    def update_best(self):
        for particle in self.particles:
            # see if it is ok to use != operator on referenced types
            if particle != self.best:
                if particle.fitness > self.best.fitness:
                    for p in self.particles:
                        p.bestPosition = self.best.bestPosition
                        p.BestFitness = self.best.BestFitness
                    break
