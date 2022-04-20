import numpy as np
class InfoTheory:
    def f(self,px):
        if(px == 0): return 0
        return px*np.log2(px)
    def rowEntropy(self,row):
        if(row.size == 1):
            p = row[0]
            return -self.f(p) - self.f(1 - p)
        return -sum(map(self.f, row))
        #match list(row):
        #    case [p]: return -self.f(p) - self.f(1 - p)
        #    case _:   return -sum(map(self.f, row))
    def Entropy(self, P):
        # Input P:
        #   Matrix (2-dim array): Each row is a probability
        #       distribution, calculate its entropy,
        # Row vector (1Xm matrix): The row is a probability
        #   distribution, calculate its entropy,
        # Column vector (nX1 matrix): Derive the binary entropy
        #   function for each entry,
        # Single value (1X1 matrix): Derive the binary entropy
        #   function
        # Output:
        #   array with entropies
        H = np.apply_along_axis(self.rowEntropy, 1, P)
        return H
    def MutualInformation(self,P):
        # Derive the mutual information I(X;Y)
        # Input P: P(X,Y)
        # Output: I(X;Y)
        Px = np.sum(P, axis=0)
        #print('Px = ' + str(Px))
        Py = np.sum(P, axis=1).transpose()
        #print('Py = ' + str(Py))
        Hx = self.rowEntropy(Px)
        #print('Hx = ' + str(Hx))
        Hy = self.rowEntropy(Py)
        #print('Hy = ' + str(Hy))
        Hxy = sum(self.Entropy(P))
        #print('Hxy = ' + str(Hxy))
        I = Hx + Hy - Hxy
        return I
if __name__=='__main__':
    IT = InfoTheory()
    #<Tests of your code when running from prompt>
    ### init
    IT = InfoTheory()
    ### 1st test
    P1 = np.transpose(np.array([np.arange(0.0,1.1,0.25)])) # column vector
    H1 = IT.Entropy(P1)
    print('H1 =',H1)
    ### 2nd test
    P2 = np.array([[0.3, 0.1, 0.3, 0.3],
                   [0.4, 0.3, 0.2, 0.1],
                   [0.8, 0.0, 0.2, 0.0]])
    H2 = IT.Entropy(P2)
    print('H2 =',H2)
    ### 3rd test
    P3 = np.array([[0,   3/4],
                   [1/8, 1/8]])
    I3 = IT.MutualInformation(P3)
    print('I3 =',I3)
    ### 4th test
    P4 = np.array([[1/12, 1/6, 1/3],
                   [1/4,  0,   1/6]])
    I4 = IT.MutualInformation(P4)
    print('I4 =',I4)

