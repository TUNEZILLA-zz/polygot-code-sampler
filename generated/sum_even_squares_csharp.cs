using System;
using System.Collections.Generic;
using System.Linq;

public static class Program
{
    public static int Execute()
    {
        return Enumerable.Range(1, 999999).Where(i => i % 2 == 0).Sum(i => i * i);
    }
}
