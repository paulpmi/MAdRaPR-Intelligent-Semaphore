from utilis.firebase_handler import Firebasehandler


class Statistics:

    @staticmethod
    def get_fitness_mean(fitnesses):
        return sum(fitnesses)/len(fitnesses)

    @staticmethod
    def get_fitness_standart_deviation(fitnesses):
        mean = Statistics.get_fitness_mean(fitnesses)
        diffs = [abs(x - mean) for x in fitnesses]
        return sum(diffs)/len(fitnesses)

runs = Firebasehandler.get_random_runs("DESKTOP-7T3FAU8","RiLSA_example1")
fitnesses = [x.best_fitness for x in runs]
mean = Statistics.get_fitness_mean(fitnesses)
std = Statistics.get_fitness_standart_deviation(fitnesses)
best = max(fitnesses)
worst = min(fitnesses)
a =1