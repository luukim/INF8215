include "globals.mzn";

int: n_object;
array[1..n_object,1..2] of int: shape; % (x,y) shape of each object
int: max_length;
int: max_width;

array[1..n_object] of var 0..max_length: X; %origin of shape x
array[1..n_object] of var 0..max_width: Y; %origin of shape y

var int: length_used;
var int: width_used;
var int: area = (X[arg_max(X)] + shape[arg_max(X), 1])*(Y[arg_max(Y)] + shape[arg_max(Y), 2]);

function int: no_overlap_x(int: x1, int:x2) = x1 - x2;


constraint forall(i in 1..n_object)(shape[i,1] <= max_length /\ shape[i,1] <= max_width);
% non overlap
constraint forall(i in 1..n_object, j in 1..n_object where i < j)
                 (X[i] + shape[i,1] <= X[j] \/
                  X[j] + shape[j,1] <= X[i] \/  
                  Y[i] + shape[i,2] <= Y[j] \/ 
                  Y[j] + shape[j,2] <= Y[i]);
                  
constraint forall(i in 1..n_object)(X[i] + shape[i,1] <= max_length);
constraint forall(i in 1..n_object)(Y[i] + shape[i,2] <= max_width);

solve :: seq_search([
         int_search([area,max_length,max_width], input_order, indomain_min, complete)]) minimize  area;



output
["length used: ", show(X[arg_max(X)] + shape[arg_max(X), 1]), "\n" ]++
["length used: ", show(Y[arg_max(Y)] + shape[arg_max(Y), 2]), "\n" ]++
["Area used: ", show(area), "\n" ] ++
["x = ", show(X), "\n"] ++
["y = ", show(Y), "\n"];
