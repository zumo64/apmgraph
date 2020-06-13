class Vertex:
    def __init__(self, v):
        self.name = v[0]
        self.service_time = v[1]
        self.p_fail = v[2]
        self.p_recovery = self.p_fail
        self.is_final = v[3]
        self.state = "OK"

class Edge:
    def __init__(self, e):
        self.name1 = e[0]
        self.name2 = e[1]
        self.p_fail = e[2]

class Graph:
    vertices = {}
    edges = []
    edge_indices = {}

    def load_yaml(self, yaml_obj):
        if yaml_obj is None:
            return
        services = yaml_obj['simpleGraph']['services']

        for a_service in services:
            service_name = list(a_service.keys())[0]
            service_values = list(a_service.values())[0]
            average_service_time = service_values.get('average_service_time')
            probability_of_failure = service_values.get('probability_of_failure')
            is_final_service = service_values.get('is_final_service')
            vertex = (service_name,average_service_time,probability_of_failure,is_final_service)

            self.add_vertex(Vertex(vertex))

        yaml_edges = yaml_obj['simpleGraph']['links']

        for edge in yaml_edges:
            verts = edge.split(":")
            ed = Edge(verts)
            self.add_edge(ed)

        return

    # return list of Vertex connected
    def get_neighbours_of(self, vertex):
        neighbours = []
        u = self.edge_indices[vertex.name]
        li = list(self.vertices.keys())
        for j in range(len(self.edges)):
            if self.edges[u][j] is not None:
                neighbours.append(li[j])
        return neighbours

    def get_vertex(self, name):
        return self.vertices[name]

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            for row in self.edges:
                row.append(None)
            self.edges.append([None] * (len(self.edges) + 1))
            self.edge_indices[vertex.name] = len(self.edge_indices)
            return True
        else:
            return False

    # TODO use weight
    def add_edge(self, e):
        if e.name1 in self.vertices and e.name2 in self.vertices:
            self.edges[self.edge_indices[e.name1]][self.edge_indices[e.name2]] = e
            # lets not do birectional for now
            # self.edges[self.edge_indices[v]][self.edge_indices[u]] = weight
            return True
        else:
            return False

    def print_graph(self):
        for v, i in sorted(self.edge_indices.items()):
            print(v + ' ', end='')
            for j in range(len(self.edges)):
                if self.edges[i][j] is not None:
                    p = "*"
                else:
                    p = "."
                print(p, end='')
            print(' ')


