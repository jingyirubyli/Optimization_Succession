set MAT;

param COST_MAT {i in MAT};
param PROTEIN_MAT {i in MAT};
param CARBOHYDRATE_MAT {i in MAT};
param FAT_MAT {i in MAT};

var x{i in MAT}, >= 0;

minimize COST: sum{i in MAT}
COST_MAT[i]*x[i];


s.t. PROTEIN: sum{i in MAT} PROTEIN_MAT[i]*x[i]>=18;
s.t. CARBOHYDRATE: sum{i in MAT} CARBOHYDRATE_MAT[i]*x[i]>=31;
s.t. FAT: sum{i in MAT} FAT_MAT[i]*x[i]>=25;

end;