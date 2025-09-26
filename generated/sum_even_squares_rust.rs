use std::collections::{HashMap, HashSet};

fn program() -> i32 {
    (1..1000000).filter(|&i| i % 2 == 0).map(|i| i * i).sum()
}
