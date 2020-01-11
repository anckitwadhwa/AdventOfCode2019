from collections import deque
import IntcodeExecutor
import time
from inspect import currentframe
import threading
        
class NetworkProcessor:
    NAT_ADDRESS = 255
    RESTART_NETWORK_ACTIVITY_THRESHOLD_IN_SECS = 10
    
    def __init__(self, nic_program, num_nodes = 50, debug_prints_level = 0):
        debug_prints_level -= 1
        
        self.num_nodes = num_nodes
        self.nodes = [None] * num_nodes
        self.network_queue = deque()
        self.NAT_x = -1
        self.NAT_y = -1
        self.last_restart_y = -2
        self.halted = False
        
        for node_id in range(num_nodes):
        
            input_queue = deque()
            input_queue.append((node_id, -1))

            self.nodes[node_id] = IntcodeExecutor.IntcodeExecutor(nic_program.copy(), IntcodeExecutor.NetworkIOHandler(input_queue, self.network_queue), False)
        
        self.thread = threading.Thread(name="process_network_traffic", target=self.process_network_traffic, args=([debug_prints_level]))
        self.thread.start()
        
    def __del__(self):
        self.signal_termination()

        for node in self.nodes:
            my_thread_join(node.thread, currentframe().f_lineno, debug_prints_level)
        
    def _restart_network_activity(self, debug_prints_level = 0):
        debug_prints_level -= 1
        
        if(debug_prints_level > 30):
            print(f'restarting network activity')
        
        self.network_queue.append((0, self.NAT_x, self.NAT_y))
        
        if(self.last_restart_y == self.NAT_y):
            print(f'first value delivered twice: {self.NAT_y}')
            self.signal_termination(debug_prints_level)
        else:
            self.last_restart_y = self.NAT_y
        
    def signal_termination(self, debug_prints_level = 0):
        debug_prints_level -= 1
        
        if(debug_prints_level > 50):
            print(f'NetworkProcessor termination signaled')
        
        self.halted = True
        
        for node in self.nodes:
            node.signal_termination(debug_prints_level)
        
    def is_halted(self, debug_prints_level = 0):
        debug_prints_level -= 1
        
        return(self.halted)
        
        
    def process_network_traffic(self, debug_prints_level = 0):
        debug_prints_level -= 1
    
        network_queue = self.network_queue
        nodes = self.nodes
        
        
        while(not(self.is_halted())):
        
            if(debug_prints_level > 90):
                print("in first while loop of process_network_traffic")
    
            sleep_time_in_secs = 0.001
            
            while (not(self.is_halted()) and (len(network_queue) < 1)):
                if(sleep_time_in_secs >= self.RESTART_NETWORK_ACTIVITY_THRESHOLD_IN_SECS):
                    self._restart_network_activity(debug_prints_level)
                
                
                if(debug_prints_level > 90):
                    print(f'Sleeping in process_network_traffic for {sleep_time_in_secs}s')
                
                time.sleep(sleep_time_in_secs)
                
                sleep_time_in_secs *= 5
                sleep_time_in_secs = min(sleep_time_in_secs, self.RESTART_NETWORK_ACTIVITY_THRESHOLD_IN_SECS)
            
            if(debug_prints_level > 50):
                print(f'Awake in process_network_traffic. Last sleep was {sleep_time_in_secs / 5}s')
                        
            if(self.is_halted()):
                break
            
            element = network_queue.popleft()
            
            destination_address = element[0]
            x_value = element[1]
            y_value = element[2]
            
            if(destination_address < self.num_nodes):
            
                if(debug_prints_level > 50):
                    print(f'destination_address:{destination_address}; x_value: {x_value}; y_value: {y_value}')
                
                input_queue = nodes[destination_address].io_handler.input_queue
                
                input_queue.append((x_value, y_value))
            
            if(destination_address == self.NAT_ADDRESS):
                print(f'y_value for address {destination_address} is {y_value}')

                self.NAT_x = x_value
                self.NAT_y = y_value
    
        if(debug_prints_level > 50):
            print("exiting process_network_traffic")
                
def my_thread_join(thread, line_num, debug_prints_level = 0):
    debug_prints_level -= 1
    
    if(debug_prints_level > 90):
        print(f'Waiting for {thread.name} to join. line#:{line_num}')
    
    thread.join()
    
    if(debug_prints_level > 90):
        print(f'{thread.name} joined. line#:{line_num}')
    
