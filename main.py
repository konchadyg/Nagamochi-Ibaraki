#####################################
#CS 6385.001 | PROJECT-2            #
#Author: Konchady Gaurav Shenoy     #
#NETID: kxs168430                   #
#####################################

import sys
import random
import networkx as nx
import matplotlib.pyplot as plt

N=19
NUMOFGRAPHS=5

##########
#Functions
##########

#Generate the number of edges between 20 and 168, in steps of 4.
def edge_gen():
	edgeval = random.randint(20,168)
	#print "Edgeval: "+str(edgeval)
	
	if edgeval > 148:
		edgeval = edgeval - 20 #To keep the series of 5 within 20-168 range
	
	#print ">>Edgeval: "+str(edgeval)
	return edgeval                               


def next_node(nagamochimatrix, slist, total):
    adjedge = 0                                
    for i in range(total):
        if(i in slist):
            continue                           
        edj = 0
        for j in slist:                     
            edj += nagamochimatrix[i][j]
        
		if (edj>=adjedge):                    
            nxt_node = i
			adjedge= edj
    return nxt_node                             


def MA_Order_Get(nagamochimatrix, total):
    choosenode = random.randint(0,total-1)        
    ma_order = [choosenode]                     
    while(len(ma_order) <total):                 
        ma_order.append(next_node(nagamochimatrix,ma_order,total)) 
    return ma_order                             

def node_degree(nagamochimatrix, n):
    return sum(nagamochimatrix[n])                   



def Node_Merge(src,s,t):
    src[s][t]= src[t][s]= 0             
    newlength = len(src)-1                    
    newsrc = [[0 for i in range(newlength)] for j in range(newlength)]
    p=0
    for i in range(newlength+1):
        q=0
        flag=0
        for j in range(0,i+1):
            if(i==max(s,t)):                   
                flag=1
                break
            if(i==min(s,t)):                    
                newsrc[p][q] = newsrc[q][p] = src[min(s,t)][j]+src[max(s,t)][j]
            else:                               
                if(j!=s and j!=t):
                    newsrc[p][q] = newsrc[q][p] = src[i][j]
                else:
                    if(j==max(s,t)):
                        continue
                    newsrc[p][q] = newsrc[q][p] = src[i][s]+src[i][t]
            if(p==q):
                newsrc[p][q]=0
            q+=1
        if(flag==0):
            p+=1    
    return newsrc
                

def nagamochi(nagamochimatrix, nodecount):
    if(nodecount==2):                                
        return node_degree(nagamochimatrix,0)      
    maorder = MA_Order_Get(nagamochimatrix,nodecount)  
        
    last_ind = len(maorder) - 1
    
    lambdag = node_degree(nagamochimatrix,maorder[last_ind])
    
    nagamochimatrix=Node_Merge(nagamochimatrix,maorder[last_ind],maorder[last_ind-1]) 
    return (min(lambdag,nagamochi(nagamochimatrix, nodecount-1))) 

def GraphGen(n, maxedges):
    global adj
    edjcnt = 0                                     
    while(edjcnt<maxedges):                        
        for i in range(n):                      
            for j in range(n):
                if (i == j):                    
                    adj[i][j] = adj[j][i] = 0
                else:
                    x = random.randint(0,1)    
                    if (x == 1):                
                        adj[i][j] = adj[j][i] = adj[i][j]+1
                        edjcnt+=x                  
                        if (edjcnt >= maxedges):  
                            break
            if (edjcnt >= maxedges):
                break

##########
#Main Fxn#
##########

if __name__ == '__main__':
	print "Number of Nodes (Fixed): "+str(N)
	edgeval = edge_gen()
	print "Edge Val chosen: "+str(edgeval)+"\n"
	print("No. OF EDGES\tDEGREE\tLAMBDA")
	print("============\t======\t======")
	graphlist=[[[0 for i in range(N)] for j in range(N)] for k in range(5)]
	Total_lambda=0
	for m in range(0,NUMOFGRAPHS): 
		edges=4*m+edgeval
		#print 4*m
		adj=[[0 for i in range(N)] for j in range(N)]
		di = 2*edges/N
		GraphGen(N,edges)
		l = nagamochi(adj, N)
		Total_lambda+=l
		print(str(edges)+"\t\t"+str(di)+"\t"+str(l)+"\t")
		graphlist[m]=adj
		
	lambdaavg = Total_lambda/float(NUMOFGRAPHS)	
	print("======================================")
	print "Average Lamda: "+str(lambdaavg)
	print("======================================")
	
	################
	#Plot The Graph#
	################
	for k in range (0,NUMOFGRAPHS):
		nodemat = graphlist[k]
		G=nx.Graph()
		#G=nx.DiGraph()
		for i in range(0,N):
			G.add_node(i)
	
		for i in range(0,N):
			for j in range(0,N):
				#print '',
				no_of_edges= nodemat[i][j]
				if no_of_edges > 0:
					for p in range(0,no_of_edges):
						G.add_edge(i,j,length =p+1)
						
		#pos = nx.spring_layout(G)
		#edge_labels=dict([((u,v,),d['length'])
		#	for u,v,d in G.edges(data=True)])
		fig=plt.figure(0)
		fig.canvas.set_window_title('Figure '+str(k+1)+' -- '+str(4*k+edgeval)+' edges')
		nx.draw(G,with_labels = True)
		#nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3, font_size=7)
		plt.show()
		'''
	for i in range(0,5):
		print "\nGraph"+str(i+1)+":" 
		print graphlist[i]
	nx.draw(G,with_labels = True)
	plt.show()	'''
		