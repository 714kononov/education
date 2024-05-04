using System;
using System.IO;

class Program
{
    static void Main()
    {
        string filePath = "/Users/admin/Downloads/+C.cs";

        try
        {
            using (StreamReader sr = new StreamReader(filePath))
            {
                string line;
                while ((line = sr.ReadLine()) != null)
                {
                    Console.WriteLine(line);
                }
            }
        }
        catch (IOException e)
        {
            Console.WriteLine("Unable to open file: " + e.Message);
        }
    }
}
