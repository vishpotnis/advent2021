import sys
from enum import Enum
from functools import reduce

class PacketType(Enum):
    LITERAL = 1
    OPERATOR = 2

class PacketIDType(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER = 5
    LESS = 6
    EQUAL = 7

class PacketParserType(Enum):
    NUM_PACKETS = 1
    LENGTH = 2
    TAKE_UNTIL = 3

class Packet():
    def __init__(self, pkt_type : PacketType, parsed_pkt):
        self.pkt_type = pkt_type
        self.subpkts = []
        self.value = None
        if self.pkt_type == PacketType.LITERAL:
            self.set_literal_pkt(parsed_pkt)
        elif self.pkt_type == PacketType.OPERATOR:
            self.set_operator_pkt(parsed_pkt)

        self.evaluate_pkt_map = {
            PacketIDType.SUM        :   self.evaluate_sum_pkt,
            PacketIDType.PRODUCT    :   self.evaluate_product_pkt,   
            PacketIDType.MINIMUM    :   self.evaluate_minimum_pkt,
            PacketIDType.MAXIMUM    :   self.evaluate_maximum_pkt,
            PacketIDType.LITERAL    :   self.evaluate_literal_pkt,
            PacketIDType.GREATER    :   self.evaluate_greater_pkt,
            PacketIDType.LESS       :   self.evaluate_less_pkt,
            PacketIDType.EQUAL      :   self.evaluate_equal_pkt
        }

    def set_literal_pkt(self, parsed_pkt):
        self.version = parsed_pkt[0]
        self.id = parsed_pkt[1]
        self.id_type = PacketIDType(self.id)
        self.literal_arr = parsed_pkt[2]
        self.literal_val = 0
        for val in self.literal_arr:
            self.literal_val = self.literal_val * 16 + val

    def set_operator_pkt(self, parsed_pkt):
        self.version = parsed_pkt[0]
        self.id = parsed_pkt[1]
        self.id_type = PacketIDType(self.id)
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
                pkt_txt = f"OPERATOR PKT: version {self.version}, id {self.id} ({self.id_type.name}), length id {self.length_id}, total length {self.total_length} bits"
            elif self.length_id == 1:
                pkt_txt =  f"OPERATOR PKT: version {self.version}, id {self.id} ({self.id_type.name}), length id {self.length_id}, num packets {self.num_subpkts}"
        
        text += header + pkt_txt + '\n'
        for subpkt in self.subpkts:
            text += subpkt.get_string_rep(indent_lvl + 1)
        return text

    def __str__(self):
        return self.get_string_rep(0)


    def evaluate_sum_pkt(self):        
        self.value = reduce(lambda a, b: a + b, map(lambda pkt: pkt.get_value(), self.subpkts))

    def evaluate_product_pkt(self):        
        self.value = reduce(lambda a, b: a * b, map(lambda pkt: pkt.get_value(), self.subpkts))

    def evaluate_minimum_pkt(self):        
        self.value = reduce(lambda a, b: min(a, b), map(lambda pkt: pkt.get_value(), self.subpkts))

    def evaluate_maximum_pkt(self):
        self.value = reduce(lambda a, b: max(a, b), map(lambda pkt: pkt.get_value(), self.subpkts))

    def evaluate_literal_pkt(self):
        self.value = self.literal_val

    def evaluate_greater_pkt(self):
        self.value = int(self.subpkts[0].get_value() > self.subpkts[1].get_value())
            
    def evaluate_less_pkt(self):
        self.value = int(self.subpkts[0].get_value() < self.subpkts[1].get_value())            

    def evaluate_equal_pkt(self):        
        self.value = int(self.subpkts[0].get_value() == self.subpkts[1].get_value())

    def evaluate_pkt(self):
        self.evaluate_pkt_map[self.id_type]()

    def get_value(self):
        if self.value is None:
            self.evaluate_pkt()
        return self.value
        

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

    def parse_num_bits(self, num_bits, advance_idx=False):
        val = int(self.text[self.idx : self.idx + num_bits], 2)
        if advance_idx:
            self.idx += num_bits
            self.num_bits_read += num_bits
        return val

    def parse_packet_header(self, advance_idx=False):
        version = self.parse_num_bits(3, advance_idx=True)
        id = self.parse_num_bits(3, advance_idx)
        if not advance_idx:
            self.idx -= 3
            self.num_bits_read -= 3
        return version, id

    def parse_literal_packet(self):
        version, id = self.parse_packet_header(advance_idx=True)

        literal_val = []
        continue_flag = True
        while continue_flag:
            continue_flag = self.parse_num_bits(1, advance_idx=True)
            val = self.parse_num_bits(4, advance_idx=True)
            literal_val.append(val)
        return (version, id, literal_val)
        
    def parse_operator_packet(self):
        version, id = self.parse_packet_header(advance_idx=True)
        length_id = self.parse_num_bits(1, advance_idx=True)

        if length_id == 0:
            total_length = self.parse_num_bits(15, advance_idx=True)
            return (version, id, length_id, total_length)
        elif length_id == 1:
            num_subpkts = self.parse_num_bits(11, advance_idx=True)
            return (version, id, length_id, num_subpkts)

    def parse(self):
        if self.parser_type == PacketParserType.TAKE_UNTIL:
            return self.parse_type_take_until()
        elif self.parser_type == PacketParserType.LENGTH:
            return self.parse_type_num_bits()
        elif self.parser_type == PacketParserType.NUM_PACKETS:
            return self.parse_type_num_packets()

    def parse_pkt(self):
        version, id = self.parse_packet_header(advance_idx=False)
        if id == 4:
            parsed_pkt = self.parse_literal_packet()
            pkt = Packet(PacketType.LITERAL, parsed_pkt)
        else:
            parsed_pkt = self.parse_operator_packet()
            pkt = Packet(PacketType.OPERATOR, parsed_pkt)
            self.parse_subpkt(pkt)

        self.pkts.append(pkt)
        self.num_pkts_parsed += 1
        PacketParser.all_pkts.append(pkt)

    def parse_subpkt(self, pkt):
        if pkt.length_id == 0:
            parser = PacketParser(self.text, PacketParserType.LENGTH, idx=self.idx, num_length=pkt.total_length)
        elif pkt.length_id == 1:
            parser = PacketParser(self.text, PacketParserType.NUM_PACKETS, idx=self.idx, num_pkts=pkt.num_subpkts)
        parsed_subpkts, new_idx, subpkt_bits_read = parser.parse()
        self.num_bits_read += subpkt_bits_read
        self.idx = new_idx
        pkt.subpkts.extend(parsed_subpkts)


    def parse_type_take_until(self):
        while len(self.text[self.idx:]) and int(self.text[self.idx:], 2) != 0:
            self.parse_pkt()
        return self.pkts, self.idx, self.num_bits_read

    def parse_type_num_bits(self):
        while self.num_bits_read < self.num_length:
            self.parse_pkt()
        return self.pkts, self.idx, self.num_bits_read

    def parse_type_num_packets(self):
        while self.num_pkts_parsed < self.num_pkts:
            self.parse_pkt()
        return self.pkts, self.idx, self.num_bits_read


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

    # istrs = ['D2FE28', '38006F45291200', 'EE00D40C823060', '8A004A801A8002F478', '620080001611562C8802118E34', 'C0015000016115A2E0802F182340', 'A0016C880162017C3686B18A3D4780',
            #  'C200B40A82', '04005AC33890', '880086C3E88112', 'CE00C43D881120', 'D8005AC2A8F0', 'F600BC2D8F', '9C005AC2F8F0', '9C0141080250320F1802104A08']    
    # bin_str = parse_input_from_str(istrs[7])

    parser = PacketParser(bin_str)
    parsed_pkts, _, _ = parser.parse()

    for pkt in parsed_pkts:
        print(pkt)
        print(f"Packet value: {pkt.get_value()}")
        
    print(f"Version sum: {get_version_sum(PacketParser.all_pkts)}")

if __name__ == "__main__":
    main()