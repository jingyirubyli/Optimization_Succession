param N integer, >0;

set V:=1..N;
set E within {V,V};

param c{V,V};
param T{V,V};

var x{V,V,V,V}, >=0, <=1;
var r, >=0, <=1;

s.t. Flow1{p in V, q in V, i in V: i=p && q!=p}: 
    sum{j in V:j!=i} x[p,q,i,j]-sum{j in V:j!=i} x[p,q,j,i]=1;
s.t. Flow2{p in V,q in V, i in V: i!=p && i!=q&& q!=p}: 
    sum{j in V:j!=i} x[p,q,i,j]-sum{j in V:j!=i} x[p,q,j,i]=0;
s.t. Capa{i in V, j in V:j!=i}: 
    sum{p in V} sum{q in V:q!=p}(T[p,q]*x[p,q,i,j])<=c[i,j]*r;


minimize CONGEATION:r;
