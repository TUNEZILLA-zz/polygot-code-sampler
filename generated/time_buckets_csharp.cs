using System;
using System.Collections.Generic;
using System.Linq;

public static class Program
{
    public static int Execute()
    {
        return Enumerable.Range(0, 1000).Sum(i => len([x for x in range(10000) if (x + i) % 1000 == 0]));
    }
}
