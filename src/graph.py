"""Graph operations for dependency analysis."""
from parser import find_package_data, extract_dependencies


class DependencyGraph:
    """Класс для построения и анализа графа зависимостей."""

    def __init__(self, repo_content):
        self.repo_content = repo_content
        self.graph = {}
        self.reverse_graph = {}

    def build_graph(self, pkg_name, max_depth, filter_str, depth=0, 
                    visited=None):
        """Строит граф с помощью рекурсивного DFS."""
        if visited is None:
            visited = set()
            
        if depth > max_depth:
            return
            
        if filter_str and filter_str in pkg_name:
            return
            
        if pkg_name in visited:
            return
            
        visited.add(pkg_name)
        
        pkg_block = find_package_data(self.repo_content, pkg_name, "1.0")
        if not pkg_block:
            pkg_block = find_package_data(self.repo_content, pkg_name, "latest")
            
        deps = extract_dependencies(pkg_block) if pkg_block else []
        self.graph[pkg_name] = deps
        
        for dep in deps:
            if dep not in self.reverse_graph:
                self.reverse_graph[dep] = []
            self.reverse_graph[dep].append(pkg_name)
            self.build_graph(dep, max_depth, filter_str, depth + 1, visited)

    def get_reverse_dependencies(self, target_pkg):
        """Возвращает обратные зависимости (Этап 4)."""
        return self.reverse_graph.get(target_pkg, [])