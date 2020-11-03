
include "globals.mzn"; 
   
% Parameters of the problems
int: n = 5;
array[1..n] of int: left_vision = [2,1,3,2,3];
array[1..n] of int: right_vision = [3,4,1,3,2];
array[1..n] of int: up_vision = [2,1,3,2,2];
array[1..n] of int: down_vision = [3,4,2,1,2];

% Variable: value for each cell
array[1..n,1..n] of var 1..n: city;

constraint forall(i in 1..n)(alldifferent(row(city,i)));
constraint forall(i in 1..n)(alldifferent(col(city,i)));

constraint forall(i in 1..n)(if left_vision[i] = 1 then city[1,i] = 5 endif);
constraint forall(i in 1..n)(if right_vision[i] = 1 then city[5,i] = 5 endif);
constraint forall(i in 1..n)(if up_vision[i] = 1 then city[i,1] = 5 endif);
constraint forall(i in 1..n)(if down_vision[i] = 1 then city[i,5] = 5 endif);

constraint forall(i in 1..n)(if left_vision[i] = 4 \/ left_vision[i] = 3 then city[1,i] != 4 /\ city[1,i] != 5 endif);
constraint forall(i in 1..n)(if right_vision[i] = 4 \/ right_vision[i] = 3 then city[5,i] != 4 /\ city[5,i] != 5 endif);
constraint forall(i in 1..n)(if up_vision[i] = 4 \/ up_vision[i] = 3 then city[i,1] != 4 /\ city[i,1] != 5 endif);
constraint forall(i in 1..n)(if down_vision[i] = 4 \/ down_vision[i] = 3 then city[i,5] != 4 /\ city[i,5] != 5 endif);

constraint forall(i in 1..n)(if down_vision[i] = 4 then city[i,4] != 4 endif);
constraint forall(i in 1..n)(if right_vision[i] = 4 then city[4,i] != 4 endif);

constraint forall(i in 1..n-1, j in 1..n-1)(if city[i+1,j] = 5 /\ city[i,j+1] = 5 /\ i = 1 then city[i,j] != 4 endif);

output
["city:"]++
[
  if j = 1 then "\n" else " " endif ++
    show(city[j,i])
  | i in 1..n, j in 1..n
];
