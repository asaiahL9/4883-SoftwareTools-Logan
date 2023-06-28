import graphviz 
from graphviz import Digraph
import csv 
import json
from json import load, loads, dump, dumps
from rich import print
import random

count = 0

def search(key, list, current_person):
  before = current_person.split()[3]
  gender = current_person.split()[2]
  for item in list:
    if key == int(item.split()[0]) and gender == 'F':
      current_person.split()[3] = item.split()[3]
      print('Switch = ' + before + " -> " + item.split()[3])
      return item.split()[3] 

    else:
      return None

dot = Digraph('G', filename='tree.dot')
dot.attr('node', shape='record')
gens = []
person_list = []
i = 0
j=0
k = 0


with open('firstnames.csv', newline='\n') as f:
    reader = csv.DictReader(f)
    for col in reader:

        cid = col['pid']
        cname = col['name']
        cgender = col['gender']
        cgen = col['generation']
        cbirth_year = col['byear']
        cdeath_year = col['dyear']
        cdeath_age = col['dage']
        cmyear = col['myear']
        cmage = col['mage']
        cpersonality = col['ptype']
        cclanID = col['clan']
        cfirstname = col['firstname']
        if col['spouseId'] == '':
          cspouseID = 'NULL'
        else:
          cspouseID = col['spouseId']
        if col['parentId1'] == '':
          cparent1 = 'NULL'
        else:
          cparent1 = col['parentId1']
        if col['parentId2'] == '':
          cparent2 = 'NULL'
        else:
          cparent2 = col['parentId2']
        cparentNode = col['parentNodeId']
        i = i + 1
        personInfo = cid + " " + cname + " " + cgender + " " + cclanID + " " + cgen + " " + cspouseID + " " + cparent1+ " " + cparent2 + " " + cfirstname + " " + cbirth_year+ " " +cdeath_year+ " " +cdeath_age+ " " +cmyear
        person_list.append(personInfo)

        
        # NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
#       so that Graphviz recognizes it as a special cluster subgraph
with dot.subgraph(name='cluster_0') as c:

    for item in person_list:
      # print(item)
      id = item.split()[0]
      lname = item.split()[1]
      gender = item.split()[2]
      clanID = item.split()[3]
      gen = item.split()[4]
      spouseID = item.split()[5]
      parent1 = item.split()[6]
      parent2 = item.split()[7]
      firstname = item.split()[8]
      birth_year = item.split()[9]
      death_year=item.split()[10]
      death_age=item.split()[11]
      if int(clanID) == 0:
          if int(gen) == 0:
            c.attr(rank='max')
          else:
            c.attr(rank='source')
          if spouseID == 'NULL':
            spouseID = None
          else:
            newClan = search(int(spouseID), person_list, item)
            # print(newClan)
            if newClan:
              newstr= id + " " + lname + " " + gender + " " + newClan + " " + gen + " " + spouseID + " " + parent1+ " " + parent2 + " " + firstname+ " " + birth_year+ " " +death_year+ " " +death_age+ " " + birth_year+ " " +death_year+ " " +death_age
              print('here')
              person_list[count] = newstr
            if gender == 'F':
              c.node(id,lname, color='deeppink')
            else:
              c.node(id,lname, color='dodgerblue')

            c.node(id, firstname + " "  + lname + '\n' + gen + '\n' + birth_year + ' - ' + death_year)
              
   
          c.node(id, firstname + " "  + lname)
  

          if parent1 == 'NULL':
            parent1 = None
          else:
              c.edge(parent1, id) 
          if parent2 == 'NULL':
            parent2 = None
          else:
            c.edge(parent2, id)
          
  
          c.node(id, firstname + " "  + lname + ' ' + birth_year + ' - ' + death_year)

