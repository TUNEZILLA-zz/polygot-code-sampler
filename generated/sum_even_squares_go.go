func program() int {
    acc := 0
    for i := 1; i < 1000000; i += 1 {
        if !(i % 2 == 0) { continue }
        acc += i * i
    }
    return acc
}
