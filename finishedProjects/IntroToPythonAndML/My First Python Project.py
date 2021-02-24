#!/usr/bin/env python
# coding: utf-8

# # Python Data Structures

# ### Tuples: Immutable, multi-type, ordered/indexed data

# In[16]:


tuple1 = (1, "two", 3.5, False)
tuple1[2] = 4


# ### Lists: mutable, multi-type, ordered/indexed data

# In[8]:


list1 = [1,"two",3.5,False]
list1[2] = 4
print(list1)


# ### Dictionaries: Unordered, immutably string-keyed set, mutably valued data

# In[10]:


dictionary1 = {'leader': 'Abraham Lincoln', 'fighter': 'Mike Tyson', 'city': "Toronto"}
dictionary1['leader'] = 'Winston Churchill'
print(dictionary1)


# ### Sets: mutable, unordered, unique elements (no duplicates)

# In[11]:


set1 = {1, "two", 3.5, 3.5, False}
print(set1)
set1.add('twenty')
print(set1)
set1.remove("two")
print(set1)


# In[12]:


set2 = {'hello', 1, 3.5, 'I', 'new'}
set2&set1


# In[13]:


set1.union(set2)


# ### Custom Objects: Standard OOP (for now)

# In[14]:


#custom class Human
class Human(object ):
    def __init__(self, height, weight):
        self.height = height;
        self.weight = weight;


# In[15]:


#initializing a Human Custom Class Object
newHuman = Human(60,180)
print(newHuman.height)
print(newHuman.weight)


# # Traversing Basic Data Structures

# ### If-Then-Else Statements: conditional structures

# In[19]:


wizard = 'Sauron'
elf = "Frodo"
helpComing = True

if(wizard == 'Sauron') and (elf == "Frodo"):
    print("Danger!")
elif (helpComing):
    print("Keep going!")
else:
    print("Oh no. End of the World")


# ### Loops: for and while, conditional structures with more oomfph

# In[20]:


list1 = [1,3,5,7,9]
for i,list in enumerate(list1): #here i is the index, list is the value at i
    list1[i] = list+1
print(list1)


# In[21]:


set1 = {'one','two','three','four'}
for item in set1:
    print(item + ' mississippi')


# In[27]:


i = 0
metals = ['silver', 'copper', 'iron', 'gold', 'tin', 'aluminum']
while(metals[i] != 'gold'):
    print('you found ' + metals[i] + ', ' + metals[i] + ' is not gold.')
    i += 1
print("you've struck gold!")


# ### Functions: perform tasks given particular data structures 

# ##### Typically made in a generalized manner, utilized for possibly repeated tasks

# In[28]:


#defining a function "multiples"
def multiples (x, list1):
    for i,list in enumerate(list1):
        list1[i] = list*x
    return list1

#using the function "multiples"

list1 = [2,5,12,64]
multiples(4,list1)
print(list1)