with dot.subgraph(name='cluster_1') as c:

    for item in person_list:
      id = item.split()[0]
      lname = item.split()[1]
      gender = item.split()[2]
      clanID = item.split()[3]
      gen = item.split()[4]
      spouseID = item.split()[5]
      parent1 = item.split()[6]
      parent2 = item.split()[7]
      firstname = item.split()[8]
      birth_year = item.split()[9]
      death_year=item.split()[10]
      death_age=item.split()[11]
      if int(clanID) == 1:
          if int(gen) == 0:
            c.attr(rank='max')
          else:
            c.attr(rank='source')
          if spouseID == 'NULL':
            spouseID = None
          else:
            # print(item)
            count = count + 1
            newClan = search(int(spouseID), person_list, item)
            print(newClan)
            if newClan:
              newstr= id + " " + lname + " " + gender + " " + newClan + " " + gen + " " + spouseID + " " + parent1+ " " + parent2 + " " + firstname+ " " + birth_year+ " " +death_year+ " " +death_age
              print('here')
              person_list[count] = newstr
            if gender == 'F':
              c.node(id,lname, color='deeppink')
            else:
              c.node(id,lname, color='dodgerblue')

            c.edge(id, spouseID)
            
          c.node(id, lname)
          if parent1 == 'NULL':
            parent1 = None
          else:
              c.edge(parent1, id) 
          if parent2 == 'NULL':
            parent2 = None
          else:
            c.edge(parent2, id)  
          c.node(id, firstname + " "  + lname + ' ' + birth_year + ' - ' + death_year)
    
    print(count)
with dot.subgraph(name='cluster_2') as c:

    for item in person_list:
      id = item.split()[0]
      lname = item.split()[1]
      gender = item.split()[2]
      clanID = item.split()[3]
      gen = item.split()[4]
      spouseID = item.split()[5]
      parent1 = item.split()[6]
      parent2 = item.split()[7]
      firstname = item.split()[8]
      birth_year = item.split()[9]
      death_year=item.split()[10]
      death_age=item.split()[11]
      if int(clanID) == 2:
          if int(gen) == 0:
            c.attr(rank='max')
          else:
            c.attr(rank='source')
          if spouseID == 'NULL':
            spouseID = None
          else:
            newClan = search(int(spouseID), person_list, item)
            print(newClan)
            if newClan:
              newstr= id + " " + lname + " " + gender + " " + newClan + " " + gen + " " + spouseID + " " + parent1+ " " + parent2 + " " + firstname+ " " + birth_year+ " " +death_year+ " " +death_age
              print('here')
              # print(item.split()[3])
              person_list[count] = newstr
            if gender == 'F':
              c.node(id,lname, color='deeppink')
            else:
              c.node(id,lname, color='dodgerblue')
            # c.attr(rank='max')
            c.edge(id, spouseID)
          
          if parent1 == 'NULL':
            parent1 = None
          else:
              c.edge(parent1, id) 
          if parent2 == 'NULL':
            parent2 = None
          else:
            c.edge(parent2, id)
          
  
          c.node(id, firstname + " "  + lname + ' ' + birth_year + ' - ' + death_year)

with dot.subgraph(name='cluster_3') as c:

    for item in person_list:
      id = item.split()[0]
      lname = item.split()[1]
      gender = item.split()[2]
      clanID = item.split()[3]
      gen = item.split()[4]
      spouseID = item.split()[5]
      parent1 = item.split()[6]
      parent2 = item.split()[7]
      firstname = item.split()[8]
      birth_year = item.split()[9]
      death_year=item.split()[10]
      death_age=item.split()[11]

      if int(clanID) == 3:
          if int(gen) == 0:
            c.attr(rank='max')
          else:
            c.attr(rank='source')
          if spouseID == 'NULL':
            spouseID = None
          else:
            newClan = search(int(spouseID), person_list, item)
            print(newClan)
            if newClan:
              newstr= id + " " + lname + " " + gender + " " + newClan + " " + gen + " " + spouseID + " " + parent1+ " " + parent2 + " " + firstname+ " " + birth_year+ " " +death_year+ " " +death_age
              print('here')
              person_list[count] = newstr
            if gender == 'F':
              c.node(id,lname, color='deeppink')
            else:
              c.node(id,lname, color='dodgerblue')
            c.edge(id, spouseID)
            
          
          if parent1 == 'NULL':
            parent1 = None
          else:
              c.edge(parent1, id) 
          if parent2 == 'NULL':
            parent2 = None
          else:
            c.edge(parent2, id)
          
  
          c.node(id, firstname + " "  + lname + ' ' + birth_year + ' - ' + death_year)

