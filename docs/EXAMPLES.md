# 📚 Real-World Examples

This document showcases practical examples of Polyglot Code Sampler in real-world scenarios, demonstrating how Python comprehensions can be transformed into optimized code across different ecosystems.

## 🏢 Business Applications

### Customer Data Processing

**Python Input:**
```python
# Process active customers with high scores
active_customers = [
    customer.name for customer in customers
    if customer.status == 'active' and customer.score > 80
]
```

**Generated Rust:**
```rust
use rayon::prelude::*;

pub fn get_active_customers(customers: &[Customer]) -> Vec<String> {
    customers.into_par_iter()
        .filter(|customer| customer.status == "active")
        .filter(|customer| customer.score > 80)
        .map(|customer| customer.name.clone())
        .collect()
}
```

**Generated SQL:**
```sql
SELECT name
FROM customers
WHERE status = 'active'
  AND score > 80;
```

### Financial Calculations

**Python Input:**
```python
# Calculate portfolio returns
returns = [
    (stock.price - stock.purchase_price) / stock.purchase_price
    for stock in portfolio
    if stock.sector == 'technology'
]
```

**Generated Julia:**
```julia
function calculate_returns(portfolio)
    tech_stocks = filter(stock -> stock.sector == "technology", portfolio)
    return [(stock.price - stock.purchase_price) / stock.purchase_price
            for stock in tech_stocks]
end
```

**Generated TypeScript:**
```typescript
export async function calculateReturns(portfolio: Stock[]): Promise<number[]> {
    const techStocks = portfolio.filter(stock => stock.sector === 'technology');

    return new Promise((resolve) => {
        const worker = new Worker('calculator.js');
        worker.postMessage(techStocks);
        worker.onmessage = (e) => resolve(e.data);
    });
}
```

## 🔬 Scientific Computing

### Data Analysis Pipeline

**Python Input:**
```python
# Normalize experimental data
normalized_data = [
    (value - mean) / std
    for value in measurements
    if value is not None and value > 0
]
```

**Generated Julia:**
```julia
function normalize_data(measurements, mean, std)
    valid_measurements = filter(x -> x !== nothing && x > 0, measurements)
    return [(x - mean) / std for x in valid_measurements]
end
```

**Generated Rust:**
```rust
use rayon::prelude::*;

pub fn normalize_data(measurements: &[Option<f64>], mean: f64, std: f64) -> Vec<f64> {
    measurements.into_par_iter()
        .filter_map(|&value| value)
        .filter(|&value| value > 0.0)
        .map(|value| (value - mean) / std)
        .collect()
}
```

### Machine Learning Preprocessing

**Python Input:**
```python
# Feature engineering for ML model
features = [
    extract_features(sample)
    for sample in dataset
    if sample.quality_score > 0.8 and sample.label is not None
]
```

**Generated C#:**
```csharp
using System.Linq;

public static class FeatureExtractor {
    public static List<FeatureVector> ExtractFeatures(List<Sample> dataset) {
        return dataset.AsParallel()
            .Where(sample => sample.QualityScore > 0.8 && sample.Label != null)
            .Select(sample => ExtractFeatures(sample))
            .ToList();
    }
}
```

## 🌐 Web Development

### API Response Processing

**Python Input:**
```python
# Process API responses
processed_responses = [
    {
        'id': response.id,
        'status': response.status,
        'data': response.data
    }
    for response in api_responses
    if response.status_code == 200 and response.data is not None
]
```

**Generated TypeScript:**
```typescript
export async function processApiResponses(responses: ApiResponse[]): Promise<ProcessedResponse[]> {
    const validResponses = responses.filter(
        response => response.statusCode === 200 && response.data !== null
    );

    return new Promise((resolve) => {
        const worker = new Worker('processor.js');
        worker.postMessage(validResponses);
        worker.onmessage = (e) => resolve(e.data);
    });
}
```

**Generated Go:**
```go
func processApiResponses(responses []ApiResponse) []ProcessedResponse {
    result := make([]ProcessedResponse, 0, len(responses))

    for _, response := range responses {
        if response.StatusCode == 200 && response.Data != nil {
            processed := ProcessedResponse{
                ID:     response.ID,
                Status: response.Status,
                Data:   response.Data,
            }
            result = append(result, processed)
        }
    }

    return result
}
```

### Real-time Data Streaming

**Python Input:**
```python
# Process streaming data
alerts = [
    create_alert(event)
    for event in stream
    if event.priority == 'high' and event.timestamp > threshold
]
```

**Generated Rust:**
```rust
use rayon::prelude::*;

pub fn process_stream(stream: &[Event], threshold: u64) -> Vec<Alert> {
    stream.into_par_iter()
        .filter(|event| event.priority == "high")
        .filter(|event| event.timestamp > threshold)
        .map(|event| create_alert(event))
        .collect()
}
```

## 🗄️ Database Operations

### Data Aggregation

**Python Input:**
```python
# Aggregate sales data by region
regional_sales = {
    region: sum(sale.amount for sale in sales if sale.region == region)
    for region in regions
}
```

**Generated SQL:**
```sql
SELECT
    region,
    SUM(amount) as total_sales
FROM sales
WHERE region IN ('north', 'south', 'east', 'west')
GROUP BY region;
```

**Generated Julia:**
```julia
function aggregate_sales_by_region(sales, regions)
    result = Dict{String, Float64}()

    for region in regions
        total = sum(sale.amount for sale in sales if sale.region == region)
        result[region] = total
    end

    return result
end
```

### Data Validation

**Python Input:**
```python
# Validate user data
valid_users = [
    user for user in users
    if user.email and '@' in user.email
    and user.age >= 18
    and user.country in allowed_countries
]
```

