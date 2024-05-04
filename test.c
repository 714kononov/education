#include <stdio.h>
#include <stdlib.h>


int function(int x , int y , int z);
int factorial (int n);

int main()
{
  printf("%d",345);
}
// Найти максимум минимум функции от трех элементов f(x,y,z) = xyz + x + y + z;
// Метод множителей Ланграджа

int function(int x , int y , int z)
{
  return x*y*z + x + y + z;
}