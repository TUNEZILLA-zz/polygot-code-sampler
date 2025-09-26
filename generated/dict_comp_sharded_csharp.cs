using System;
using System.Collections.Generic;
using System.Linq;

public static class Program
{
    public static Dictionary<int, int> Execute()
    {
        return Enumerable.Range(1, 99999).Where(x => x % 3 == 0).ToDictionary(x => x, x => x * x);
    }
}
