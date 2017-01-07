import queue
import copy
from vertex import Vertex
from graph import Graph

#Первые 6 - датчики, следующие 5 - контроллеры, следующие 4
# процессоры, следующие 5 - шины, следующие 3 - сетевые модули, следующий 1 - канал связи M
#total 24, but numeration from 0
class Model:
    def assign(self,data):
        self.data=data
        self.sensors=[]
        self.controllers=[]
        self.processors=[]
        self.bus=[]
        self.netwotk=[]
        for i in range(6):
            self.sensors.append(data[i])
        for i in range(6,11):
            self.controllers.append(data[i])
        for i in range(11,15):
            self.processors.append(data[i])
        if(self.type_of_model=='default'):
            for i in range(15,20):
                self.bus.append(data[i])
            for i in range(20,23):
                self.netwotk.append(data[i])
            self.mid_net=data[23]
        else:
            for i in range(15, 21):
                self.bus.append(data[i])
            for i in range(21, 24):
                self.netwotk.append(data[i])
            self.mid_net = data[24]

    def __init__(self,data,type='default'):
        self.type_of_model = type
        self.assign(data)

        self.processors_table=[]
        self.processors_table.append({'nominal_load': 40, "max_load": 100,
                                      "reloading": [ 0, 30, 40, 10]
                                      })
        self.processors_table.append({'nominal_load': 70, "max_load": 100,
                                      "reloading": [50, 0, 50, 20]
                                      })
        self.processors_table.append({'nominal_load': 20, "max_load": 80,
                                      "reloading": [20, 20, 0, 20]
                                      })
        self.processors_table.append({'nominal_load': 50, "max_load": 80,
                                      "reloading": [50, 30, 20, 0]
                                      })
        self.sensors_reliability=3.2*10e-5
        self.controllers_reliability=1.9*10e-4
        self.processors_reliability=1.2*10e-4
        self.bus_reliability=1.4*10e-5
        self.netwotk_reliability=1.1*10e-4
        self.mid_net_reliability=3.3*10e-4


    # def f1(self):
    #    return (((self.sensors[0] or self.sensors[1]) and self.controllers[0]) or ( (self.sensors[2] or self.sensors[1]) and self.controllers[1] )) and (self.bus[0] or self.bus[1]) \
    #     and (self.processors[0] or self.processors[1] or self.processors[2] or (self.netwotk[0] and self.mid_net and self.netwotk[1]
    #                                                                             and (self.bus[2] or self.bus[4]) and self.processors[3]))
    #
    # def f2(self):
    #    return self.sensors[3] and self.controllers[2] and self.mid_net and((self.netwotk[0] and (self.bus[0] or self.bus[1]))
    #                                                                  and(self.processors[0] or self.processors[1] or
    #                                                                      self.processors[2]) or (self.netwotk[1] and(self.bus[4] or self.bus[2])
    #                                                                      and self.processors[3]))
    #
    # def f3(self):
    #     return (self.sensors[4] or self.sensors[5]) and self.controllers[4] and self.bus[2] \
    #             and (self.processors[3] or (self.netwotk[1] and self.mid_net and self.netwotk[0] and (self.bus[0] or self.bus[1])
    #                                         and (self.processors[0] or self.processors[1] or self.processors[2])))
    #
    #
    #
    # def f4(self):
    #     return (self.sensors[5] and self.controllers[4] and(self.bus[2] and(self.processors[3] or
    #     (self.netwotk[1] and self.mid_net and self.netwotk[0] and (self.bus[0] or self.bus[1])
    #      and (self.processors[0] or self.processors[1] or self.processors[2]))
    #                                                                  ) or (self.bus[3] and(self.processors[3] or (self.netwotk[2])
    #                                                                                        and self.bus[3] and (self.netwotk[1] and self.mid_net and self.netwotk[0] and (self.bus[0] or self.bus[1])
    #                                                                                                             and (self.processors[0] or self.processors[1] or self.processors[2]))))))

    # def f1(self):
    #     return (((self.sensors[0] or self.sensors[1]) and self.controllers[0]) or ( (self.sensors[2] or self.sensors[1]) and self.controllers[1] )) and (self.bus[0] or self.bus[1]) \
    #         and (self.processors[0])
    #
    # def f2(self):
    #     return self.sensors[3] and self.controllers[2] and self.mid_net and((self.netwotk[0] and (self.bus[0]))
    #                                                                  and(self.processors[2]) or (self.netwotk[1] and(self.bus[4] or self.bus[2])
    #                                                                      and self.processors[3]))
    #
    #
    # def f3(self):
    #     return (self.sensors[4] or self.sensors[5]) and self.controllers[4] and self.bus[2] \
    #             and (self.processors[3] or (self.netwotk[1] and self.mid_net and self.netwotk[0] and (self.bus[1])
    #                                         and (self.processors[2])))
    #
    # def f4(self):
    #     return (self.sensors[5] and(self.bus[2] and(self.processors[3])
    #                                                         or (self.bus[3] and(self.processors[3] or (self.netwotk[2])
    #                                         and self.bus[3] and (self.netwotk[1] and self.mid_net and self.netwotk[0] and (self.bus[0] or self.bus[1])
    #                                                                                                             and (self.processors[1]))))))
    #

    def f1(self):
        return (((self.sensors[0] or self.sensors[1]) and self.controllers[0]) or ( (self.sensors[2] or self.sensors[1]) and self.controllers[1] )) and (self.bus[0] or self.bus[1]) \
            and (self.processors[0] or self.processors[1])

    def f2(self):
        return self.sensors[3] and self.controllers[2] and self.mid_net and((self.netwotk[0] and (self.bus[0] or self.bus[1]))
                                                                     and(self.processors[2]) or (self.netwotk[1] and(self.bus[4] or self.bus[2])
                                                                         and self.processors[3]))


    def f3(self):
        return (self.sensors[4] or self.sensors[5]) and self.bus[2] and self.processors[3]

    def f4(self):
        return (self.sensors[5] and self.controllers[4] and self.bus[3] and self.netwotk[2] and self.bus[4] and self.processors[3])

    def f1_mod(self):
        return (((self.sensors[0] or self.sensors[1]) and self.controllers[0]) or ( (self.sensors[2] or self.sensors[1]) and self.controllers[1] )) and (self.bus[0] or self.bus[1] or self.bus[5]) \
            and (self.processors[0] or self.processors[1])

    def f2_mod(self):
        return self.sensors[3] and self.controllers[2] and self.mid_net and((self.netwotk[0] and (self.bus[0] or self.bus[1] or self.bus[5]))
                                                                     and(self.processors[2]) or (self.netwotk[1] and(self.bus[4] or self.bus[2])
                                                                         and self.processors[3]))


    def f3_mod(self):
        return (self.sensors[4] or self.sensors[5]) and (self.controllers[3] or self.controllers[4]) \
        and (self.bus[2] or (self.netwotk[2] and self.bus[4])) and self.processors[3]



    def total_function(self):
        if(self.type_of_model=='default'):
            return self.f1() and self.f2() and self.f3() and self.f4()
        else: return self.f1_mod() and self.f2_mod() and self.f3_mod()

    def probability(self):
        res=1
        for sensor in self.sensors:
            if(sensor):
                res*=1-self.sensors_reliability
            else:
                res*=self.sensors_reliability

        for controller in self.controllers:
            if (controller):
                res *= 1 - self.controllers_reliability
            else:
                res *= self.controllers_reliability

        for processor in self.processors:
            if (processor):
                res *= 1 - self.processors_reliability
            else:
                res *= self.processors_reliability

        for bus in self.bus:
            if (bus):
                res *= 1 - self.bus_reliability
            else:
                res *= self.bus_reliability

        for network in self.netwotk:
            if (network):
                res *= 1 - self.netwotk_reliability
            else:
                res *= self.netwotk_reliability
        if(self.mid_net):
            res*=1-self.mid_net_reliability
        else: res*=self.mid_net_reliability
        return res

    def redistribute(self):
        modules_for_redistribute=[]
        for i in range(len(self.processors)):
            if(self.processors[i]==0):
                modules_for_redistribute.extend([i])
        if(len(modules_for_redistribute)==0): return False;

        redistrib_table = {}
        for i in range(len(self.processors_table)):
            if (i in modules_for_redistribute):
                redistrib_table[i] = copy.deepcopy(self.processors_table[i]['reloading'])
                for m in modules_for_redistribute:
                    redistrib_table[i][m]=0

        #print(redistrib_table, modules_for_redistribute)
        we_need_at_least=0
        for m in modules_for_redistribute:
            we_need_at_least+=self.processors_table[m]['nominal_load']
        free_space=0
        for pr in range(len(self.processors_table)):
            if pr not in modules_for_redistribute:
                #if (len(modules_for_redistribute) > 1):print(pr)
                free_space+=self.processors_table[pr]["max_load"]-self.processors_table[pr]["nominal_load"]
        #if(len(modules_for_redistribute)>1): print(we_need_at_least,free_space,modules_for_redistribute)
        if(we_need_at_least>free_space): return False

        current_loading=[]
        max_loading = []
        for pr in self.processors_table:
            current_loading.append(pr['nominal_load'])
            max_loading.append(pr['max_load'])
        start=Vertex(redistrib_table,modules_for_redistribute,current_loading,max_loading)
        gr=Graph(start)
        #start.buildConnections()

        vertQueue = queue.Queue()
        vertQueue.put(start)
        while (not vertQueue.empty()):
            currentVert = vertQueue.get()
            for nbr in currentVert.getConnections():
                if (nbr.getColor() == 'white'):
                    nbr.setColor('gray')
                    if(nbr.isReconfigured()):
                        #print("Can be reconfigured")
                        return True
                    vertQueue.put(nbr)
            currentVert.setColor('black')
        return False

        # redistrib_table={
        #     key: frozenset(
        #         r for r in self.processors_table[key]['reloading'] if
        #         r not in modules_for_redistribute
        #     ) for key in modules_for_redistribute
        #     }
        # print(redistrib_table,modules_for_redistribute)
        #
        # # print(modules_for_redistribute)
        # # print(redistrib_table)
        #
        # current_load={
        #     key: self.processors_table[key]['nominal_load'] for key in redistrib_table.keys()
        #     }
        # alternatives={}
        # #print(redistrib_table)
        # for k in redistrib_table.keys():
        #     alternatives[k]=redistrib_table[k]
        #     for l in redistrib_table.keys():
        #         if(k!=l):
        #             alternatives[k]-=redistrib_table[l]
        #
        # # print(current_load)
        #
        # #print(modules_for_redistribute)
        # #print(alternatives)
        # for key in redistrib_table.keys():
        #     for target in alternatives[key]:
        #         current_load[key] -= min(
        #             self.processors_table[target]['max_load'] - self.processors_table[target]['nominal_load'],
        #             self.processors_table[key]['reloading'][target])
        #
        # if all(current_load[key] <= 0 for key in current_load.keys()):
        #     return True
        # #print(modules_for_redistribute)
        # for key in modules_for_redistribute:
        #         if current_load[key] <= 0:
        #             current_load.pop(key, None)
        #             redistrib_table.pop(key, None)
        #
        #
        # if len(current_load) <= 1:
        #     return True
        #
        #     current_possibilities = {}
        #     for key in self.processors_table.keys():
        #         if key not in modules_for_redistribute:
        #             current_possibilities[key] = self.processors_table[key]['max_load'] - self.processors_table[key]['nominal_load']
        #     for key in current_possibilities.keys():
        #         found = False
        #         for failed in current_load.keys():
        #             for target in redistrib_table[failed]:
        #                 if target == key:
        #                     found = True
        #         if not found:
        #             current_possibilities.pop(key, None)
        #     if sum(current_load.values()) > sum(current_possibilities.values()):
        #         return False
        #     return True

