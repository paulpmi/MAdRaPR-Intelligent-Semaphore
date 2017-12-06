import random
import xml
import xml.etree.ElementTree as ET
from xml.dom import minidom
import traci
import os
import time
import sys
from copy import deepcopy
xmldoc = minidom.parse('rilsa1.net.xml')
itemlist = xmldoc.getElementsByTagName('phase')
#print(len(itemlist))
#print(itemlist[0].attributes['duration'].value)
#for s in itemlist:
#    print(s.attributes['duration'].value)


class Cell:
    def __init__(self):
        self.value = None


class LightPopulation:
    def __init__(self, nr):
        self.map = {0 : 'r', 1 : 'R', 2: 'y', 3: 'g', 4: 'G'}
        self.pop = [random.randint(0, 5) for _ in range(nr)]
        self.previousPop = self.pop

    def changeValues(self):
        i = 0
        if self.pop[i] > self.pop[i+1]:
                self.pop[i] = random.randint(0, self.pop[i + 1])
        elif self.pop[i] < self.pop[i+1]:
            self.pop[i] = random.randint(15, 31)
        else:
            self.pop[i] = random.randint(5, 31)


class TimePopulation:
    def __init__(self, nr):
        self.pop = [random.randint(5, 31) for _ in range(nr)]
        self.oldpop = deepcopy(self.pop)

    def changeValues(self):
        for i in range(1, len(self.pop)-1):
            if self.pop[i] > self.oldpop[i-1] and self.pop[i] > self.oldpop[i+1]:
                #self.pop[i] = random.randint(self.pop[i-1], self.pop[i])
                self.pop[i] = random.randint(5, 15)
            elif self.pop[i] < self.oldpop[i-1] and self.pop[i] < self.oldpop[i+1]:
                #self.pop[i] = random.randint(self.pop[i], self.pop[i+1])
                self.pop[i] = random.randint(15, 31)
            else:
                if self.pop[i-1] > self.pop[i+1]:
                    self.pop[i-1], self.pop[i + 1] = self.pop[i+1], self.pop[i-1]
                #self.pop[i] = random.randint(self.pop[i-1], self.pop[i+1])
                self.pop[i] = random.randint(5, 31)
        i = 0
        if self.pop[i] > self.pop[i+1]:
            self.pop[i] = random.randint(5, 15)
        elif self.pop[i] < self.pop[i+1]:
            self.pop[i] = random.randint(15, 31)
        else:
            self.pop[i] = random.randint(5, 31)
        i = -1
        if self.pop[i] > self.pop[i-1]:
            self.pop[i] = random.randint(5, 15)
        elif self.pop[i] < self.pop[i-1]:
            self.pop[i] = random.randint(15, 31)
        else:
            self.pop[i] = random.randint(5, 31)

    def modify_xml(self):
        et = xml.etree.ElementTree.parse("D:/facultate/IA/RiLSA_Example/rilsa1_tls.add.xml")
        root = et.getroot()
        for child in root.getchildren():
            tl_id = child.get('id')
            k = 0
            xmldoc.getElementsByTagName('phase')
            for s in itemlist:
                print(s.attributes['duration'].value)
                s.attributes['duration'].value = str(self.pop[k])
                k +=1
            """
            if tl_id == 0:
                for phase in child.getchildren():
                    phase.set('duration', str(self.pop[k]))
                    k += 1
            """
        et.write("D:/facultate/IA/RiLSA_Example/rilsa1_tls.add.xml")

    def interations(self, nrIter):
        for i in range(nrIter):
            self.changeValues()
        print(self.pop)


class Simulation:
    sumoBinary = "C:/Program Files (x86)/DLR/Sumo/bin/sumo"
    sumoBinaryGui = "C:/Program Files (x86)/DLR/Sumo/bin/sumo-gui"
    LogicLocation = "C:/Users/ntvid/Sumo/test/rilsa1_tls.add.xml"

    def __init__(self):

        self.sumo_cmd = [Simulation.sumoBinary, "-c", "D:/facultate/IA/RiLSA_Example/run.sumo.cfg"]
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

    def run_gui(self):
        sumo_cmd = [Simulation.sumoBinaryGui, "-c", "D:/facultate/IA/RiLSA_Example/run.sumo.cfg"]
        traci.start(sumo_cmd)
        step = 0
        arrived = 0
        deaparted = 0
        tp = TimePopulation(len(itemlist))
        while step < 1000:
            traci.simulationStep()
            step += 1
            tp.changeValues()
            tp.modify_xml()
            arrived += traci.simulation.getArrivedNumber()
            deaparted += traci.simulation.getDepartedNumber()
        traci.close()
        print(arrived, deaparted)

    def run_simulation(self):
        traci.start(self.sumo_cmd)
        step = 0
        arrived = 0
        deaparted = 0
        tp = TimePopulation(len(itemlist))
        while step < 1000:
            traci.simulationStep()
            step += 1
            tp.changeValues()
            tp.modify_xml()

            #time.sleep(0.5)
            arrived += traci.simulation.getArrivedNumber()
            deaparted += traci.simulation.getDepartedNumber()
            print("Lights: ")
            print(tp.pop)
            print("Vehicles: ")
            print(arrived,deaparted)
        traci.close()
        return pow(arrived,2) - (deaparted - arrived)

arrived = 0
deaparted = 0
print("Algorithm Started: ")

s = Simulation()
s.run_simulation()
