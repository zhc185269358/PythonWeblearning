# ！/usr/bin/python3
# author:m1312
# -*- coding:utf-8 -*-
# @Time     : 2019/4/30 11:08
# @Author   : m1312
# @File     :mcts_for_RR.py
import random
import math

# example
# 顾客历史数据
# 格式:(l路段, 时间, 是否被分配)
# time :乘客发出请求的时间
# 需要大量历史数据支持
CUSTOMER_REQUEST = [['S' + str(i), random.randint(time, 1000), False] for i in range(1, 13) for time in range(0, 10)]

# 路段网络信息
ROAD_NETWORK = {
    'S1': {'DIS': 321, 'TIME': 60, 'NEIB': ['S5', 'S7']},
    'S2': {'DIS': 482, 'TIME': 120, 'NEIB': ['S1', 'S3', 'S4']},
    'S3': {'DIS': 160, 'TIME': 60, 'NEIB': []},
    'S4': {'DIS': 480, 'TIME': 80, 'NEIB': ['S5', 'S6', 'S7', 'S11']},
    'S5': {'DIS': 640, 'TIME': 180, 'NEIB': ['S11']},
    'S6': {'DIS': 600, 'TIME': 120, 'NEIB': []},
    'S7': {'DIS': 800, 'TIME': 120, 'NEIB': ['S8', 'S10']},
    'S8': {'DIS': 300, 'TIME': 120, 'NEIB': ['S9']},
    'S9': {'DIS': 1287, 'TIME': 240, 'NEIB': ['S10', 'S12']},
    'S10': {'DIS': 800, 'TIME': 120, 'NEIB': []},
    'S11': {'DIS': 960, 'TIME': 180, 'NEIB': ['S9']},
    'S12': {'DIS': 310, 'TIME': 100, 'NEIB': []}
}
# 模拟轮数
MAX_ROUND = 15

# -V 当整个搜索未找到乘客时奖励(惩罚)的最大值
V = 3000


class State():

    def __init__(self, name, distance, neighbours, travel_time):
        self.name = name
        self.distance = distance
        self.neighbours = neighbours
        # 当前路段需要花费的行车时间
        self.travel_time = travel_time
        # 记录出租车到当前路段行走的总时间
        self.car_time = 0

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_distance(self, distance):
        self.distance = distance

    def get_distance(self):
        return self.distance

    def set_travel_time(self, travel_time):
        self.travel_time = travel_time

    def get_travel_time(self):
        return self.travel_time

    def set_neighbours(self, neighbour):
        self.neighbours = neighbour

    def get_neighbours(self):
        return self.neighbours

    def set_car_time(self, car_time):
        self.car_time = car_time

    def get_car_time(self):
        return self.car_time

    def is_terminate(self):
        '''
        判断路段是否是Dead-End
        :return: 真值
        '''
        if self.neighbours == []:
            return True
        else:
            return False

    def found_customer(self, original_query_time):
        '''
        从查询时间起,判断是否找到乘客
        :param original_query_time: 司机初始请求的时间
        :return: True or False
        '''
        current_road_customer = [x for x in CUSTOMER_REQUEST if x[0] == self.name]
        for customer in current_road_customer:
            if original_query_time <= customer[1] <= self.car_time + original_query_time:
                if customer[2] is False:
                    customer[2] = True
                    return True
            else:
                return False


class Node():

    def __init__(self):
        self.state = None
        # 当前节点上一轮的Q值
        self.Q = 0
        self.visit_times = 0
        self.parent = None
        # 只有当节点被扩展过,才加入其中
        self.children = []

    def set_Q(self, quality):
        self.Q = quality

    def get_Q(self):
        return self.Q

    def set_visit_times(self, v):
        self.visit_times += v

    def get_visit_times(self):
        return self.visit_times

    def is_all_expanded(self):
        '''
        判断当前节点是否被完全扩展
        :return: True or False
        '''
        if len(self.children) is len(self.state.neighbours):
            return True
        else:
            return False


def basic_visit(node):
    '''
    从当前节点的未扩展的子节点中随机选择一个节点来扩展
    这个方法其实是一种变相的快速走子策略,以便在判断时,
    迅速得出一个结果
    :return: 子节点
    '''
    children_name_list = [children.state.name for children in node.children]
    not_expanded_nodes = [name for name in node.state.neighbours if name not in children_name_list]
    sub_node_name = random.choice(not_expanded_nodes)
    sub_node = expand(node, sub_node_name)
    node.children.append(sub_node)
    return sub_node


def expand(node, sub_node_name):
    '''
    根据当前节点以及所给的子节点名称,创建一个节点并添加进搜索树中
    :param node: 当前节点
    :param sub_node_name: 选定的子节点名称
    :return: 一个创建好的子节点
    '''
    sub_node = Node()
    sub_node.state = State(sub_node_name, ROAD_NETWORK[sub_node_name]['DIS'], ROAD_NETWORK[sub_node_name]['NEIB'],
                           ROAD_NETWORK[sub_node_name]['TIME'])
    sub_node.parent = node
    sub_node.state.set_car_time(sub_node.parent.state.get_car_time() + sub_node.state.get_travel_time())
    # 当扩展完成节点后,标志该节点已经被访问,访问次数 +1
    sub_node.set_visit_times(1)

    return sub_node


