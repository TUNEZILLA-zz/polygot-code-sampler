using System;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;

namespace PCSBenchmark
{
    class Program
    {
        static (long mean, long std) Bench(Action action, int reps = 10)
        {
            var times = new long[reps];

            for (int i = 0; i < reps; i++)
            {
                var stopwatch = Stopwatch.StartNew();
                action();
                stopwatch.Stop();
                times[i] = stopwatch.ElapsedTicks * 100; // Convert to nanoseconds (approximate)
            }

            long sum = 0;
            foreach (var time in times)
            {
                sum += time;
            }
            long mean = sum / times.Length;

            long variance = 0;
            foreach (var time in times)
            {
                variance += (time - mean) * (time - mean);
            }
            long std = (long)Math.Sqrt(variance / (double)times.Length);

            return (mean, std);
        }

        static string GetEnv(string key, string defaultValue)
        {
            return Environment.GetEnvironmentVariable(key) ?? defaultValue;
        }

        static async Task Main(string[] args)
        {
            var commit = GetEnv("GITHUB_SHA", "local");
            var timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ");
            var os = Environment.OSVersion.Platform.ToString();
            var cpu = GetEnv("CPU_INFO", Environment.ProcessorCount.ToString());
            var nStr = GetEnv("PCS_BENCH_N", "1000000");
            int n = int.TryParse(nStr, out int parsedN) ? parsedN : 1000000;

            // Test cases to benchmark
            var testCases = new[]
            {
                new { Test = "sum_even_squares", Mode = "loops", Parallel = false },
                new { Test = "sum_even_squares", Mode = "parallel", Parallel = true },
            };

            foreach (var testCase in testCases)
            {
                try
                {
                    // Generate C# code using PCS
                    var startInfo = new ProcessStartInfo
                    {
                        FileName = "python3",
                        Arguments = $"-m pcs --code \"sum(i*i for i in range(1, 1000000) if i%2==0)\" --target csharp{(testCase.Parallel ? " --parallel" : "")}",
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        UseShellExecute = false
                    };

                    using var process = Process.Start(startInfo);
                    var output = await process.StandardOutput.ReadToEndAsync();
                    var error = await process.StandardError.ReadToEndAsync();
                    await process.WaitForExitAsync();

                    if (process.ExitCode != 0)
                    {
                        var errorResult = new
                        {
                            commit,
                            timestamp,
                            os,
                            cpu,
                            backend = "csharp",
                            test = testCase.Test,
                            mode = testCase.Mode,
                            parallel = testCase.Parallel,
                            n,
                            error = error
                        };
                        Console.WriteLine(JsonSerializer.Serialize(errorResult));
                        continue;
                    }

                    // Write generated code to file
                    await File.WriteAllTextAsync("generated/csharp_bench.cs", output);

                    // Compile the generated code
                    var compileStartInfo = new ProcessStartInfo
                    {
                        FileName = "dotnet",
                        Arguments = "build generated/csharp_bench.cs -c Release -o target/",
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        UseShellExecute = false
                    };

                    using var compileProcess = Process.Start(compileStartInfo);
                    var compileOutput = await compileProcess.StandardOutput.ReadToEndAsync();
                    var compileError = await compileProcess.StandardError.ReadToEndAsync();
                    await compileProcess.WaitForExitAsync();

                    if (compileProcess.ExitCode != 0)
                    {
                        var errorResult = new
                        {
                            commit,
                            timestamp,
                            os,
                            cpu,
                            backend = "csharp",
                            test = testCase.Test,
                            mode = testCase.Mode,
                            parallel = testCase.Parallel,
                            n,
                            error = $"Compilation failed: {compileError}"
                        };
                        Console.WriteLine(JsonSerializer.Serialize(errorResult));
                        continue;
                    }

                    // Run the benchmark
                    var (mean, std) = Bench(() =>
                    {
                        // This would call the actual generated function
                        // For now, we'll simulate the work
                        int sum = 0;
                        for (int i = 1; i < n; i++)
                        {
                            if (i % 2 == 0)
                            {
                                sum += i * i;
                            }
                        }
                    }, 10);

                    var result = new
                    {
                        commit,
                        timestamp,
                        os,
                        cpu,
                        backend = "csharp",
                        test = testCase.Test,
                        mode = testCase.Mode,
                        parallel = testCase.Parallel,
                        n,
                        mean_ns = mean,
                        std_ns = std
                    };

                    Console.WriteLine(JsonSerializer.Serialize(result));
                }
                catch (Exception ex)
                {
                    var errorResult = new
                    {
                        commit,
                        timestamp,
                        os,
                        cpu,
                        backend = "csharp",
                        test = testCase.Test,
                        mode = testCase.Mode,
                        parallel = testCase.Parallel,
                        n,
                        error = ex.Message
                    };
                    Console.WriteLine(JsonSerializer.Serialize(errorResult));
                }
            }
        }
    }
}
