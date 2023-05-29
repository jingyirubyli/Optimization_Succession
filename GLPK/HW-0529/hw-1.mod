
/* hw-1.mod */

var a >= 0;
var b >= 0;
var c >= 0;
var d >= 0;

minimize z : 5*a + 7.5*b + 3.75*c + 2.5*d;
s.t. protein: 0.18*a +0.31*b + 0.12*c + 0.18*d >= 18;
s.t. carbohydrate: 0.43*a +0.25*b + 0.12*c + 0.5*d >= 31;
s.t. fat: 0.31*a +0.37*b + 0.37*c + 0.12*d >= 25;

end;