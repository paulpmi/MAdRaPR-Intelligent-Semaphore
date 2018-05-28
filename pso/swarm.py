from particle import Particle


class Swarm:
    def __init__(self, no, intersection):
        self.particles = []
        self.no_particles = no

        for i in range(0, no):
            self.particles.append(Particle(intersection))

    # def get_best_neighbour(self, particle):
    #   # for now: the range of particles that differ only with a maximum of 3-5 seconds for each state
    #    return Particle()

    def get_best_particle(self):
        pBest = self.particles[0]
        for p in self.particles:
            if p.fitness < pBest.fitness:
                pBest = p
        return pBest

    def fly_away(self, size):
        size = min(size, self.no_particles)
        sorted(self.particles, key=lambda x: x.fitness, reverse=True)

    def update_best(self):
        for particle in self.particles:
            # see if it is ok to use != operator on referenced types
            if particle != self.best:
                if particle.fitness < self.best.fitness:
                    for p in self.particles:
                        p.bestPosition = self.best.bestPosition
                        p.BestFitness = self.best.BestFitness
                    break
