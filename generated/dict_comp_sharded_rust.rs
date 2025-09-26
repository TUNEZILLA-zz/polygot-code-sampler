use std::collections::{HashMap, HashSet};

fn program() -> HashMap<i32, i32> {
    (1..100000).filter(|&x| x % 3 == 0).map(|x| (x, x * x)).collect()
}