**Generated SQL:**
```sql
SELECT *
FROM users
WHERE email IS NOT NULL
  AND email LIKE '%@%'
  AND age >= 18
  AND country IN ('US', 'CA', 'UK', 'DE');
```

## 🎮 Game Development

### Game State Processing

**Python Input:**
```python
# Update game entities
updated_entities = [
    update_entity(entity)
    for entity in game_entities
    if entity.active and entity.position.distance_to(player.position) < 100
]
```

**Generated C#:**
```csharp
using System.Linq;

public static class GameEngine {
    public static List<Entity> UpdateEntities(List<Entity> entities, Vector3 playerPosition) {
        return entities.AsParallel()
            .Where(entity => entity.Active &&
                            entity.Position.DistanceTo(playerPosition) < 100)
            .Select(entity => UpdateEntity(entity))
            .ToList();
    }
}
```

**Generated Rust:**
```rust
use rayon::prelude::*;

pub fn update_entities(entities: &[Entity], player_position: Vector3) -> Vec<Entity> {
    entities.into_par_iter()
        .filter(|entity| entity.active)
        .filter(|entity| entity.position.distance_to(player_position) < 100.0)
        .map(|entity| update_entity(entity))
        .collect()
}
```

## 🔧 System Administration

### Log Processing

**Python Input:**
```python
# Process system logs
error_logs = [
    log_entry for log_entry in logs
    if log_entry.level == 'ERROR'
    and log_entry.timestamp > start_time
    and 'database' in log_entry.component
]
```

**Generated Go:**
```go
func processErrorLogs(logs []LogEntry, startTime time.Time) []LogEntry {
    result := make([]LogEntry, 0, len(logs))

    for _, log := range logs {
        if log.Level == "ERROR" &&
           log.Timestamp.After(startTime) &&
           strings.Contains(log.Component, "database") {
            result = append(result, log)
        }
    }

    return result
}
```

**Generated SQL:**
```sql
SELECT *
FROM logs
WHERE level = 'ERROR'
  AND timestamp > '2024-01-01 00:00:00'
  AND component LIKE '%database%';
```

## 📊 Data Science

### Time Series Analysis

**Python Input:**
```python
# Calculate moving averages
moving_averages = [
    sum(prices[i:i+window]) / window
    for i in range(len(prices) - window + 1)
    if all(prices[i:i+window])
]
```

**Generated Julia:**
```julia
function calculate_moving_averages(prices, window)
    result = Float64[]

    for i in 1:(length(prices) - window + 1)
        window_prices = prices[i:(i + window - 1)]
        if all(isfinite, window_prices)
            avg = sum(window_prices) / window
            push!(result, avg)
        end
    end

    return result
end
```

### Feature Engineering

**Python Input:**
```python
# Create feature combinations
feature_combinations = [
    (f1, f2, f1 * f2)
    for f1 in features1
    for f2 in features2
    if f1 > 0 and f2 > 0
]
```

**Generated Rust:**
```rust
use rayon::prelude::*;

pub fn create_feature_combinations(features1: &[f64], features2: &[f64]) -> Vec<(f64, f64, f64)> {
    features1.into_par_iter()
        .flat_map(|&f1| features2.iter().map(move |&f2| (f1, f2)))
        .filter(|(f1, f2)| *f1 > 0.0 && *f2 > 0.0)
        .map(|(f1, f2)| (f1, f2, f1 * f2))
        .collect()
}
```

## 🚀 Performance Optimization

### Parallel Processing Patterns

**Python Input:**
```python
# Process large datasets in parallel
results = [
    process_chunk(chunk)
    for chunk in data_chunks
    if chunk.size > 0
]
```

**Generated Rust (with Rayon):**
```rust
use rayon::prelude::*;

pub fn process_large_dataset(chunks: &[DataChunk]) -> Vec<ProcessedChunk> {
    chunks.into_par_iter()
        .filter(|chunk| chunk.size > 0)
        .map(|chunk| process_chunk(chunk))
        .collect()
}
```

**Generated Go (with Goroutines):**
```go
func processLargeDataset(chunks []DataChunk) []ProcessedChunk {
    var wg sync.WaitGroup
    results := make([]ProcessedChunk, 0, len(chunks))
    mu := sync.Mutex{}

    for _, chunk := range chunks {
        if chunk.Size > 0 {
            wg.Add(1)
            go func(c DataChunk) {
                defer wg.Done()
                processed := processChunk(c)
                mu.Lock()
                results = append(results, processed)
                mu.Unlock()
            }(chunk)
        }
    }

    wg.Wait()
    return results
}
```

## 🎯 Best Practices

### 1. **Choose the Right Backend**

- **Rust** - High-performance systems, embedded applications
- **Julia** - Scientific computing, numerical analysis
- **Go** - Microservices, concurrent systems
- **TypeScript** - Web applications, browser-based processing
- **C#** - Enterprise applications, Windows development
- **SQL** - Database operations, data warehousing

### 2. **Optimize for Your Use Case**

- **Parallel Processing** - Use for CPU-intensive tasks
- **Sequential Processing** - Use for I/O-bound tasks
- **Broadcast Operations** - Use for vectorized operations (Julia)
- **Database Optimization** - Use predicate pushdown for SQL

### 3. **Consider Data Types**

- **Integer Operations** - Use `int` for counting, indexing
- **Floating Point** - Use `float64` for calculations
- **String Processing** - Use appropriate string types per language
- **Custom Types** - Define structs/classes for complex data

### 4. **Error Handling**

- **Validation** - Check input data before processing
- **Fallbacks** - Provide default values for missing data
- **Logging** - Include error logging in generated code
- **Testing** - Test edge cases and error conditions

---

**Ready to transform your Python code?** Try the [Playground](playground.html) or check out our [Quick Start Guide](README.md#-quick-start)!
