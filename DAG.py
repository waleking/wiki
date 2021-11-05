class Graph:
    def __init__(self):
        self.graph = {}
        with open("./taxonomy.csv", "r") as f:
            num = 0
            for line in f:
                num += 1
                source, target = line.strip().split("\t")
                if(source in self.graph):
                    self.graph[source].append(target)
                else:
                    self.graph[source] = [target]
            print("The graph is initialized.")
            print("The number of edges is %s" % num)

        self.root = "Main_topic_classifications"
        self.dag_file_name = "./DAG.csv"
        self.edge_num = num


    def build_DAG(self):
        f = open(self.dag_file_name, "w")
        # The category's level info will be updated 
        # in the BFS travesal. 
        category_level_dict = {}

        # It's BFS travesal of the graph, plus maintain 
        # the level as an additioanl info. 
        # So we need current_level_queue, and next_level_queue
        # at the same time. Only if the current_level_queue is
        # empty, the level will increment.
        level = 0
        current_level_queue = [self.root]
        next_level_queue = []

        visited_edges = set()
        while(len(current_level_queue)>0 or len(next_level_queue)>0):
            current_category = current_level_queue.pop(0)
            if(len(visited_edges)//1000 % 10) == 0:
                print("\r%s/%s edges are visited." % \
                        (len(visited_edges), self.edge_num), \
                        end='', flush=True)

            # Set the current node's level 
            category_level_dict[current_category] = level

            if current_category in self.graph:
                for neighbor in self.graph[current_category]:
                   # Check if the node will be point to upper-level node.
                   # If so, we do not output the edge into the final DAG, 
                   # because the "cross" edge "may" cause a cycle. 
                   if neighbor in category_level_dict \
                           and category_level_dict[neighbor] < level: 
                       # print("The edge [%s, %s] is deleted" \
                       #        % (current_category, neighbor))
                       pass
                   else:
                       try:
                           edge = "%s\t%s" % (current_category, neighbor)
                           if(edge not in visited_edges):
                               f.write(edge)
                               visited_edges.add(edge)
                               next_level_queue.append(neighbor)
                       except Exception as e:
                           print(e)

            if(len(current_level_queue)==0):
               current_level_queue = next_level_queue
               next_level_queue = []
               level += 1
               # print(level)


g = Graph()
g.build_DAG()
