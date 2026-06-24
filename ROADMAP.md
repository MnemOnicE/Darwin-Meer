# The Volumetric JLSM Engine: Development Roadmap

This roadmap outlines the technical milestones for building the JLSM Engine, adhering to the principles defined in the `BLUEPRINT.md` and `docs/ARCHITECTURE.md`.

## Phase 1: Foundation & Boilerplate (Current)
- [x] Define Architecture and Data Flow schemas.
- [x] Establish the memory boundary zero-copy strategy.
- [x] Scaffold `core_pbd` (Rust library via PyO3/Maturin).
- [x] Scaffold `fishtank_ui` (Python ModernGL + Pygame-ce environment).
- [x] Set up the "Dead World" local benchmarking framework in Rust.

## Phase 2: The Data-Oriented Core
- [x] Implement the Arena Allocator / ECS backbone in `core_pbd` for storing Joints, Links, and Skins.
- [x] Construct the FFI bridge: Expose internal ECS arrays as zero-copy NumPy buffers to Python.
- [x] Build the basic 60Hz loop inside `core_pbd` that simply increments dummy positions.
- [x] Bind Python/ModernGL to these buffers to render dummy moving points (verifying the FFI boundary).

## Phase 3: Position Based Dynamics (PBD)
- [ ] Implement spatial hashing for $O(1)$ collision detection between Joints.
- [ ] Implement distance constraints (rigid bones).
- [ ] Implement compliant constraints ($\alpha > 0$ for soft tissue/muscles).
- [ ] Implement Link snapping logic (structural_integrity threshold).
- [ ] Implement continuous collision detection against the SDF terrain.

## Phase 4: The World Matrix & Thermodynamics
- [ ] Implement the topological SDF representation.
- [ ] Build the 1Hz Double-Buffered Thermodynamic Grids (Illumination, Temperature, Oxygen, Fluid Currents).
- [ ] Implement background thread workers for diffusion and raymarching the grids.
- [ ] Wire the 60Hz physics loop to sample from the active thermodynamic buffer.

## Phase 5: The Cognitive Matrix
- [ ] Define the Bipartite Genetics schema (Block A: Somatic, Block B: Cognitive).
- [ ] Implement the KD-Tree / Spatial Hash for $O(\log N)$ sensor-to-neuron mapping.
- [ ] Build the Elastic Perception accumulator logic to decouple neural evaluations from the 60Hz tick.
- [ ] Implement Hebbian learning ($W_{life}$) and Epigenetic Imprinting.

## Phase 6: Ecology & Rendering
- [ ] Connect ingestion (Maws), energy budgets, and damage algorithms.
- [ ] Implement isogamous reproduction and genetic crossover.
- [ ] Refine the `fishtank_ui` shaders to visually represent structural integrity, bioluminescence, and 3D fluid grids.
