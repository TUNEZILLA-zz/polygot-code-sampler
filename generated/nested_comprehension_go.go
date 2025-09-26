func program() int {
    acc := 0
    for x := 1; x < 1000; x += 1 {
        if !(x % 3 == 0) { continue }
        acc += sum((x * y for y in range(1, 100) if y % 2 == 0))
    }
    return acc
}
