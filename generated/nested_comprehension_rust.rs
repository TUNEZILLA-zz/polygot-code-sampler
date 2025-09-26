use std::collections::{HashMap, HashSet};

fn program() -> i32 {
    (1..1000).filter(|&x| x % 3 == 0).map(|x| sum((x * y for y in range(1, 100) if y % 2 == 0))).sum()
}