def solve_day_23_puzzle(nic_program, num_nodes, debug_prints_level):
    debug_prints_level -= 1
    
    processor = NetworkProcessor(nic_program, num_nodes, debug_prints_level)
    
    choice = ""
    
    while((choice != 'q') and (choice != 'y')):
        
        input_str = input("Quit Q/q?: ")
        
        if(len(input_str) > 0):
            choice = input_str[0].lower()
        else:
            choice = ""
    
    processor.signal_termination(debug_prints_level)
    
    my_thread_join(processor.thread, currentframe().f_lineno, debug_prints_level)
    
nic_program = [3,62,1001,62,11,10,109,2253,105,1,0,1585,1752,2053,1981,1074,2216,571,602,2018,878,1039,2117,1309,944,1344,779,1245,633,1816,913,1851,2086,1882,1167,1447,1552,1478,1379,975,2148,1946,1416,738,1521,1134,672,812,1105,705,1721,1626,1006,1276,1787,1655,1917,843,1210,2179,1690,0,0,0,0,0,0,0,0,0,0,0,0,3,64,1008,64,-1,62,1006,62,88,1006,61,170,1106,0,73,3,65,21002,64,1,1,20101,0,66,2,21101,0,105,0,1105,1,436,1201,1,-1,64,1007,64,0,62,1005,62,73,7,64,67,62,1006,62,73,1002,64,2,133,1,133,68,133,101,0,0,62,1001,133,1,140,8,0,65,63,2,63,62,62,1005,62,73,1002,64,2,161,1,161,68,161,1101,0,1,0,1001,161,1,169,102,1,65,0,1102,1,1,61,1101,0,0,63,7,63,67,62,1006,62,203,1002,63,2,194,1,68,194,194,1006,0,73,1001,63,1,63,1106,0,178,21101,210,0,0,105,1,69,1201,1,0,70,1101,0,0,63,7,63,71,62,1006,62,250,1002,63,2,234,1,72,234,234,4,0,101,1,234,240,4,0,4,70,1001,63,1,63,1105,1,218,1105,1,73,109,4,21102,0,1,-3,21102,0,1,-2,20207,-2,67,-1,1206,-1,293,1202,-2,2,283,101,1,283,283,1,68,283,283,22001,0,-3,-3,21201,-2,1,-2,1105,1,263,22101,0,-3,-3,109,-4,2106,0,0,109,4,21101,0,1,-3,21102,0,1,-2,20207,-2,67,-1,1206,-1,342,1202,-2,2,332,101,1,332,332,1,68,332,332,22002,0,-3,-3,21201,-2,1,-2,1106,0,312,21201,-3,0,-3,109,-4,2105,1,0,109,1,101,1,68,359,20102,1,0,1,101,3,68,367,20101,0,0,2,21102,376,1,0,1106,0,436,22102,1,1,0,109,-1,2105,1,0,1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576,2097152,4194304,8388608,16777216,33554432,67108864,134217728,268435456,536870912,1073741824,2147483648,4294967296,8589934592,17179869184,34359738368,68719476736,137438953472,274877906944,549755813888,1099511627776,2199023255552,4398046511104,8796093022208,17592186044416,35184372088832,70368744177664,140737488355328,281474976710656,562949953421312,1125899906842624,109,8,21202,-6,10,-5,22207,-7,-5,-5,1205,-5,521,21101,0,0,-4,21102,1,0,-3,21101,0,51,-2,21201,-2,-1,-2,1201,-2,385,470,21002,0,1,-1,21202,-3,2,-3,22207,-7,-1,-5,1205,-5,496,21201,-3,1,-3,22102,-1,-1,-5,22201,-7,-5,-7,22207,-3,-6,-5,1205,-5,515,22102,-1,-6,-5,22201,-3,-5,-3,22201,-1,-4,-4,1205,-2,461,1105,1,547,21101,0,-1,-4,21202,-6,-1,-6,21207,-7,0,-5,1205,-5,547,22201,-7,-6,-7,21201,-4,1,-4,1106,0,529,21202,-4,1,-7,109,-8,2106,0,0,109,1,101,1,68,563,21001,0,0,0,109,-1,2105,1,0,1102,22153,1,66,1102,1,1,67,1101,0,598,68,1101,556,0,69,1102,1,1,71,1102,600,1,72,1106,0,73,1,160,32,66644,1102,1,73561,66,1101,0,1,67,1102,1,629,68,1101,0,556,69,1101,1,0,71,1102,631,1,72,1106,0,73,1,1167,48,257073,1102,1,21773,66,1101,5,0,67,1101,0,660,68,1101,302,0,69,1102,1,1,71,1101,0,670,72,1106,0,73,0,0,0,0,0,0,0,0,0,0,3,288843,1101,59063,0,66,1102,1,1,67,1102,1,699,68,1102,556,1,69,1101,0,2,71,1101,701,0,72,1106,0,73,1,10,27,55702,32,99966,1102,1,89797,66,1102,1,1,67,1101,732,0,68,1102,1,556,69,1101,2,0,71,1102,1,734,72,1105,1,73,1,3,9,137338,17,65319,1102,1,16661,66,1101,0,6,67,1102,1,765,68,1102,1,302,69,1101,0,1,71,1102,777,1,72,1106,0,73,0,0,0,0,0,0,0,0,0,0,0,0,2,173702,1102,41357,1,66,1101,2,0,67,1101,0,806,68,1102,302,1,69,1101,1,0,71,1102,1,810,72,1105,1,73,0,0,0,0,3,96281,1101,85381,0,66,1102,1,1,67,1102,839,1,68,1101,556,0,69,1101,1,0,71,1101,0,841,72,1106,0,73,1,307,47,49297,1101,99371,0,66,1101,0,3,67,1102,870,1,68,1101,253,0,69,1102,1,1,71,1102,876,1,72,1106,0,73,0,0,0,0,0,0,34,71881,1102,68669,1,66,1102,1,3,67,1101,0,905,68,1102,302,1,69,1102,1,1,71,1101,0,911,72,1106,0,73,0,0,0,0,0,0,17,21773,1101,0,12763,66,1101,0,1,67,1101,940,0,68,1101,0,556,69,1102,1,1,71,1101,942,0,72,1106,0,73,1,19,5,189746,1102,22699,1,66,1102,1,1,67,1102,1,971,68,1102,556,1,69,1102,1,1,71,1102,973,1,72,1106,0,73,1,-126,44,29473,1102,1,75193,66,1101,1,0,67,1102,1002,1,68,1102,1,556,69,1101,0,1,71,1101,1004,0,72,1105,1,73,1,15731,30,278097,1101,23879,0,66,1102,1,1,67,1102,1,1033,68,1102,1,556,69,1101,0,2,71,1101,0,1035,72,1105,1,73,1,7,17,43546,5,379492,1102,1,93179,66,1101,0,3,67,1102,1,1066,68,1102,302,1,69,1101,1,0,71,1102,1072,1,72,1106,0,73,0,0,0,0,0,0,14,35146,1101,101873,0,66,1101,1,0,67,1102,1,1101,68,1101,0,556,69,1102,1,1,71,1101,0,1103,72,1105,1,73,1,205,1,1877,1101,0,104161,66,1101,0,1,67,1102,1132,1,68,1102,556,1,69,1102,1,0,71,1101,1134,0,72,1106,0,73,1,1010,1101,71881,0,66,1101,2,0,67,1101,1161,0,68,1102,302,1,69,1102,1,1,71,1101,1165,0,72,1106,0,73,0,0,0,0,5,284619,1102,11483,1,66,1101,0,1,67,1102,1194,1,68,1101,0,556,69,1102,7,1,71,1102,1,1196,72,1106,0,73,1,1,22,90994,10,186358,30,185398,47,98594,1,5631,48,342764,44,88419,1102,49297,1,66,1101,0,3,67,1102,1237,1,68,1102,302,1,69,1102,1,1,71,1102,1243,1,72,1106,0,73,0,0,0,0,0,0,46,198742,1102,56369,1,66,1102,1,1,67,1101,0,1272,68,1101,556,0,69,1102,1,1,71,1102,1,1274,72,1105,1,73,1,-95,10,93179,1102,29671,1,66,1102,1,1,67,1101,0,1303,68,1102,1,556,69,1101,2,0,71,1102,1,1305,72,1105,1,73,1,263,17,87092,44,58946,1102,1,50273,66,1102,1,1,67,1101,0,1336,68,1102,1,556,69,1101,0,3,71,1101,1338,0,72,1105,1,73,1,5,27,83553,27,111404,32,16661,1102,1,17573,66,1101,3,0,67,1102,1371,1,68,1101,253,0,69,1101,0,1,71,1102,1,1377,72,1106,0,73,0,0,0,0,0,0,25,65171,1101,0,27851,66,1101,4,0,67,1102,1406,1,68,1101,0,302,69,1101,0,1,71,1101,0,1414,72,1105,1,73,0,0,0,0,0,0,0,0,32,83305,1102,1,29399,66,1102,1,1,67,1102,1443,1,68,1101,0,556,69,1102,1,1,71,1102,1445,1,72,1105,1,73,1,1753,1,3754,1101,62659,0,66,1102,1,1,67,1102,1474,1,68,1102,1,556,69,1102,1,1,71,1102,1476,1,72,1105,1,73,1,126,47,147891,1101,64951,0,66,1101,0,1,67,1101,0,1505,68,1102,1,556,69,1101,7,0,71,1101,1507,0,72,1106,0,73,1,2,25,130342,9,206007,17,108865,34,143762,5,94873,32,33322,32,49983,1102,1,33851,66,1102,1,1,67,1101,0,1548,68,1102,1,556,69,1102,1,1,71,1101,0,1550,72,1106,0,73,1,2903,10,279537,1101,65171,0,66,1101,0,2,67,1102,1,1579,68,1102,1,302,69,1102,1,1,71,1101,0,1583,72,1106,0,73,0,0,0,0,9,68669,1101,47857,0,66,1102,1,1,67,1102,1612,1,68,1101,556,0,69,1101,6,0,71,1102,1,1614,72,1105,1,73,1,18000,15,41357,8,68963,8,137926,18,37897,18,75794,18,113691,1102,95957,1,66,1101,0,1,67,1102,1,1653,68,1102,1,556,69,1102,1,0,71,1102,1655,1,72,1105,1,73,1,1065,1101,29473,0,66,1101,0,3,67,1101,1682,0,68,1101,302,0,69,1101,1,0,71,1102,1688,1,72,1106,0,73,0,0,0,0,0,0,8,206889,1102,70877,1,66,1101,0,1,67,1101,1717,0,68,1102,1,556,69,1102,1,1,71,1101,0,1719,72,1106,0,73,1,43,48,171382,1101,92987,0,66,1102,1,1,67,1101,0,1748,68,1101,0,556,69,1102,1,1,71,1101,1750,0,72,1106,0,73,1,-804,22,45497,1101,0,1877,66,1102,1,3,67,1102,1779,1,68,1101,302,0,69,1101,0,1,71,1101,1785,0,72,1105,1,73,0,0,0,0,0,0,46,99371,1102,1,29759,66,1102,1,1,67,1102,1814,1,68,1101,556,0,69,1101,0,0,71,1101,0,1816,72,1106,0,73,1,1138,1101,37897,0,66,1101,0,3,67,1102,1,1843,68,1102,1,302,69,1102,1,1,71,1101,0,1849,72,1105,1,73,0,0,0,0,0,0,3,385124,1101,51683,0,66,1102,1,1,67,1101,1878,0,68,1101,556,0,69,1101,1,0,71,1101,1880,0,72,1106,0,73,1,32,48,85691,1101,0,45497,66,1102,3,1,67,1102,1,1909,68,1101,0,302,69,1102,1,1,71,1102,1915,1,72,1105,1,73,0,0,0,0,0,0,14,52719,1102,22063,1,66,1101,0,1,67,1102,1,1944,68,1102,1,556,69,1101,0,0,71,1102,1,1946,72,1105,1,73,1,1265,1102,92699,1,66,1102,1,3,67,1101,0,1973,68,1102,1,302,69,1101,1,0,71,1101,0,1979,72,1106,0,73,0,0,0,0,0,0,14,17573,1101,0,96281,66,1102,1,4,67,1102,1,2008,68,1102,253,1,69,1102,1,1,71,1101,2016,0,72,1105,1,73,0,0,0,0,0,0,0,0,2,86851,1102,1,68963,66,1101,0,3,67,1101,0,2045,68,1101,302,0,69,1101,1,0,71,1102,1,2051,72,1105,1,73,0,0,0,0,0,0,3,192562,1101,86851,0,66,1101,0,2,67,1102,2080,1,68,1101,0,351,69,1101,0,1,71,1102,2084,1,72,1106,0,73,0,0,0,0,255,47857,1101,0,95783,66,1101,0,1,67,1101,2113,0,68,1102,556,1,69,1102,1,1,71,1101,0,2115,72,1106,0,73,1,125,27,27851,1102,1,93787,66,1101,0,1,67,1102,2144,1,68,1102,1,556,69,1102,1,1,71,1102,2146,1,72,1105,1,73,1,4649,22,136491,1101,0,90971,66,1101,0,1,67,1101,0,2175,68,1101,556,0,69,1101,1,0,71,1102,1,2177,72,1106,0,73,1,1198,30,92699,1102,85691,1,66,1102,4,1,67,1102,2206,1,68,1101,0,302,69,1101,1,0,71,1101,0,2214,72,1106,0,73,0,0,0,0,0,0,0,0,46,298113,1102,1,94873,66,1101,4,0,67,1102,2243,1,68,1101,302,0,69,1101,1,0,71,1101,2251,0,72,1105,1,73,0,0,0,0,0,0,0,0,15,82714]

# debug_prints_level = 100
# num_nodes = 1

debug_prints_level = 50
num_nodes = 50

solve_day_23_puzzle(nic_program, num_nodes, debug_prints_level)
