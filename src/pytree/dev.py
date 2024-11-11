from dataclasses import dataclass, field
from typing import Generator

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

    def __hash__(self) -> int:
        return hash(self.value)


@dataclass
class Graph:
    nodes: dict[str, Node] = field(default_factory=dict)
    _first_node: Node = None

    def add_node(self, value: str) -> Node:
        if value not in self.nodes:
            self.nodes[value] = Node(value)
        if not self.first_node:
            self.first_node = self.nodes[value]
        return self.nodes[value]

    def add_edge(self, from_value: str, to_value: str) -> None:
        from_node = self.add_node(from_value)
        to_node = self.add_node(to_value)
        from_node.add_edge(to_node)

    @property
    def first_node(self) -> Node | None:
        """helper attribute"""
        return self._first_node

    @first_node.setter
    def first_node(self, node: Node) -> None:
        self._first_node = node

    def display_tree(
        self, start_value: str = None, visited: set[Node] = set(), prefix: str = ""
    ) -> Generator[str] | None:
        current_node = self.nodes.get(start_value)

        # Avoid recursion in case of cycles in graph
        if current_node in visited or not current_node:
            return

        if not visited:
            visited.add(current_node)
            yield f"{prefix}{current_node.value}"

        for i, edge in enumerate(sorted(current_node.edges, key=lambda e: e.value)):
            is_last: bool = i == len(current_node.edges) - 1

            suffix = last if is_last else tee

            yield f"{prefix + suffix}{edge.value}"

            if edge.edges:
                prefix_extension = branch if not is_last else space
                for line in self.display_tree(
                    edge.value, visited, prefix + prefix_extension
                ):
                    yield line

    def __repr__(self) -> str:
        return "\n".join(self.display_tree(self.first_node.value))


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
