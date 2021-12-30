import sys
from typing import Tuple
import numpy as np
import numpy.typing as npt
import itertools
from rot_mat import rot_mat
from collections import deque

Beacon = npt.NDArray
class Scanner:
    id = 0
    def __init__(self, beacons:list[Beacon]):

        self.beacons = beacons
        self.num_beacons = len(beacons)
        self.id = Scanner.id
        Scanner.id += 1
        self.rot_mat = rot_mat[0]
        self.offset = np.array([0,0,0])
        self.fixed = False
        self.compute_distances_between_beacons()

    def compute_distances_between_beacons(self): 
        self.distances = [[get_distance(b1, b2) for b2 in self.beacons] for b1 in self.beacons]


    def get_overlapping_beacons(s1:'Scanner', s2:'Scanner') -> list[Tuple[Beacon, Beacon]]:
        itr = itertools.product(range(s1.num_beacons), range(s2.num_beacons))
        overlapping_beacons = [ (s1.beacons[b1_idx], s2.beacons[b2_idx]) for b1_idx, b2_idx in itr if len(set(s1.distances[b1_idx]) & set(s2.distances[b2_idx])) >= 12]
        return overlapping_beacons

    def adjust_scanner_offset(self, overlapping_beacons:list[Tuple[Beacon, Beacon]]):
        if not self.fixed:
            for mat in rot_mat:
                adj_loc = [b1-mat.dot(b2) for b1, b2 in overlapping_beacons]
                if np.all(adj_loc[0] == adj_loc[1]):
                    self.rot_mat = mat
                    self.offset = adj_loc[0]
                    self.adjust_beacon_locations()

    def adjust_beacon_locations(self):
        self.fixed = True
        for i, beacon in enumerate(self.beacons):
            self.beacons[i] = self.rot_mat.dot(beacon) + self.offset


def get_distance(b1:Beacon, b2:Beacon) -> float:
    return np.sqrt(np.sum((b1 - b2) ** 2))


def get_manhattan_distance(b1:Beacon, b2:Beacon) -> int:
    return np.sum(np.abs(b1-b2))


def compute_scanner_orientations(scanners:list[Scanner]):
    scanner_idx_q = deque([0])
    scanner_idx_visited = set()

    while scanner_idx_q:
        curr_idx = scanner_idx_q.popleft()
        scanner_idx_visited.add(curr_idx)
        for i in range(len(scanners)):
            if i == curr_idx or i in scanner_idx_visited:
                continue
            overlapping_beacons = Scanner.get_overlapping_beacons(scanners[curr_idx], scanners[i])
            if overlapping_beacons:
                print(f"Found overlap between Scanner {curr_idx} and Scanner {i}")
                scanners[i].adjust_scanner_offset(overlapping_beacons)
                if i not in scanner_idx_q:
                    scanner_idx_q.append(i)

def get_unique_beacons(scanners:list[Scanner]) -> list[Beacon]:
    beacons = []
    for scanner in scanners:
        for beacon in scanner.beacons:
            if not beacons or not np.any(np.all(beacon == beacons, axis=1)):
                beacons.append(beacon)
    return beacons

def get_max_manhattan_distance(scanners:list[Scanner]) -> int:
    dist = [get_manhattan_distance(s1.offset, s2.offset) for s1, s2 in itertools.product(scanners, scanners)]
    return max(dist)

def parse_input(fname:str) -> list[Scanner]:
    scanners = []
    beacons = []
    with open(fname) as file:
        for line in file.readlines():
            tmp = line.strip()
            if tmp:
                if tmp[:3] == '---':
                    beacons.clear()
                else:
                    beacon = np.array([int(x) for x in tmp.split(',')])
                    beacons.append(beacon)
            else:
                scanner = Scanner(beacons.copy())
                scanners.append(scanner)
            
    return scanners


def main():
    fname = sys.argv[1]

    scanners = parse_input(fname)
    compute_scanner_orientations(scanners)

    unique_beacons = get_unique_beacons(scanners)
    print(f"{len(unique_beacons)} unique beacons")

    max_man_dist = get_max_manhattan_distance(scanners)
    print(f"Max Manhattan distance of scanners: {max_man_dist}")


    
if __name__ == "__main__":
    main()