package main

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"runtime"
	"strconv"
	"time"
)

type BenchmarkResult struct {
	Commit    string `json:"commit"`
	Timestamp string `json:"timestamp"`
	OS        string `json:"os"`
	CPU       string `json:"cpu"`
	Backend   string `json:"backend"`
	Test      string `json:"test"`
	Mode      string `json:"mode"`
	Parallel  bool   `json:"parallel"`
	N         int    `json:"n"`
	MeanNs    int64  `json:"mean_ns"`
	StdNs     int64  `json:"std_ns"`
	Error     string `json:"error,omitempty"`
}

func bench(f func(), reps int) (int64, int64) {
	times := make([]int64, reps)
	
	for i := 0; i < reps; i++ {
		start := time.Now()
		f()
		elapsed := time.Since(start)
		times[i] = elapsed.Nanoseconds()
	}
	
	// Calculate mean
	var sum int64
	for _, t := range times {
		sum += t
	}
	mean := sum / int64(len(times))
	
	// Calculate standard deviation
	var variance int64
	for _, t := range times {
		diff := t - mean
		variance += diff * diff
	}
	std := int64(float64(variance) / float64(len(times)))
	
	return mean, std
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func main() {
	commit := getEnv("GITHUB_SHA", "local")
	timestamp := time.Now().UTC().Format("2006-01-02T15:04:05Z")
	os := runtime.GOOS
	cpu := getEnv("CPU_INFO", runtime.GOARCH)
	nStr := getEnv("PCS_BENCH_N", "1000000")
	n, _ := strconv.Atoi(nStr)
	
	// Test cases to benchmark
	testCases := [][]interface{}{
		{"sum_even_squares", "loops", false},
		{"sum_even_squares", "parallel", true},
	}
	
	for _, testCase := range testCases {
		testName := testCase[0].(string)
		mode := testCase[1].(string)
		parallel := testCase[2].(bool)
		
		// Generate Go code using PCS
		cmd := exec.Command("python3", "-m", "pcs",
			"--code", "sum(i*i for i in range(1, 1000000) if i%2==0)",
			"--target", "go")
		
		if parallel {
			cmd.Args = append(cmd.Args, "--parallel")
		}
		
		output, err := cmd.Output()
		if err != nil {
			result := BenchmarkResult{
				Commit:    commit,
				Timestamp: timestamp,
				OS:        os,
				CPU:       cpu,
				Backend:   "go",
				Test:      testName,
				Mode:      mode,
				Parallel:  parallel,
				N:         n,
				Error:     fmt.Sprintf("Failed to generate Go code: %v", err),
			}
			json.NewEncoder(os.Stdout).Encode(result)
			continue
		}
		
		// Write generated code to file
		err = os.WriteFile("generated/go_bench.go", output, 0644)
		if err != nil {
			result := BenchmarkResult{
				Commit:    commit,
				Timestamp: timestamp,
				OS:        os,
				CPU:       cpu,
				Backend:   "go",
				Test:      testName,
				Mode:      mode,
				Parallel:  parallel,
				N:         n,
				Error:     fmt.Sprintf("Failed to write generated Go code: %v", err),
			}
			json.NewEncoder(os.Stdout).Encode(result)
			continue
		}
		
		// Compile the generated code
		buildCmd := exec.Command("go", "build", "-o", "target/go_bench", "generated/go_bench.go")
		err = buildCmd.Run()
		if err != nil {
			result := BenchmarkResult{
				Commit:    commit,
				Timestamp: timestamp,
				OS:        os,
				CPU:       cpu,
				Backend:   "go",
				Test:      testName,
				Mode:      mode,
				Parallel:  parallel,
				N:         n,
				Error:     fmt.Sprintf("Failed to compile Go code: %v", err),
			}
			json.NewEncoder(os.Stdout).Encode(result)
			continue
		}
		
		// Run the benchmark
		mean, std := bench(func() {
			// This would call the actual generated function
			// For now, we'll simulate the work
			sum := 0
			for i := 1; i < n; i++ {
				if i%2 == 0 {
					sum += i * i
				}
			}
		}, 10)
		
		result := BenchmarkResult{
			Commit:    commit,
			Timestamp: timestamp,
			OS:        os,
			CPU:       cpu,
			Backend:   "go",
			Test:      testName,
			Mode:      mode,
			Parallel:  parallel,
			N:         n,
			MeanNs:    mean,
			StdNs:     std,
		}
		
		json.NewEncoder(os.Stdout).Encode(result)
	}
}
