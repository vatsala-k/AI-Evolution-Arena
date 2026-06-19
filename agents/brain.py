import numpy as np
class Brain:
    def __init__(self, input_size=4, hidden_size=8, output_size=2,genome=None):
        self.input_size=input_size
        self.hidden_size=hidden_size
        self.output_size=output_size

        self.genome_length=(input_size*hidden_size+hidden_size+hidden_size*output_size+output_size)
        if genome is not None:
            self.from_genome(genome)
        else:
            self.weights1=np.random.randn(input_size,hidden_size)*0.5
            self.bias1=np.random.randn(hidden_size)*0.1
            self.weights2=np.random.randn(hidden_size,output_size)*0.5
            self.bias2=np.random.randn(output_size)*0.1

    def relu(self,x):
        return np.maximum(0,x)
    
    def sigmoid(self,x):
        return 1/(1+np.exp(-x))
    
    def forward(self,inputs):
        inputs=np.array(inputs)
        hidden=self.relu(np.dot(inputs,self.weights1)+self.bias1)
        output=self.sigmoid(np.dot(hidden,self.weights2)+self.bias2)
        return output
    
    def to_genome(self):
        genome=np.concatenate([self.weights1.flatten(),self.bias1,self.weights2.flatten(),self.bias2])
        return genome
    
    def from_genome(self,genome):
        genome=np.array(genome)
        ind=0
        w1_size=self.input_size*self.hidden_size
        self.weights1=genome[ind:ind+w1_size].reshape(self.input_size,self.hidden_size)
        ind+=w1_size
        self.bias1=genome[ind:ind+self.hidden_size]
        ind+=self.hidden_size

        w2_size=self.hidden_size*self.output_size
        self.weights2=genome[ind:ind+w2_size].reshape(self.hidden_size,self.output_size)
        ind+=w2_size
        self.bias2=genome[ind:ind+self.output_size]


        

        
    