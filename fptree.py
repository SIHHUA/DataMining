import time
import pandas as pd

#讀檔
def Load_data(filename):
    with open(filename) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    Transaction = []

    for i in range(0, len(content)):
        Transaction.append(content[i].split())

    return Transaction

#轉換成frozenset，以利hash
def create_initialset(dataset):
    retDict = {}
    for trans in dataset:
        retDict[frozenset(trans)] = 1
    return retDict

class TreeNode:
    def __init__(self, Node_name,counter,parentNode):
        self.name = Node_name
        self.count = counter
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
        
    def increment_counter(self, counter):
        self.count += counter

#建立Tree
def create_FPTree(dataset, minSupport):
    HeaderTable = {}
    for transaction in dataset:
        for item in transaction:
            HeaderTable[item] = HeaderTable.get(item,0) + dataset[transaction]
    for k in list(HeaderTable):
        if HeaderTable[k] < minSupport:
            del(HeaderTable[k])

    frequent_itemset = set(HeaderTable.keys())

    if len(frequent_itemset) == 0:
        return None, None

    for k in HeaderTable:
        HeaderTable[k] = [HeaderTable[k], None]

    retTree = TreeNode('Null Set',1,None)
    for itemset,count in dataset.items():
        frequent_transaction = {}
        for item in itemset:
            if item in frequent_itemset:
                frequent_transaction[item] = HeaderTable[item][0]
        if len(frequent_transaction) > 0:
            #取得排序
            ordered_itemset = [v[0] for v in sorted(frequent_transaction.items(), key=lambda p: p[1], reverse=True)]
            #更新Tree
            updateTree(ordered_itemset, retTree, HeaderTable, count)
    return retTree, HeaderTable

#更新Tree，照著sort過的資料
def updateTree(itemset, FPTree, HeaderTable, count):
    if itemset[0] in FPTree.children:
        FPTree.children[itemset[0]].increment_counter(count)
    else:
        FPTree.children[itemset[0]] = TreeNode(itemset[0], count, FPTree)

        if HeaderTable[itemset[0]][1] == None:
            HeaderTable[itemset[0]][1] = FPTree.children[itemset[0]]
        else:
            update_NodeLink(HeaderTable[itemset[0]][1], FPTree.children[itemset[0]])

    if len(itemset) > 1:
        updateTree(itemset[1::], FPTree.children[itemset[0]], HeaderTable, count)

#更新Tree連結
def update_NodeLink(Test_Node, Target_Node):
    while (Test_Node.nodeLink != None):
        Test_Node = Test_Node.nodeLink

    Test_Node.nodeLink = Target_Node

#找樹枝
def FPTree_uptransveral(leaf_Node, prefixPath):
 if leaf_Node.parent != None:
    prefixPath.append(leaf_Node.name)
    FPTree_uptransveral(leaf_Node.parent, prefixPath)

#找conditional Pattern
def find_prefix_path(basePat, TreeNode):
 Conditional_patterns_base = {}

 while TreeNode != None:
    prefixPath = []
    FPTree_uptransveral(TreeNode, prefixPath)
    if len(prefixPath) > 1:
        Conditional_patterns_base[frozenset(prefixPath[1:])] = TreeNode.count
    TreeNode = TreeNode.nodeLink

 return Conditional_patterns_base

#利用conditional patterns base 、conditional FP tree進行遞迴找frequent pattern
def Mine_Tree(FPTree, HeaderTable, minSupport, prefix, frequent_itemset):
    bigL = [v[0] for v in sorted(HeaderTable.items(),key=lambda p: p[1][0])]
    for basePat in bigL:
        new_frequentset = prefix.copy()
        new_frequentset.add(basePat)
        #新增frequent itemsets
        frequent_itemset.append(new_frequentset)
        #所有conditional pattern bases
        Conditional_pattern_bases = find_prefix_path(basePat, HeaderTable[basePat][1])
        #建立conditional FP Tree
        Conditional_FPTree, Conditional_header = create_FPTree(Conditional_pattern_bases,minSupport)

        if Conditional_header != None:
            Mine_Tree(Conditional_FPTree, Conditional_header, minSupport, new_frequentset, frequent_itemset)

df = pd.read_csv('dataset.csv')
data = []
for i in df.values:
    tmp = []
    for j in range(len(i)):
        if i[j] != '?':
            tmp.append(j+1)
    data.append(tmp)

File = open('data','w')
for i in range(len(data)):
    str1 = ""
    for j in range(len(data[i])):
        if str1 == "":
            str1 = str(data[i][j])
        else:
            str1 = str1+" "+str(data[i][j])
    str1 = str1 + "\n"
    File.write(str1)

File.close()

min_Support= 30
initSet = create_initialset(Load_data('data'))
start = time.time()
FPtree, HeaderTable = create_FPTree(initSet, min_Support)

frequent_itemset = []
Mine_Tree(FPtree, HeaderTable, min_Support, set([]), frequent_itemset)
end = time.time()

print("Time Taken is:")
print(end-start)
print("All frequent itemsets:")
print(len(frequent_itemset))
print(frequent_itemset)