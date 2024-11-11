from dataclasses import dataclass, field

# prefix:
space = "    "
branch = "│   "
# suffix:
tee = "├── "
last = "└── "


@dataclass
class Node:
    value: str
    edges: set["Node"] = field(default_factory=set)

    def add_edge(self, to_node: "Node") -> None:
        self.edges.add(to_node)

    def __repr__(self) -> str:
        return f"Node({self.value})"

    def __hash__(self):
        return hash(self.value)


@dataclass
class Graph:
    nodes: dict[str, Node] = field(default_factory=dict)

    def add_node(self, value: str) -> Node:
        if value not in self.nodes:
            self.nodes[value] = Node(value)
        return self.nodes[value]

    def add_edge(self, from_value: str, to_value: str):
        from_node = self.add_node(from_value)
        to_node = self.add_node(to_value)
        from_node.add_edge(to_node)

    def display_tree(
        self, start_value: str = None, visited: set[Node] = set(), prefix: str = ""
    ) -> None:
        current_node = self.nodes.get(start_value)

        # Avoid recursion in case of cycles in graph
        if current_node in visited or not current_node:
            return

        if not visited:
            visited.add(current_node)
            print(f"{prefix}{current_node.value}")

        for i, edge in enumerate(sorted(current_node.edges, key=lambda e: e.value)):
            is_last: bool = i == len(current_node.edges) - 1

            suffix = last if is_last else tee

            print(f"{prefix + suffix}{edge.value}")

            if edge.edges:
                prefix_extension = branch if not is_last else space
                self.display_tree(edge.value, visited, prefix + prefix_extension)

    def __repr__(self) -> str:
        return self.display_tree("A")


if __name__ == "__main__":
    # Example usage
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("D", "E")
    graph.add_edge("C", "F")
    graph.add_edge("C", "G")
    graph.add_edge("B", "H")
    graph.add_edge("B", "I")
    graph.add_edge("B", "A")

    print(graph)
