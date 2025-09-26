func program() map[int]int {
    result := make(map[int]int)
    for x := 1; x < 100000; x += 1 {
        if !(x % 3 == 0) { continue }
        result[x] = x
    }
    return result
}
