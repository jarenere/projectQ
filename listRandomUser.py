import random
class list_random:

    def __init__(self, n):
        self.n=n
        self.count=n/2
        self.l_tuple=[]
        for i in range(n):
            for j in range(i+1,n):
                self.l_tuple.append([i,j,0])
                # 0 no usado
                # 1 invalido
                # 2 usado

    def _valido(self,i,lista):
        if self.l_tuple[i][2]==0:
            for j in lista:
                if (j[0]==self.l_tuple[i][0] or\
                    j[0]==self.l_tuple[i][1] or\
                    j[1]==self.l_tuple[i][0] or\
                    j[1]==self.l_tuple[i][1]): 
                    self.l_tuple[i][2]==1
                    return False
            self.l_tuple[i][2]==2
            lista.append((self.l_tuple[i][0],self.l_tuple[i][1]))
            return True
        return False

    def list1(self):
        lista=[]
        k = self.count
        while (k>0):
            i = random.randrange(len(self.l_tuple))
            if self._valido(i,lista):
                pass
            else:
                last = len(self.l_tuple)-1
                for j in range(len(self.l_tuple)):
                    if self._valido((i+j+1) % len(self.l_tuple),lista):
                        break
                    if j == last:
                        # no encontrada solucion
                        raise "solucion no encontrada"
            k=k-1
            print "UNO MENOS", k
        return lista


