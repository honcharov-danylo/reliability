import  vertex
import copy

class Graph:
    def __init__(self,start):
        self.vertexs=set()
        #tuple_table = tuple(tuple((x,tuple(start.redistrib_table[x])) for x in start.redistrib_table.keys()))
        #for t in tuple_table:
        #    print(type(t),t)
        #tuple_modules = tuple(start.modules_for_redistribute)
        #tuple_loading = tuple(start.current_loading)
        #self.vertexs=set(((tuple_table,tuple_modules,tuple_loading)))
        self.buildConnections(start)

    def buildConnections(self,start):
            #self.connections = []
            for module in start.modules_for_redistribute:
                for iter in range(len(start.redistrib_table[module])):
                    if module != iter:
                        if ((start.redistrib_table[module][iter] + start.current_loading[iter]) <= start.max_loading[
                            iter]):
                            new_current_loading = copy.deepcopy(start.current_loading)
                            new_current_loading[iter] += start.redistrib_table[module][iter]
                            new_current_loading[module] -= start.redistrib_table[module][iter]
                            # new_redistrib_table = self.redistrib_table.copy()
                            new_redistrib_table = copy.deepcopy(start.redistrib_table)
                            new_redistrib_table[module][iter] = 0
                            new_modules_for_redistribute = copy.deepcopy(start.modules_for_redistribute)
                            if (new_current_loading[module] <= 0):
                                new_modules_for_redistribute.remove(module)
                            #print(new_redistrib_table, new_modules_for_redistribute, new_current_loading,
                             #     start.max_loading)
                            # input()
                            v = vertex.Vertex(new_redistrib_table, new_modules_for_redistribute, new_current_loading,
                                       start.max_loading)
                            tuple_table = tuple(tuple((x,tuple(start.redistrib_table[x])) for x in start.redistrib_table.keys()))
                            tuple_modules=tuple(new_modules_for_redistribute)
                            tuple_loading=tuple(new_current_loading)
                            oldsize=len(self.vertexs)
                            self.vertexs.add((tuple_table,tuple_modules,tuple_loading))
                            if(oldsize!=len(self.vertexs)):
                                self.buildConnections(v)
                                #self.vertexs.add((tuple_table,tuple_modules,tuple_loading))
                                start.addConnection(v)
                                #print(self.vertexs)

                            #self.connections.append(v)