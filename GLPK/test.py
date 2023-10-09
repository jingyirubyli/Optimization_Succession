import numpy as np
import matplotlib.pyplot as plt  # 导入 Matplotlib 工具包
import networkx as nx  # 导入 NetworkX 工具包
import pulp      # 导入 pulp库

# 5. 多商品流问题 (Multi-commodity Flow Problem)
# 5.1 创建有向图
G2 = nx.DiGraph()  # 创建一个有向图 DiGraph
G2.add_edges_from([('v0','v1',{'capacity': 7, 'weight': 4}),
                  ('v0','v2',{'capacity': 8, 'weight': 4}),
                  ('v1','v3',{'capacity': 9, 'weight': 1}),
                  ('v2','v1',{'capacity': 5, 'weight': 5}),
                  ('v2','v4',{'capacity': 9, 'weight': 4}),
                  ('v3','v4',{'capacity': 6, 'weight': 2}),
                  ('v3','v5',{'capacity': 10, 'weight': 6}),
                  ('v3','v6',{'capacity': 10, 'weight': 6}),
                  ('v4','v1',{'capacity': 2, 'weight': 1}),
                  ('v4','v5',{'capacity': 5, 'weight': 2}),
                  ('v4','v6',{'capacity': 5, 'weight': 2})]) # 添加边的属性 'capacity', 'weight'
pos={'v0':(0,5),'v1':(4,2),'v2':(4,8),'v3':(10,2),'v4':(10,8),'v5':(15,3),'v6':(15,7)}  # 指定顶点绘图位置

supplyA = 6.0  # 商品 A 供应量
supplyB = 5.0  # 商品 B 供应量
print("Supply A:{}\tSupply B:{}".format(supplyA,supplyB))

# 整理边的标签
edgeLabel1 = nx.get_edge_attributes(G2, 'capacity')
edgeLabel2 = nx.get_edge_attributes(G2, 'weight')
edgeLabel = {}
for i in edgeLabel1.keys():
    edgeLabel[i] = f'({edgeLabel1[i]:},{edgeLabel2[i]:})'  # 边的(容量，成本)

# 5.2 绘制有向网络图
fig, ax = plt.subplots(figsize=(8,6))
nx.draw(G2,pos,with_labels=True,node_color='skyblue',node_size=400,font_size=10)   # 绘制有向图，显示顶点标签
nx.draw_networkx_nodes(G2, pos, nodelist=['v0'], node_color='orange',node_size=400)  # 设置指定顶点的颜色、宽度
nx.draw_networkx_nodes(G2, pos, nodelist=['v5','v6'], node_color='c',node_size=400)  # 设置指定顶点的颜色、宽度
nx.draw_networkx_edge_labels(G2,pos,edgeLabel,font_size=10)  # 显示边的标签：'capacity','weight'
ax.set_title("Multi-Communication Data Traffic Problem")
ax.text(-1.8,5.2,"A:{}".format(supplyA),color='m')
ax.text(-1.8,4.6,"B:{}".format(supplyB),color='navy')
ax.text(15.8,7.0,"A:{}".format(supplyA),color='m')
ax.text(15.8,2.8,"B:{}".format(supplyB),color='navy')
plt.xlim(-3, 18)
plt.ylim(1, 9)
plt.axis('on')
# plt.show(YouCans-XUPT)

# 5.3  用 PuLP 求解多商品流最小费用问题 (Multi-commodity Flow Problem YouCans-XUPT)
edgeWeight = nx.get_edge_attributes(G2, 'weight')  # 'weight', 单位流量的成本
edgeCapacity = nx.get_edge_attributes(G2, 'capacity')  # 'capacity', 边的容量
maxCapacity = max(edgeCapacity.values())  # 边的容量的最大值
print(edgeWeight)
print("max(Weight)",max(edgeWeight.values()))
print("max(Capacity)",max(edgeCapacity.values()))

# (1) 建立优化问题 MCFproblem: 求最小值(LpMinimize)
MCFproblem = pulp.LpProblem("MultiCommodityFlowProb", sense=pulp.LpMinimize)  # 定义问题，求最小值

# (2) 定义决策变量 fA(edges), fB(edges)
# itemsG2 = ["A","B"]  # 商品种类
fA = pulp.LpVariable.dicts("FlowA", G2.edges(), lowBound=0.0, upBound=maxCapacity, cat='Continuous')
fB = pulp.LpVariable.dicts("FlowB", G2.edges(), lowBound=0.0, upBound=maxCapacity, cat='Continuous')
print(fA)
print(fB)

# (3). 设置目标函数
MCFproblem += pulp.lpSum([edgeWeight[edge] * (fA[edge]+fB[edge]) for edge in G2.edges])  # 总运输费用

