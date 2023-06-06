## Assignment 3

Use Graphviz to create a binary search tree using dot language/engine

![bst](https://raw.githubusercontent.com/asaiahL9/4883-SoftwareTools-Logan/2f2e4d1350f9c221f89f038bd8a6c8a79bdfd9de/Assignments/A03/graphviz.svg)

```
digraph linkedlist {  
  node [shape=record]
  edge[arrowhead=vee, arrowtail=dot, color=black, tailclip=true];
  
  A[label="<LEFT> | <DATA> 10 | <RIGHT>"];
  B[label="<LEFT> | <DATA> 8 | <RIGHT>"];
  C[label="<LEFT> | <DATA> 15 | <RIGHT>"];
  D[label="<LEFT> | <DATA> 4 | <RIGHT>"];
  E[label="<LEFT> | <DATA> 9 | <RIGHT>"];
  F[label="<LEFT> | <DATA> 11 | <RIGHT>"];
  G[label="<LEFT> | <DATA> 17 | <RIGHT>"];
  
  
  A:LEFT->B:DATA
  A:RIGHT->C:DATA
  B:LEFT->D:DATA
  B:RIGHT->E:DATA
  C:LEFT->F:DATA
  C:RIGHT->G:DATA
}
```

|   #   | File | Description |
| :---: | ----------- | ----------|
|  1 | [binarysearchtree.dot](https://github.com/asaiahL9/4883-SoftwareTools-Logan/blob/main/Assignments/A03/binarysearchtree.dot)|Implementation|  
|2| [Binary Search Tree](https://github.com/asaiahL9/4883-SoftwareTools-Logan/blob/main/Assignments/A03/graphviz.svg)|Graphic Representation| 
