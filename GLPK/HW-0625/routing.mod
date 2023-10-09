set POINTS;
set LINKS within POINTS cross POINTS;

param C{LINKS}; 
param T{POINTS, POINTS}; 
param p; 

var x{LINKS} >= 0; 

minimize CongestionRatio:
    sum{(i,j) in LINKS}(x[i,j] + x[j,i]) / C[i,j];

subject to FlowConservation{i in POINTS: i != p}:
    sum{j in POINTS: j != i}(x[i,j] - x[j,i]) = 0;

subject to LinkCapacity{(i,j) in LINKS}:
    x[i,j] + x[j,i] <= C[i,j];

subject to NonNegativity{(i,j) in LINKS}:
    x[i,j] >= 0;

subject to TriangleFormation{(i,j) in LINKS: (i,j) not in LINKS}:
    x[i,j] = 0;

