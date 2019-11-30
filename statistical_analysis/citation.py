# -*- coding: utf-8 -*-
"""

@author: Shubham
"""

import matplotlib.pyplot as plt
import numpy as np
import re
import scholarly
import pandas as pd

def citation_money(input):
    '''
    This fuunction takes input as a cvs file and plots citation and money
    of department as bar graph
    :param:name
    :type: string containing the name with extension
    '''
    assert isinstance(input, str)
    dataset = pd.read_csv(input)
    x = pd.DataFrame(dataset)
    name = x['Instructor']
    unique = list(set(name))
    
    last = []
    first = []
    for i in range(0, len(unique)):
        my_string = unique[i]
        result = [x.strip() for x in my_string.split(',')]
        last.append(result[0])
        temp1 = result[1]
        temp2 = re.findall('[A-Z][^A-Z]*', temp1)
        first.append(temp2)
    
    #For extracting name in a particular format that can be used to scrape data from Google Scholar
    scholar = []
    for i in range(0, len(first)):
        if len(first[i])==1:
            scholar.append(first[i][0]+' ' +last[i])
        elif len(first[i])==2:
            scholar.append(first[i][0] +' '+ first[i][1][0] + ' ' +last[i])
    
    #Extracting the number of citation of  the professors whose data is available on google scholar        
    citation =  []
    for i in range(0,len(scholar)):
        try:
            author = next(scholarly.search_author(scholar[i]))
            author_dict = vars(author)
            citation.append(author_dict['citedby'])
        except StopIteration:
            citation.append(0)        
    total_citation = sum(citation)
    
    #Creating an array to take into account only those professor's pay whose citation data was available
    contributer = []
    for i in range(0,len(citation)):
        if citation[i]>0:
            contributer.append(1)
        else:
            contributer.append(0)
    
    #Calculating the pay of citation contributing professors        
    temp5 = list(x['GrossPay'])
    money = []
    for i in range(0,len(contributer)):
        if contributer[i]>0:
            temp5[i] = temp5[i].replace(',','')
            money.append(float(temp5[i]))        
    total_money = sum(money)
    
    #Plotting the sum of gross pay of professors whose citations are taken into account
    #along with the total citation of all the professors under a specific department.
    
    labels = ['MAE']
    x = np.arange(len(labels))  
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, total_money, width, label='Money')
    rects2 = ax.bar(x + width/2, total_citation, width, label='Citation')
    ax.set_ylabel('Number/ Dollars')
    ax.set_title('Money and Citation')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), 
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    return plt.show()
                
