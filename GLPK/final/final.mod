/* Define the sets */
set NODES;
set ARCS within {i in NODES, j in NODES};

/* Parameters for capacities and costs */
param capacity {i in NODES, j in NODES};
param cost {i in NODES, j in NODES};

/* Parameters for supply/demand */
param supplyA {i in NODES} default 0;
param supplyB {i in NODES} default 0;
/* Decision variables for flow of A and B */
var fA {i in NODES, j in NODES} >= 0, <= capacity[i,j];
var fB {i in NODES, j in NODES} >= 0, <= capacity[i,j];
/* Objective function */
minimize total_cost: sum {(i,j) in ARCS} cost[i,j] * (fA[i,j] + fB[i,j]);

/* Constraints */
s.t. capacity_constr {(i,j) in ARCS}: fA[i,j] + fB[i,j] <= capacity[i,j];
s.t. flow_balanceA {i in NODES}: sum {(i,j) in ARCS} fA[i,j] - sum {(j,i) in ARCS} fA[j,i] = supplyA[i];
s.t. flow_balanceB {i in NODES}: sum {(i,j) in ARCS} fB[i,j] - sum {(j,i) in ARCS} fB[j,i] = supplyB[i];

/* Solve the problem */
solve;
/* Display results */
