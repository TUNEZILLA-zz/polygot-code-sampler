use std::collections::{HashMap, HashSet};

fn program() -> i32 {
    (0..1000).map(|i| len([x for x in range(10000) if (x + i) % 1000 == 0])).sum()
}
