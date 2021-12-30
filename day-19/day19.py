import sys
import numpy as np
import numpy.typing as npt
import itertools
from rot_mat import rot_mat
from collections import deque

class Beacon:
    def __init__(self, loc:npt.NDArray):
        self.loc = loc

    def get_beacon_distance(b1:'Beacon', b2:'Beacon'):
        return np.sqrt(np.sum((b1.loc - b2.loc) ** 2))

    def __str__(self):
        return str(self.loc)
    
    def __sub__(self, other):
        return Beacon(self.loc - other.loc)

    # def __add__(self, other):
    #     return Beacon(self.loc + other.loc)

    def rotate(self, rot_mat:npt.NDArray):
        return Beacon(rot_mat.dot(self.loc))


class Scanner:
    id = 0
    def __init__(self, beacons:list[Beacon]):

        self.beacons = beacons
        self.id = Scanner.id
        Scanner.id += 1
        self.rot_mat = rot_mat[0]
        self.offset = None
        self.compute_distances_between_beacons()

    def compute_distances_between_beacons(self): 
        self.distances = {b1:[Beacon.get_beacon_distance(b1, b2) for b2 in self.beacons] for b1 in self.beacons}

    def get_overlapping_beacons(s1:'Scanner', s2:'Scanner'):
        itr = itertools.product(s1.beacons, s2.beacons)
        overlapping_beacons = [ (b1,b2) for b1, b2 in itr if len(set(s1.distances[b1]) & set(s2.distances[b2])) >= 12]
        return overlapping_beacons

    def compute_scanner_offset(self, overlapping_beacons):
        for mat in rot_mat:
            adj_loc = [b1-b2.rotate(mat) for b1, b2 in overlapping_beacons]
            if np.all(adj_loc[0].loc == adj_loc[1].loc):
                self.rot_mat = mat
                self.offset = adj_loc[0].loc
                return mat, adj_loc[0].loc

    def adjust_beacon_locations(self):
        for i, beacon in enumerate(self.beacons):
            self.beacons[i] = Beacon(beacon.rotate(self.rot_mat).loc + self.offset)
        self.compute_distances_between_beacons()

def get_unique_beacons(scanners):
    beacons = []
    for scanner in scanners:
        for beacon in scanner.beacons:
            if not beacons or not np.any(np.all(beacon.loc == beacons, axis=1)):
                beacons.append(beacon.loc)
    print(f"{len(beacons)} unique beacons")


def parse_input(fname):
    scanners = []
    beacons = []
    with open(fname) as file:
        for line in file.readlines():
            tmp = line.strip()
            if tmp:
                if tmp[:3] == '---':
                    beacons.clear()
                else:
                    beacon = Beacon(np.array([int(x) for x in tmp.split(',')]))
                    beacons.append(beacon)
            else:
                scanner = Scanner(beacons.copy())
                scanners.append(scanner)
            
    return scanners




def main():
    fname = sys.argv[1]

    scanners = parse_input(fname)

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
                mat, offset = scanners[i].compute_scanner_offset(overlapping_beacons)
                print(f"Found overlap between Scanner {curr_idx} and Scanner {i}")
                scanners[i].adjust_beacon_locations()
                scanner_idx_q.append(i)
        
    get_unique_beacons(scanners)


    

if __name__ == "__main__":
    main()