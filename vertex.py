import copy

class Vertex:
    def __init__(self, redistrib_table, modules_for_redistribute,current_loading,max_loading):
        self.redistrib_table=redistrib_table
        self.color='white'
        self.modules_for_redistribute=modules_for_redistribute
        self.current_loading=current_loading
        self.max_loading=max_loading
        self.connections=[]
        #print("New vertex was created ",redistrib_table, modules_for_redistribute, current_loading, max_loading,"\r\n")

    def isReconfigured(self):
        return len(self.modules_for_redistribute)==0

    def getColor(self):
        return self.color

    def setColor(self,color):
        self.color=color

    def setConnections(self,connections):
        self.connections=connections

    def addConnection(self,elem):
        self.connections.append(elem)

    def getConnections(self):
        return self.connections