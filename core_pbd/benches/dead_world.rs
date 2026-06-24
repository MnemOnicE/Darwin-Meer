use core_pbd::World;
use criterion::{black_box, criterion_group, criterion_main, BatchSize, Criterion};

fn bench_dead_world(c: &mut Criterion) {
    c.bench_function("dead_world_5000_ticks", |b| {
        b.iter_batched(
            || World::new(),
            |mut world| {
                for _ in 0..5000 {
                    world.step(black_box(1.0 / 60.0));
                }
            },
            BatchSize::SmallInput,
        )
    });
}

criterion_group!(benches, bench_dead_world);
criterion_main!(benches);
