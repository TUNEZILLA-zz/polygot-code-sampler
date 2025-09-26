function program(): number {
    return Array.from({length: 999}, (_, i) => 1 + i).filter(x => x % 3 == 0).reduce((acc, x) => acc + (sum((x * y for y in range(1, 100) if y % 2 == 0))), 0);
}
