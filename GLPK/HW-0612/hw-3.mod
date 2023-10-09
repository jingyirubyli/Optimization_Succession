
param K integer,>0;
param N integer,>0;
param p integer,>0;
param q integer,>0;

set V:=1..N;
set E within {V, V};
set M:=1..K;

param cost{E};

var x{E,M} binary;

minimize PATH_COST: sum{k in M} sum{i in V} (sum{j in V} (cost[i,j]*x[i,j,k]));

s.t. INTERNAL{i in V, k in M: i!=p && i!=q && p != q}:sum{j in V}(x[i,j,k])-sum{j in V}(x[j,i,k])=0;
s.t. SOURCE{i in V, k in M: i=p && p != q}:sum{j in V}(x[i,j,k])-sum{j in V}(x[j,i,k])=1;
s.t. DISJOINT{i in V, j in V, k1 in M, k2 in M: k1 != k2}: x[i,j,k1]+x[j,i,k2]<=1;
s.t. DISJOINT_NODE{i in V: i != p && i!=q&& p!=q}: sum{j in V} sum{k in M}(x[i,j,k])<=1;

end;