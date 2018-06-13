class Statistics:

    @staticmethod
    def get_fitness_mean(fitnesses):
        return sum(fitnesses) / len(fitnesses)

    @staticmethod
    def get_fitness_standart_deviation(fitnesses):
        mean = Statistics.get_fitness_mean(fitnesses)
        diffs = [abs(x - mean) for x in fitnesses]
        return sum(diffs) / len(fitnesses)

    @staticmethod
    def separate_random_runs(data):
        # key(generations*populations)
        runs_classification = {}
        for d in data:
            no_eval = int(d.population) * int(d.generations)
            if runs_classification.get(no_eval) is None:
                runs_classification[no_eval] = []
            runs_classification[no_eval].append(d.v)
        return runs_classification

    @staticmethod
    def separate_abc_runs(data):
        # key(generations*populations, limit)
        runs_classification = {}
        for d in data:
            no_eval = int(d.population) * int(d.generations)
            limit = int(d.limit)
            if runs_classification.get((no_eval, limit)) is None:
                runs_classification[(no_eval, limit)] = []
            runs_classification[(no_eval, limit)].append(d.v)
        return runs_classification

    @staticmethod
    def separate_pso_runs(data):
        # key( generations*populations, inertia, cognitive, social)
        runs_classification = {}
        for d in data:
            no_eval = int(d.population) * int(d.generations)
            inertia = int(d.inertia)
            cognitive = int(d.cognitive)
            social = int(d.social)
            if runs_classification.get((no_eval, inertia, cognitive, social)) is None:
                runs_classification[(no_eval, inertia, cognitive, social)] = []
            runs_classification[(no_eval, inertia, cognitive, social)].append(d.v)
        return runs_classification

    @staticmethod
    def map_to_mean_and_std_dev(data):
        new_map = {}
        for key in data.keys():
            mean = Statistics.get_fitness_mean(data[key])
            std_dev = Statistics.get_fitness_standart_deviation(data[key])
            new_map[key] = [mean, std_dev, len(data[key])]
        return new_map
