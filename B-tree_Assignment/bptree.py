import bisect
import math
import csv
import sys

class Node:
    def __init__(self, isleaf, nxt, parent, degree, file):
        self.key = []
        self.value = []
        self.isleaf = isleaf
        self.next = nxt
        self.parent = parent
        self.child = []
        self.degree = int(degree)
        self.file = file

    def insert(self, key, value, skip):
        while self.parent != None and skip == 0:#skip==1μΌλ μλ skip
            self = self.parent
        if self.isleaf == 1:
            #if key in self.key == False:
            index = bisect.bisect_left(self.key, key)
            self.key.insert(index, key)
            self.value.insert(index, value)
            if len(self.key) >= self.degree:
                mid = math.floor(self.degree/2)
                self.split(mid)
                self = self.parent
        else:
            index = bisect.bisect_left(self.key, key)
            self = self.child[index]
            self.insert(key, value, 1)

    def insertNode(self, key, child):
        index = bisect.bisect_left(self.key, key)
        self.key.insert(index, key)
        self.child.insert(index+1, child)
        if len(self.key) >= self.degree:
            mid = math.floor(self.degree/2)
            self.split(mid)
            
    def split(self, mid):
        if self.isleaf == 1:
            new = Node(1, self.next, self.parent, self.degree, file)
            new.key = self.key[mid:]
            new.value = self.value[mid:]
            self.key = self.key[:mid]
            self.value = self.value[:mid]
            self.next = new
            
            if self.parent == None:
                self.parent = Node(0, None, None, self.degree, file)
                self.parent.key.append(new.key[0])
                self.parent.child.append(self)
                self.parent.child.append(new)
                new.parent = self.parent
            else:
                self.parent.insertNode(new.key[0], new)
        else:
            new = Node(0, self.next, self.parent, self.degree, file)
            up = self.key[mid]
            new.key = self.key[mid+1:]
            new.child = self.child[mid+1:]
            i = 0
            while i < len(new.child):
                new.child[i].parent = new
                i = i + 1
            self.key = self.key[:mid]
            self.child = self.child[:mid+1]
            self.next = new
            
            if self.parent == None:
                self.parent = Node(0, None, None, self.degree, file)
                self.parent.key.append(up)
                self.parent.child.append(self)
                self.parent.child.append(new)
                new.parent = self.parent
            else:
                self.parent.insertNode(up, new)

    def read(self, line):
        with open(self.file, "r") as f:
            i = 1
            while i < line:
                skip = f.readline()
                i = i+1
            read_line = f.readline()#line λ²μ§Έ μ€ μ½κΈ°
            if not read_line:
                return
            read_line = read_line.rstrip("\n")
            if "leaf:" in read_line:
                read_line = read_line.lstrip("leaf:")
                read_line = read_line.rstrip()
                node = read_line.split(" -> ")
                save = self
                for i in node:
                    key = i.split(" ")
                    for k in key:
                        self.key.append(int(k))
                    if self.next != None:
                        self = self.next
                self = save
                self.read(line+1)

            elif "value:" in read_line:
                read_line = read_line.lstrip("value:")
                read_line = read_line.rstrip()
                node = read_line.split(" | ")
                for i in node:
                    value = i.split(" ")
                    for v in value:
                        self.value.append(int(v))
                    if self.next != None:
                        self = self.next

            else:
                read_line = read_line.rstrip(" / ")
                node = read_line.split(" / ")
                pre = None
                for i in node:
                    key = i.split(" ")
                    for k in key:
                        self.key.append(int(k))
                        new = Node(1, None, self, self.degree, self.file)
                        self.child.append(new)
                        if pre != None:
                            pre.next = new
                        pre = new
                    new = Node(1, None, self, self.degree, self.file)
                    self.child.append(new)#key κ°μ +1κ°λ§νΌ childλΈλ λ§λ€κΈ°
                    pre.next = new
                    pre = new
                    
                    self.isleaf = 0
                    if self.next != None:
                        self = self.next
                i = 0
                while self.parent != None:
                    self = self.parent
                    i = i+1
                while i > 0:
                    self = self.child[0]
                    i = i-1
                    
                self = self.child[0]
                self.read(line+1)
                        

    def write(self):
        index = open(self.file, "w")
        sys.stdout = index
        print("degree : " + degree)
        while self.parent != None:#rootκΉμ§ μ¬λΌκ°κΈ°
            self = self.parent
            
        while self.isleaf != 1:
            down = self.child[0]#λ΄λ €κ° μμμ 
            while self != None:
                for i in self.key:
                    print(str(i), end = " ")#ν λΈλμ μν ν€ μΆλ ₯
                print("/", end = " " )#'/' λ‘ λΈλ κ΅¬λ³
                self = self.next
            print("")#"\n"μΌλ‘ level κ΅¬λ³
            self = down
            
        #leafλΈλ μΆλ ₯
        start = self
        print("leaf:", end = "")
        while self != None:
            for k in self.key:
                print(str(k), end = " ")
            if self.next != None:
                print("->", end = " ")
            self = self.next
        print("")
        self = start
        print("value:", end = "")
        while self != None:
            for v in self.value:
                print(str(v), end = " ")
            if self.next != None:
                print("|", end = " ")
            self = self.next
        print("")


    def key_search(self, key, skip):
        while self.parent != None and skip == 0:#skip==1μΌλ μλμ€ skip
            self = self.parent
        if self.isleaf == 1:
            if key in self.key:
                index = bisect.bisect_left(self.key, key)
                print(str(self.value[index]))
            else:
                print("NOT FOUND")

        else:
            for i in self.key:
                if i == self.key[len(self.key)-1]:
                    print(str(i), end = "")
                else:
                    print(str(i), end = ",")
            print("")
            index = bisect.bisect_left(self.key, key)
            if index <= (len(self.key)-1) and self.key[index] == key:
                index = index + 1
            self = self.child[index]
            self.key_search(key, 1)

    def range_search(self, start, end):
        while self.parent != None:
            self = self.parent
        while self.isleaf != 1:
            self = self.child[0]

        while self != None:
            v = 0
            for i in self.key:
                if int(i) >= start and int(i) <= end:
                   print(str(i) + "," + str(self.value[v]))
                v = v+1
            self = self.next
        
    def delete(self, key):
        need_del = None
        left_sibiling = None
        while self.parent != None:
            self = self.parent
        while self.isleaf != 1:
            index = bisect.bisect_left(self.key, key)
            if index <= (len(self.key)-1) and self.key[index] == key:
                index = index + 1
                need_del = self#leaf μλ κ³³μλ keyκ° μλμ§ νμΈ
                del_index = index - 1
            if index > 0:
                left_sibiling = self.child[index-1]
            else:
                left_sibling = None
            self = self.child[index]
            p_index = index

        d_index = bisect.bisect_left(self.key, key)
        del(self.key[d_index])
        del(self.value[d_index])
        if need_del != None:
            need_del.key[del_index] = self.key[d_index]

        while True:
            if len(self.key) >= math.floor((self.degree-1)/2):#keyκ°μ μΆ©λΆν κ²½μ°
                break
            else:
                #μ€λ₯Έμͺ½μμ borrow
                if index < len(self.parent.key) and len(self.next.key) > math.floor((self.degree-1)/2):
                    b1 = self.parent.key[p_index]
                    self.key.append(b1)
                    if self.isleaf == 1:
                        self.value.append(self.next.value[0])
                        del(self.next.value[0])
                        del(self.next.key[0])
                        self.parent.key[p_index] = self.next.key[0]
                    else:
                        self.child.append(self.next.child[0])
                        self.next.child[0].parent = self
                        self.parent.key[p_index] = self.next.key[0]
                        del(self.next.key[0])
                        del(self.next.child[0])
                    break

                #μΌμͺ½μμ borrow
                elif left_sibiling != None and len(left_sibiling.key) > math.floor((self.degree-1)/2):
                    s_index = len(left_sibiling.key)-1
                    if self.isleaf == 1:
                        self.key.insert(0, left_sibiling.key[s_index])
                        self.value.insert(0, left_sibiling.value[s_index])
                        del(left_sibiling.key[s_index])
                        del(left_sibiling.value[s_index])
                        self.parent.key[p_index-1] = self.key[0]
                    else:
                        b1 = self.parent.key[p_index-1]
                        self.key.insert(0, b1)
                        self.child.insert(0, left_sibiling.child[s_index+1])
                        self.child[0].parent = self
                        self.parent.key[p_index-1] = left_sibiling.key[s_index]
                        del(left_sibiling.key[s_index])
                        del(left_sibiling.child[s_index+1])
                    break

                #merge
                else:                      
                    #μ€λ₯Έμͺ½ λΈλλ merge
                    if index < len(self.parent.key):
                        self.key = self.key + self.next.key
                        self.value = self.value + self.next.value
                        self.next.key = None
                        self.next.value = None
                        self.next = self.next.next
                        del(self.parent.key[p_index])
                        del(self.parent.child[p_index+1])

                    #μΌμͺ½ λΈλλ merge
                    else:
                        left_sibiling.key = left_sibiling.key + self.key
                        left_sibiling.value = left_sibiling.value + self.value
                        self.key = None
                        self.value = None
                        left_sibiling.next = self.next
                        del(self.parent.key[p_index-1])
                        del(self.parent.child[p_index])
                        
                    self = self.parent
                    if self.parent == None:
                        break
                    p_index = bisect.bisect_left(self.parent.key, self.key[0])
                    index = p_index
                    if p_index > 0:
                        left_sibiling = self.parent.child[p_index-1]
                    else:
                        left_sibiling = None

