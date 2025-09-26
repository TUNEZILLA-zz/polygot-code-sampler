using System;
using System.Collections.Generic;
using System.Linq;

public static class Program
{
    public static int Execute()
    {
        return Enumerable.Range(1, 999).Where(x => x % 3 == 0).Sum(x => sum((x * y for y in range(1, 100) if y % 2 == 0)));
    }
}