# (4) 设置约束条件
for edge in G2.edges:  # 边的最大流量约束
    MCFproblem += (fA[edge] + fB[edge] - edgeCapacity[edge] <= 0)  # edgeCapacity[edge], 边的容量

for node in G2.nodes:  # 顶点的净流量约束
    if G2.in_degree(node) == 0:  # 入度为 0，判断是否为源点
        print("源点：{}, 出边：{}".format(node,G2.out_edges(nbunch=node)))
        MCFproblem += (sum(fA[edge] for edge in G2.out_edges(nbunch=node)) <= supplyA)  # A 供应量约束
        MCFproblem += (sum(fB[edge] for edge in G2.out_edges(nbunch=node)) <= supplyB)  # B 供应量约束
    elif G2.out_degree(node) == 0:  # 出度为 0，判断是否为汇点
        print("汇点：{}, 入边：{}".format(node,G2.in_edges(nbunch=node)))
        if node=='v6':  # 题目条件, v6 需求为 B
            MCFproblem += (sum(fA[edge] for edge in G2.in_edges(nbunch=node)) == supplyA)  # A 需求量约束
        if node=='v5':  # 题目条件, v5 需求为 A
            MCFproblem += (sum(fB[edge] for edge in G2.in_edges(nbunch=node)) == supplyB)  # B 需求量约束
    else:  # 中间节点，每种商品都是流量平衡
        print("中间点：{}, 入边：{}, 出边：{}".format(node,G2.in_edges(nbunch=node),G2.out_edges(nbunch=node)))
        MCFproblem += (sum(fA[edge1] for edge1 in G2.out_edges(nbunch=node))
                       - sum(fA[edge2] for edge2 in G2.in_edges(nbunch=node)) == 0)  # 总流出 = 总流入
        MCFproblem += (sum(fB[edge1] for edge1 in G2.out_edges(nbunch=node))
                       - sum(fB[edge2] for edge2 in G2.in_edges(nbunch=node)) == 0)  # 总流出 = 总流入
# (5) 求解线性规划问题
MCFproblem.solve()

# 绘制商品A的流量信息
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# 绘制商品A的流量图
nx.draw(G2, pos, with_labels=True, node_color='skyblue', node_size=400, font_size=10, ax=ax1)
nx.draw_networkx_nodes(G2, pos, nodelist=['v0'], node_color='orange', node_size=400, ax=ax1)
nx.draw_networkx_nodes(G2, pos, nodelist=['v5', 'v6'], node_color='c', node_size=400, ax=ax1)
nx.draw_networkx_edge_labels(G2, pos, edgeLabel, font_size=10, ax=ax1)
edgeLabelA = {edge: f'A:{fA[edge].varValue:.1f}' for edge in G2.edges}
nx.draw_networkx_edge_labels(G2, pos, edgeLabelA, font_color='m', font_size=8, ax=ax1)
ax1.set_title("Flow of Data A")
ax1.text(-1.8, 5.2, "A:{}".format(supplyA), color='m')
ax1.text(15.8, 7.0, "A:{}".format(supplyA), color='m')
ax1.set_xlim(-3, 18)
ax1.set_ylim(1, 9)
ax1.axis('on')

# 绘制商品B的流量信息
nx.draw(G2, pos, with_labels=True, node_color='skyblue', node_size=400, font_size=10, ax=ax2)
nx.draw_networkx_nodes(G2, pos, nodelist=['v0'], node_color='orange', node_size=400, ax=ax2)
nx.draw_networkx_nodes(G2, pos, nodelist=['v5', 'v6'], node_color='c', node_size=400, ax=ax2)
nx.draw_networkx_edge_labels(G2, pos, edgeLabel, font_size=10, ax=ax2)
edgeLabelB = {edge: f'B:{fB[edge].varValue:.1f}' for edge in G2.edges}
nx.draw_networkx_edge_labels(G2, pos, edgeLabelB, font_color='navy', font_size=8, ax=ax2)
ax2.set_title("Flow of Data B")
ax2.text(-1.8, 4.6, "B:{}".format(supplyB), color='navy')
ax2.text(15.8, 2.8, "B:{}".format(supplyB), color='navy')
ax2.set_xlim(-3, 18)
ax2.set_ylim(1, 9)
ax2.axis('on')

plt.tight_layout()
plt.show()

# (6) 输出优化结果
print("2. PuLP 线性规划（最小费用的优化结果）：")  # PuLP 工具包
print(MCFproblem)  # 输出问题设定参数和条件
print("Optimization result")  # PuLP 工具包
for v in MCFproblem.variables():
    print(v.name, " = ", v.varValue)  # 输出每个变量的最优值
print("\n最小运输费用 = ", pulp.value(MCFproblem.objective))  # 输出最优解的目标函数值
plt.show()