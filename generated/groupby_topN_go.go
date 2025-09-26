func program() int {
    acc := 0
    for group := 0; group < 1000; group += 1 {
        if sum(group) > acc { acc = sum(group) }
    }
    return acc
}