#νμΌ λ§λ€κΈ°
if(sys.argv[1] == "-c"):
    f = open(sys.argv[2], "w")
    degree = sys.argv[3]
    sys.stdout = f
    print("degree : " + degree)
    f.close()

#μ½μνκΈ°
elif(sys.argv[1] == "-i"):
    #κΈ°μ‘΄ index νμΌμμ degree μ½μ΄μ€κΈ°
    with open(sys.argv[2], "r") as f:
        degree_line = f.readline()
        degree = degree_line[9:]
    
    pair = {}
    with open(sys.argv[3], "r") as file:
        file_read = csv.reader(file)
        for line in file:
            pair_list = line.split(',')
            pair[int(pair_list[0])] = int(pair_list[1])

    root = Node(1, None, None, degree, sys.argv[2])
    root.read(3)#κΈ°μ‘΄ λΈλ μ½μ΄μ€κΈ°
    for key in pair:
        root.insert(key, pair[key], 0)
    root.write()

#μ­μ νκΈ°
elif(sys.argv[1] == "-d"):
    with open(sys.argv[2], "r") as f:
        degree_line = f.readline()
        degree = degree_line[9:]
    root = Node(1, None, None, degree, sys.argv[2])
    root.read(3)
    
    delete = []
    with open(sys.argv[3], "r") as file:
        file_read = csv.reader(file)
        for line in file:
            delete.append(int(line))
    for d in delete:
        root.delete(d)
    root.write()

#λ¨μΌ κ²μνκΈ°
elif(sys.argv[1] == "-s"):
    with open(sys.argv[2], "r") as f:
        degree_line = f.readline()
        degree = degree_line[9:]
    search_key = int(sys.argv[3])
    root = Node(1, None, None, degree, sys.argv[2])
    root.read(3)
    root.key_search(search_key, 0)#ν¨μλ΄λΆμμ μΆλ ₯
    
#λ²μ κ²μνκΈ°
elif sys.argv[1] == "-r":
    with open(sys.argv[2], "r") as f:
        degree_line = f.readline()
        degree = degree_line[9:]
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    root = Node(1, None, None, degree, sys.argv[2])
    root.read(3)
    root.range_search(start, end)#ν¨μλ΄λΆμμ μΆλ ₯
