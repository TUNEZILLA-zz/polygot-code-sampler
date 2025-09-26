function program(): Map<number, number> {
    return Array.from({length: 99999}, (_, i) => 1 + i).filter(x => x % 3 == 0).reduce((map, x) => map.set(x, x * x), new Map<number, number>());
}
