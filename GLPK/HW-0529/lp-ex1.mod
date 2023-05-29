
/* lp-ex1.mod */

var x >= 0;
var y >= 0;

maximize z : x+y ;
s.t. st1: 5*x+3*y <= 15;
s.t. st2: x-y <=2;
s.t. st3: y <=3;

end;