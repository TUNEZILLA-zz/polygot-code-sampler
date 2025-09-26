function program(): number {
    return Array.from({length: 1000}, (_, i) => 0 + i).reduce((acc, i) => acc + (len([x for x in range(10000) if (x + i) % 1000 == 0])), 0);
}
