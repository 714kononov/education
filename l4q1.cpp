#include <iostream>

using namespace std;


#define SIZE 14

int max(int *arr);
int sort(int *a);
int main()
{
  int arr[SIZE];
  for(int i = 0; i < SIZE ; i++)
  {
    cout << "Введите элемент массива ["<<i<<"]: ";
    cin >> arr[i];
  }
  cout <<"Макс.значение массива: "<< max(arr)<<endl;
    cout<<"Отсортированный массив на половину: "<<endl;
    sort(arr);
    for(int i = 0 ; i < SIZE ; i++)
    {
      cout<<arr[i]<<" ";
    }
}

int max(int *arr)
{
  int max = arr[0];
  for(int i = 0 ; i < SIZE ; i++)
  {
    if(arr[i]>max)max = arr[i];
  }
  return max;
}

int sort(int *a)
{
  int min = 0; 
  int buf = 0; 
  for (int i = 0; i < SIZE/2; i++)
  {
      min = i; 
      for (int j = i + 1; j < SIZE /2; j++)
        if( a[j] < a[min] )min = j;
        else min = min;
        if (i != min)
        {
          buf = a[i];
          a[i] = a[min];
          a[min] = buf;
        }
  }
  return 0;
}