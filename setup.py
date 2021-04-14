from pony.orm import *
import csv

db = Database()
db.bind(provider='mysql', user='root', password='statracker1', host='127.0.0.1', db='internet')
# db.drop_all_tables()

class Flow(db.Entity):
    id = PrimaryKey(int, auto=True)
    category = Optional(str)
    application_protocol = Optional(str)
    web_service = Optional(str)
    src_node = Required('NetworkNode', reverse='flows_as_src')
    dest_node = Required('NetworkNode', reverse='flows_as_dest')
    packet_info = Optional('PacketInfo')
    protocol_id = Optional('Protocol')
    end_reason_id = Optional('EndReason')


class NetworkNode(db.Entity):
    ip = Required(str)
    port = Required(int)
    flows_as_src = Set(Flow, reverse='src_node')
    flows_as_dest = Set(Flow, reverse='dest_node')
    notes = Optional(str)
    PrimaryKey(ip, port)


class PacketInfo(db.Entity):
    id = PrimaryKey(int, auto=True)
    flow_id = Required(Flow)
    packet_total_count = Optional(int)
    octet_total_count = Optional(int)
    max_pkt_size = Optional(float)
    avg_pkt_size = Optional(float)
    max_pkt_arrival_time = Optional(float)
    avg_pkt_arrival_time = Optional(float)


class Protocol(db.Entity):
    id = PrimaryKey(int)
    name = Optional(str)
    flow_ids = Set(Flow)


class EndReason(db.Entity):
    id = PrimaryKey(int)
    description = Optional(str)
    flow_ids = Set(Flow)


db.generate_mapping(create_tables=True)

@db_session
def populate_db():
    # p1 = Protocol(id=1, name='ICMP')
    # p2 = Protocol(id=6, name='TCP')
    # p3 = Protocol(id=17, name='UDP')
    #
    # er0 = EndReason(id=0, description='inactive timeout expired')
    # er1 = EndReason(id=1, description='active timeout expired')
    # er2 = EndReason(id=2, description='forced expiration due to end of pcap file or live captured stopped')
    # er3 = EndReason(id=3, description='FIN flag detected on both directions')
    # er4 = EndReason(id=4, description='RST flag detected')
    # er5 = EndReason(id=5, description='FIN Flag detected on one direction only and timer expired')

    row_number = 0
    with open('dataset.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row_number > 10:
                # NetworkNode
                src_ip = row[2]
                src_port = row[3]
                src_node = NetworkNode.get(ip=src_ip, port=src_port)
                if src_node is None:
                    src_node = NetworkNode(ip=src_ip, port=src_port)
                dest_ip = row[4]
                dest_port = row[5]
                dest_node = NetworkNode.get(ip=dest_ip, port=dest_port)
                if dest_node is None:
                    dest_node = NetworkNode(ip=dest_ip, port=dest_port)

                # Flow
                temp_flow = Flow(src_node=src_node, dest_node=dest_node, category=row[47], application_protocol=row[48], web_service=row[49])
                # PacketInfo
                temp_pkt_info = PacketInfo(flow_id=temp_flow, packet_total_count=row[7], octet_total_count=row[8], max_pkt_size=row[10], avg_pkt_size=row[11], max_pkt_arrival_time=row[27], avg_pkt_arrival_time=row[28])
                temp_flow.packet_info = temp_pkt_info
                # Protocol
                protocol = Protocol.get(id=row[6])
                if protocol is None:
                    print("invalid protocol: ", row[6])
                else:
                    temp_flow.protocol_id = protocol
                # EndReason
                end_reason = EndReason.get(id=int(row[46]))
                if end_reason is None:
                    print("invalid end reason: ", row[46])
                else:
                    temp_flow.end_reason_id = end_reason
            row_number += 1
            if row_number > 1000:
                break

populate_db()