def ucb(node, r):
    '''
    基于当前游戏轮数和节点,计算选择最优子节点
    :param node: 当前节点
    :param r: 当前游戏轮数
    :return:
    '''
    # 一个系数
    c = 6
    # 所有的子节点计算的score都放在其中,以便比较
    marks = []
    for tuple_elem in list(enumerate(node.children)):
        '''
        使用内置函数,取出当前节点所有子节点的索引和元素,通过元素的Q计算score,然后将score和索引一起返回
        再取score的最大值对应索引的子节点即可
        '''
        left = tuple_elem[1].get_Q()
        right = math.log(r - 1) / tuple_elem[1].get_visit_times()
        score = left + c * math.sqrt(right)
        marks.append((score, tuple_elem[0]))
    print(f"marks:{marks}")
    # score最大的节点索引
    node_index = max(marks)[1]
    # 将score最大的索引对应的子节点返回回去
    node.children[node_index].set_visit_times(1)
    node.children[node_index].state.set_car_time(
        node.state.get_car_time() + node.children[node_index].state.get_travel_time())
    return node.children[node_index]


def create_query(segment, tmin, tmax):
    '''
    创建随机出租车请求函数
    :param segment:
    :param tmin: 下限
    :param tmax: 上限
    :return: 返回一个请求的元组
    '''
    query_time = random.randint(tmin, tmax)
    query = (segment, query_time)
    return query


def reset_customer_request(customer_requeset):
    for customer in customer_requeset:
        customer[2] = False
    return customer_requeset


def mcts(road_segments, history):
    road_segments = road_segments
    History = history
    tmin, tmax = History[0][1], History[len(History) - 1][1]

    for segment in road_segments:

        # 不是Dead-End 再判断是否找到乘客
        print("---------------------------------")
        print("当前:" + segment)
        all_shortest_road = []

        if ROAD_NETWORK[segment]['NEIB'] == []:
            start_node = Node()
            state = State(segment, ROAD_NETWORK[segment]['DIS'], ROAD_NETWORK[segment]['NEIB'],
                          ROAD_NETWORK[segment]['TIME'])
            start_node.state = state
            start_node.Q = -V
            start_node.set_visit_times(1)
            print("起始节点为死胡同,无法找到乘客,请返回")
            continue

        start_node = Node()
        state = State(segment, ROAD_NETWORK[segment]['DIS'], ROAD_NETWORK[segment]['NEIB'],
                      ROAD_NETWORK[segment]['TIME'])
        start_node.state = state
        start_node.set_visit_times(1)

        for i in range(1, MAX_ROUND + 1):
            reward = 0
            query = create_query(segment, tmin, tmax)
            print(f"当前请求{query} ")
            # 初始节点的判断,
            if start_node.is_all_expanded():
                print(f"{start_node.state.name}使用ucb策略", end='--->')
                sub_node = ucb(start_node, i)
                print(f"选择节点为{sub_node.state.name}")
            else:
                print(f"{start_node.state.name}使用基础策略", end='--->')
                sub_node = basic_visit(start_node)
                print(f"选择节点为{sub_node.state.name}")

            flag_node = sub_node
            shortest_road = []
            shortest_road.append(start_node)
            shortest_road.append(flag_node)
            while flag_node.state.is_terminate() is False:
                # 放在最前面的意思是说
                # 从发起点开始的子节点就开始记录路段R,直到找到乘客为止
                # 扩展或者选定一个子节点后,都要进行记录
                if flag_node.state.found_customer(query[1]):
                    print(f"在{flag_node.state.name} 找到乘客")
                    for road in shortest_road:
                        reward += -(road.state.get_distance() / i)
                    for road in shortest_road:
                        road.Q = reward
                    all_shortest_road.append(shortest_road)
                    print("此时所走路段的Q值:")
                    for r in shortest_road:
                        print(f"{r.state.name}的Q: {r.Q}", end=' ')
                    print()
                    # 当找到乘客后,便确定了最短距离.因为在found_customer方法中,已经对已分配的乘客做了判断
                    break
                # 未找到乘客
                elif flag_node.state.is_terminate() is False:
                    # 先设置Q为 -V,如果找到乘客,则设置计算结果,若最终未找到,就为-V
                    flag_node.Q = -V
                    #  在未找到乘客时,
                    # 该路段并非死胡同,但未找到乘客,相当于在这个路段重新发起一次新的请求
                    if flag_node.is_all_expanded():
                        print(f"{flag_node.state.name}使用ucb策略", end='--->')
                        flag_node = ucb(flag_node, i)
                        shortest_road.append(flag_node)
                        print(f"选择节点为{flag_node.state.name}")
                    else:
                        print(f"{flag_node.state.name}使用基础策略", end='--->')
                        flag_node = basic_visit(flag_node)
                        shortest_road.append(flag_node)
                        print(f"选择节点为{flag_node.state.name}")
            else:
                flag_node.Q = -V
                print(f"到达Dead-END")
                for r in shortest_road:
                    print(f"{r.state.name}的Q: {r.Q}", end=' ')
                print()

        # 当以新路段为起点时,重置所有的客户请求分配情况
        reset_customer_request(CUSTOMER_REQUEST)

        print(f"以{start_node.state.name}为起点的出租车行驶路段:")
        for short in all_shortest_road:
            for road in short:
                print(road.state.name, end=' ')
            print()

    # return all_shortest_road


if __name__ == '__main__':
    road_segments = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12']
    History = sorted(CUSTOMER_REQUEST, key=lambda x: (x[1], x[0]))
    mcts(road_segments, History)
