import xml


class ConfigurationIO:
    def __init__(self):
        pass

    @staticmethod
    def modify_sumo_configuration(simulation, solution):
        et = xml.etree.ElementTree.parse(simulation.LogicLocation)
        root = et.getroot()
        for child in root.getchildren():
            k = 0
            if child.tag == "tlLogic":
                for phase in child.getchildren():
                    phase.set('duration', str(solution[k]))
                    k += 1
        et.write(simulation.LogicLocation)
