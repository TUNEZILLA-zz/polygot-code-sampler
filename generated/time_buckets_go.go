func program() int {
    acc := 0
    for i := 0; i < 1000; i += 1 {
        acc += len([x for x in range(10000) if (x + i) % 1000 == 0])
    }
    return acc
}
