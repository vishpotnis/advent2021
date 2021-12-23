import sys
from enum import Enum

class PacketType(Enum):
    LITERAL = 1
    OPERATOR = 2

class PacketParserType(Enum):
    NUM_PACKETS = 1
    LENGTH = 2
    TAKE_UNTIL = 3


class Packet():
    def __init__(self, pkt_type : PacketType, parsed_pkt):
        self.pkt_type = pkt_type
        self.subpkts = []
        if self.pkt_type == PacketType.LITERAL:
            self.set_literal_pkt(parsed_pkt)
        elif self.pkt_type == PacketType.OPERATOR:
            self.set_operator_pkt(parsed_pkt)

    def set_literal_pkt(self, parsed_pkt):
        self.version = parsed_pkt[0]
        self.id = parsed_pkt[1]
        self.literal_arr = parsed_pkt[2]
        self.literal_val = 0
        for val in self.literal_arr:
            self.literal_val = self.literal_val * 16 + val

    def set_operator_pkt(self, parsed_pkt):
        self.version = parsed_pkt[0]
        self.id = parsed_pkt[1]
        self.length_id = parsed_pkt[2]
        if self.length_id == 0:
            self.total_length = parsed_pkt[3]
        elif self.length_id == 1:
            self.num_subpkts = parsed_pkt[3]

    def get_string_rep(self, indent_lvl):
        header = '\t' * indent_lvl
        text = ''
        if self.pkt_type == PacketType.LITERAL:
            pkt_txt = f"LITERAL PKT: version {self.version}, id {self.id}, literal {self.literal_val}"
        elif self.pkt_type == PacketType.OPERATOR:
            if self.length_id == 0:
                pkt_txt = f"OPERATOR PKT: version {self.version}, id {self.id}, length id {self.length_id}, total length {self.total_length} bits"
            elif self.length_id == 1:
                pkt_txt =  f"OPERATOR PKT: version {self.version}, id {self.id}, length id {self.length_id}, num packets {self.num_subpkts}"
        
        text += header + pkt_txt + '\n'
        for subpkt in self.subpkts:
            text += subpkt.get_string_rep(indent_lvl + 1)            
        return text


    def __str__(self):
        return self.get_string_rep(0)
        



class PacketParser():

    all_pkts = []

    def __init__(self, text, parser_type=PacketParserType.TAKE_UNTIL, idx=0, num_length=None, num_pkts=None):
        self.text = text
        self.idx = idx     
        self.parser_type = parser_type
        self.num_length = num_length
        self.num_pkts = num_pkts

        self.pkts = []
        self.num_bits_read = 0
        self.num_pkts_parsed = 0

    def parse_literal_packet(self):
        version, id = self.parse_packet_header(advance_idx=True)
        
        literal_val = []
        done = False        
        while not done:
            literal_text = self.text[self.idx : self.idx + 5]
            if literal_text[0] == '0':
                done = True
            literal_val.append(int(self.text[self.idx + 1 : self.idx + 5], 2))
            self.idx += 5
            self.num_bits_read += 5
        return (version, id, literal_val)
        
    def parse_operator_packet(self):
        version, id = self.parse_packet_header(advance_idx=True)
        length_id = int(self.text[self.idx], 2)
        self.idx += 1
        self.num_bits_read += 1

        if length_id == 0:
            total_length = int(self.text[self.idx : self.idx + 15], 2)
            self.idx += 15
            self.num_bits_read += 15
            return (version, id, length_id, total_length)
        elif length_id == 1:
            num_subpkts = int(self.text[self.idx : self.idx + 11], 2)
            self.idx += 11
            self.num_bits_read += 11
            return (version, id, length_id, num_subpkts)
            

    def parse_packet_header(self, advance_idx=False):
        version = int(self.text[self.idx : self.idx + 3],2)
        id = int(self.text[self.idx + 3: self.idx + 6],2)
        if advance_idx:
            self.idx += 6
            self.num_bits_read += 6
        return version, id


    def parse(self):
        if self.parser_type == PacketParserType.TAKE_UNTIL:
            return self.parse_take_until()
        elif self.parser_type == PacketParserType.LENGTH:
            return self.parse_num_bits()
        elif self.parser_type == PacketParserType.NUM_PACKETS:
            return self.parse_num_packets()

    def parse_block(self):
        version, id = self.parse_packet_header(advance_idx=False)
        if id == 4:
            parsed_pkt = self.parse_literal_packet()
            pkt = Packet(PacketType.LITERAL, parsed_pkt)
        else:
            parsed_pkt = self.parse_operator_packet()
            length_id = parsed_pkt[2]
            pkt = Packet(PacketType.OPERATOR, parsed_pkt)
            if length_id == 0:
                parser = PacketParser(self.text, PacketParserType.LENGTH, idx=self.idx, num_length=parsed_pkt[3])
            elif length_id == 1:
                parser = PacketParser(self.text, PacketParserType.NUM_PACKETS, idx=self.idx, num_pkts=parsed_pkt[3])
            parsed_subpkts, new_idx = parser.parse()
            self.num_bits_read += new_idx - self.idx
            self.idx = new_idx
            pkt.subpkts.extend(parsed_subpkts)

        self.pkts.append(pkt)
        self.num_pkts_parsed += 1
        PacketParser.all_pkts.append(pkt)



    def parse_take_until(self):
        while int(self.text[self.idx:], 2) != 0:        
            self.parse_block()
        return self.pkts, self.idx
    
    def parse_num_bits(self):
        while self.num_bits_read < self.num_length:
            self.parse_block()
        return self.pkts, self.idx

    def parse_num_packets(self):
        while self.num_pkts_parsed < self.num_pkts:
            self.parse_block()
        return self.pkts, self.idx


def parse_input(fname):
    with open(fname) as file:
        text = file.readline()    
    return parse_input_from_str(text)

def parse_input_from_str(text):
    bin_str = bin(int(text,16))[2:].zfill(len(text)*4)
    return bin_str    

def get_version_sum(pkts):
    sum = 0
    for pkt in pkts:
        sum += pkt.version
    return sum


def main():
    fname = sys.argv[1]
    bin_str = parse_input(fname)

    # istrs = ['D2FE28', '38006F45291200', 'EE00D40C823060', '8A004A801A8002F478', '620080001611562C8802118E34', 'C0015000016115A2E0802F182340', 'A0016C880162017C3686B18A3D4780']
    # bin_str = parse_input_from_str(istrs[6])

    parser = PacketParser(bin_str)
    parsed_pkts, num_bits_parsed = parser.parse()    

    for pkt in parsed_pkts:
        print(pkt)
        
    print(f"Version sum: {get_version_sum(PacketParser.all_pkts)}")

if __name__ == "__main__":
    main()