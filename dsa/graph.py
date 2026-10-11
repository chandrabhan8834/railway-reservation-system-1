from collections import deque, defaultdict


class RailwayGraph:
    """Graph representation of railway station connectivity."""

    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, source, destination):
        self.graph[source].append(destination)
        self.graph[destination].append(source)

    def bfs(self, start, goal=None):
        # BFS: O(V + E), used for shortest path exploration in unweighted graphs.
        visited = {start}
        queue = deque([start])
        parent = {start: None}

        while queue:
            current = queue.popleft()
            if goal and current == goal:
                break
            for neighbor in self.graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        if goal is None:
            return visited, parent
        return self._build_path(parent, goal), visited

    def dfs(self, start, visited=None, traversal=None):
        # DFS: O(V + E), used to traverse station connectivity deeply.
        if visited is None:
            visited = set()
        if traversal is None:
            traversal = []
        visited.add(start)
        traversal.append(start)

        for neighbor in self.graph.get(start, []):
            if neighbor not in visited:
                self.dfs(neighbor, visited, traversal)
        return traversal

    def connected_components(self):
        visited = set()
        components = []
        for station in self.graph:
            if station not in visited:
                comp = []
                stack = [station]
                while stack:
                    node = stack.pop()
                    if node in visited:
                        continue
                    visited.add(node)
                    comp.append(node)
                    for neighbor in self.graph.get(node, []):
                        if neighbor not in visited:
                            stack.append(neighbor)
                components.append(comp)
        return components

    def _build_path(self, parent, goal):
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        return list(reversed(path))

    def routes_between(self, source, destination):
        queue = deque([(source, [source])])
        visited = {source}
        routes = []
        while queue:
            station, path = queue.popleft()
            for neighbor in self.graph.get(station, []):
                if neighbor == destination:
                    routes.append(path + [neighbor])
                elif neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return routes