with dot.subgraph(name='cluster_4') as c:
    for item in person_list:
      # print(item)
      id = item.split()[0]
      lname = item.split()[1]
      gender = item.split()[2]
      clanID = item.split()[3]
      gen = item.split()[4]
      spouseID = item.split()[5]
      parent1 = item.split()[6]
      parent2 = item.split()[7]
      firstname = item.split()[8]
      birth_year = item.split()[9]
      death_year=item.split()[10]
      death_age=item.split()[11]

      if int(clanID) == 4:
          if int(gen) == 0:
            c.attr(rank='max')
          else:
            c.attr(rank='source')
          if spouseID == 'NULL':
            spouseID = None
          else:
            newClan = search(int(spouseID), person_list, item)
            print(newClan)
            if newClan:
              newstr= id + " " + lname + " " + gender + " " + newClan + " " + gen + " " + spouseID + " " + parent1+ " " + parent2 + " " + firstname+ " " + birth_year+ " " +death_year+ " " +death_age
              print('here')
              person_list[count] = newstr
            if gender == 'F':
              c.node(id,lname, color='deeppink')
            else:
              c.node(id,lname, color='dodgerblue')

            c.edge(id, spouseID)
            c.node(id, firstname + " "  + lname + '\n' + gen + '\n' + birth_year + ' - ' + death_year)
              
          if parent1 == 'NULL':
            parent1 = None
          else:
              c.edge(parent1, id) 
          if parent2 == 'NULL':
            parent2 = None
          else:
            c.edge(parent2, id)
          
  
          c.node(id, firstname + " "  + lname + ' ' + birth_year + ' - ' + death_year)

with dot.subgraph(name='cluster_5') as c:

    for item in person_list:
      id = item.split()[0]
      lname = item.split()[1]
      gender = item.split()[2]
      clanID = item.split()[3]
      gen = item.split()[4]
      spouseID = item.split()[5]
      parent1 = item.split()[6]
      parent2 = item.split()[7]
      firstname = item.split()[8]
      birth_year = item.split()[9]
      death_year=item.split()[10]
      death_age=item.split()[11]

      if int(clanID) == 5:
          if int(gen) == 0:
            dot.attr(rank='max')
          else:
            c.attr(rank='source')
          if spouseID == 'NULL':
            spouseID = None
          else:
            newClan = search(int(spouseID), person_list, item)
            print(newClan)
            if newClan:
              newstr= id + " " + lname + " " + gender + " " + newClan + " " + gen + " " + spouseID + " " + parent1+ " " + parent2 + " " + firstname+ " " + birth_year+ " " +death_year+ " " +death_age
              print('here')
              person_list[count] = newstr
            if gender == 'F':
              c.node(id,lname, color='deeppink')
            else:
              c.node(id,lname, color='dodgerblue')
            # c.attr(rank='max')
            c.edge(id, spouseID)
          
          if parent1 == 'NULL':
            parent1 = None
          else:
              c.edge(parent1, id) 
          if parent2 == 'NULL':
            parent2 = None
          else:
            c.edge(parent2, id)
          
  
          c.node(id, firstname + " "  + lname + ' ' + birth_year + ' - ' + death_year)
with open('tree.dot','w') as f:
    f.write(dot.source)