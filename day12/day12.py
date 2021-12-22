import sys
from collections import deque
import os

def parse_input(fname):
    graph = {}
    with open(fname) as file:
        for line in file.readlines():
            path = line.strip().split('-')

            a = path[0]
            b = path[1]

            target = graph.get(a, [])
            if b not in target:
                target.append(b)
                graph[a] = target

            target = graph.get(b, [])
            if a not in target:
                target.append(a)
                graph[b] = target


    return graph

def is_small_cave_visited_twice(visited):
    return len(visited) != len(set(visited))


def find_paths_bfs(graph):

    final_paths = []
    q = deque()
    visited_q = deque()
    path_q = deque()

    q.append('start')
    visited_q.append(['start'])
    path_q.append(['start'])

    while len(q) > 0:
        curr_node = q.popleft()

        visited = visited_q.popleft()
        path = path_q.popleft()

        for node in graph[curr_node]:
            if node == 'end':
                final_paths.append(path+['end'])
                continue

            if node != 'start' and (node not in visited or not is_small_cave_visited_twice(visited)):
                q.append(node)

                path_tmp = path.copy()
                path_tmp.append(node)
                path_q.append(path_tmp)

                visited_tmp = visited.copy()
                if node.islower():
                    visited_tmp.append(node)
                visited_q.append(visited_tmp)

    return final_paths

def find_paths_dfs(graph):
    curr_node = 'start'
    path = []
    visited = []
    paths = []
    find_paths_dfs_helper(curr_node, path, visited, paths, graph)

    return paths

def find_paths_dfs_helper(node, path, visited, paths, graph):
    if node in visited:
        return
    path.append(node)
    visited.append(node)
    if node == 'end':
        paths.append(path)
    
    for adjNode in graph[node]:
        find_paths_dfs_helper(adjNode, path, visited, paths, graph)
        path.pop()
        visited.pop()
        


def main():
    fname = sys.argv[1]
    graph = parse_input(fname)
    print(graph)

    paths = find_paths_dfs(graph)
    for path in paths:
        print('-'.join(path))
    print(f"Total paths: {len(paths)}")

if __name__ == "__main__":
    main()