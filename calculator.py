import model
import random
import math

class calculator:

    def __init__(self,model_size,model_type='default'):
        self.model_size=model_size
        self.statistics = [0 for x in range(model_size)]
        self.model_type=model_type

    def print_statistics(self):
        sensors = []
        controllers = []
        processors = []
        bus = []
        netwotk = []
        for i in range(6):
            sensors.append(self.statistics[i])
        for i in range(6, 11):
            controllers.append(self.statistics[i])
        for i in range(11, 15):
            processors.append(self.statistics[i])
        if(self.model_type=='default'):
            for i in range(15, 20):
                bus.append(self.statistics[i])
            for i in range(20, 23):
                netwotk.append(self.statistics[i])
            mid_net = self.statistics[23]
        else:
            for i in range(15, 21):
                bus.append(self.statistics[i])
            for i in range(21, 24):
                netwotk.append(self.statistics[i])
            mid_net = self.statistics[24]
        print("Statistics. Count of fail of elements:")
        print("Sensors:",sensors)
        print("Controllers:", controllers)
        print("Processors:", processors)
        print("Bus:", bus)
        print("Network:", netwotk)
        print("Network bus",mid_net)

    def null_statistic(self):
        self.statistics = [0 for x in range(len(self.statistics))]

    def generate_zero_positions(self, number, failures,model_size):
        vectors=set()
        while len(vectors)<number:
            positions=frozenset()
            while (len(positions) < failures):
                positions=frozenset(int(random.uniform(0,model_size)) for i in range(failures))
            vectors.add(positions)
        return vectors

    def get_vector(self,positions,model_size):
        l=model_size
        vector=[1 for x in range(model_size)]
        for p in positions:
            vector[p]=0
        return vector

    def calculate_probability_of_working_system(self,model_size, failures,
                                            percentage,
                                            redistribution=True):
        res = 0.0
        count_of_vectors = math.factorial(model_size) / math.factorial(failures) / math.factorial(
        model_size - failures)
        count_of_vectors = int(count_of_vectors * percentage)
        vectors_with_zero=self.generate_zero_positions(count_of_vectors,failures,model_size)
        for current in vectors_with_zero:
            if(self.model_type=='default'):
                mod= model.Model(self.get_vector(current,model_size))
            else:
                mod=model.Model(self.get_vector(current,model_size),'mod')
            state=mod.total_function() or (mod.redistribute() and redistribution)
            if(state):
                prob = mod.probability()
                res+=prob
            else:
                for v in range(len(self.get_vector(current,model_size))):
                    self.statistics[v]+=self.get_vector(current,model_size)[v]
        return res/percentage

    def calculate_all(self,redistribution=True):
        return (self.calculate_probability_of_working_system(self.model_size,0,1.0,redistribution)+
                self.calculate_probability_of_working_system(self.model_size, 1, 1.0, redistribution) +
                self.calculate_probability_of_working_system(self.model_size, 2, 1, redistribution) +
                self.calculate_probability_of_working_system(self.model_size,3,0.5,redistribution)
                #+self.calculate_probability_of_working_system(self.model_size, 4, 0.1, redistribution)
        )

    def calculate_points(self,redistribution=True):
      return [self.calculate_probability_of_working_system(self.model_size, 0, 1.0, redistribution),
         self.calculate_probability_of_working_system(self.model_size, 1, 1.0, redistribution),
         self.calculate_probability_of_working_system(self.model_size, 2, 0.5, redistribution),
         self.calculate_probability_of_working_system(self.model_size, 3, 0.5, redistribution),
         self.calculate_probability_of_working_system(self.model_size, 4, 0.1, redistribution)]
