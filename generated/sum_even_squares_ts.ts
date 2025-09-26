function program(): number {
    return Array.from({length: 999999}, (_, i) => 1 + i).filter(i => i % 2 == 0).reduce((acc, i) => acc + (i * i), 0);
}
