include "globals.mzn"; 

int: n;
array[1..n, 1..n] of var 0..1: grid; % var is used in order to take into account the "not-bounded case" _
 
% decision variables: mine or not on the specific cell
array[1..n, 1..n] of var 0..1: x;

% initializing the grid: '_' values on the grid correspond to variables not already set (i.e. the choices you have to make)
constraint forall(i in 1..n, j in 1..n)(x[i,j] = grid[i,j]);
            
% 1. Pour chaque ligne et colonne, le nombre de cases avec et sans mine doit être identique.

% Étant donnée une grille n x n , le nombre de mine pour les lignes = le nombre de mine pour les colonnes
% constraint forall(i in 1..n, j in 1..n)( 
%            sum(c in 1..n)(x[c,j] = 1) = sum(c in 1..n)(x[i,c]=1) );
                    
constraint forall(i in 1..n-1)(
                sum(c in 1..n)(x[c,i] = 1) = sum(c in 1..n)(x[c,i+1]=1)
           ); 

constraint forall(i in 1..n-1)(
                sum(c in 1..n)(x[i,c] = 1) = sum(c in 1..n)(x[i+1,c]=1)
           ); 

% 2 Pour chaque ligne et colonne, Il ne peut pas y avoir plus de deux cases consécutives sans mine.
% 3. Pour chaque ligne et colonne, Il ne peut pas y avoir plus de deux cases consécutives avec mine.

constraint forall(i in 1..n, j in 1..n-2)(
                if(x[i,j] = x[i,j+1]) 
                  then (x[i,j+2] != x[i,j]) 
                endif 
           );        
              
constraint forall(i in 1..n-2, j in 1..n)(
                if(x[i,j] = x[i+1,j])
                  then (x[i+2,j] != x[i,j])
                endif
           ); 
                       
% 4. Il ne peut pas y avoir deux lignes identiques (i.e., ayant des mines exactement au même endroit).

constraint forall(i in 1..n)(
                  forall(j in 1..n)(
                  if (i != j)
                      then row(x,i) != row(x,j) 
                  endif
));

% % % 5. Il ne peut pas y avoir deux colonnes identiques (i.e., ayant des mines exactement au même endroit).

constraint forall(i in 1..n)(
                  forall(j in 1..n)(
                  if (i != j )
                      then col(x,i) != col(x,j) 
                  endif
));

% 6. Pour certaines cases, vous avez l’information exacte de s’il y a une mine ou non.

output [
   if j = 1 then "\n" else " " endif ++
     show(x[i,j])
   | i,j in 1..n
];