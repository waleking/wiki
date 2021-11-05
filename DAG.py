class Graph:
    def __init__(self):
        self.graph = {}
        with open("./category_edges.csv", "r") as f:
            num = 0
            for line in f:
                if(num==0):
                    # Skip the csv head
                    num += 1
                    continue
                source, target = line.strip().split("\t")
                if(source in self.graph):
                    self.graph[source].append(target)
                else:
                    self.graph[source] = [target]
                num += 1
            print("The graph is initialized.")

        self.root = "Main_topic_classifications"
        self.dag_file_name = "./DAG.csv"
        self.edge_num = num


    def build_DAG(self):
        f = open(self.dag_file_name, "w")
        # The category's level info will be updated 
        # in the BFS travesal. 
        category_level_dict = {}

        # It's BFS travesal of the graph, plus maintaining 
        # the level as an additioanl info. 
        # So we need current_level_queue, and next_level_queue
        # at the same time. Only if the current_level_queue is
        # empty, the level will increment.
        level = 0
        current_level_queue = [self.root]
        next_level_queue = []

        visited_edges = set()
        num_visited_edges = 0

        while(len(current_level_queue)>0 or len(next_level_queue)>0):
            current_category = current_level_queue.pop(0)
            if(num_visited_edges//1000 % 10) == 0:
                print("\r%s/%s edges are visited." % \
                        (num_visited_edges, self.edge_num), \
                        end='', flush=True)

            # Set the current node's level 
            category_level_dict[current_category] = level

            if current_category in self.graph:
                for neighbor in self.graph[current_category]:
                   # Check if the node will connect to an upper-level node.
                   # If so, we do not output the edge into the final DAG, 
                   # because the "cross" edge "may" cause a cycle. 
                   if neighbor in category_level_dict \
                           and category_level_dict[neighbor] < level: 
                       num_visited_edges += 1
                   else:
                       try:
                           edge = "%s\t%s" % (current_category, neighbor)
                           if(edge not in visited_edges):
                               num_visited_edges += 1

                               f.write("%s\n" % edge)
                               visited_edges.add(edge)
                               next_level_queue.append(neighbor)
                       except Exception as e:
                           print(e)

            if(len(current_level_queue)==0):
               current_level_queue = next_level_queue
               next_level_queue = []
               level += 1
        f.close()
        print("\nThe DAG is saved in %s" % self.dag_file_name)


g = Graph()
g.build_DAG()
