set NUM;

param OUTPUT_NUM {i in NUM};
param A_PRICE {i in NUM};
param B_PRICE {i in NUM};
param C_PRICE {i in NUM};
param D_PRICE {i in NUM};


var x{i in NUM}, >= 0;

maximize OUTPUT: sum{i in NUM}
OUTPUT_NUM[i]*x[i];


s.t. A: sum{i in NUM} A_PRICE[i]*x[i] <= 5; 
s.t. B: sum{i in NUM} B_PRICE[i]*x[i] <= 7.5;
s.t. C: sum{i in NUM} C_PRICE[i]*x[i] <= 3.75;
s.t. D: sum{i in NUM} D_PRICE[i]*x[i] <= 2.5;


end;