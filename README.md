# Triadic Contemplative Model (Dwelling → Insight)

A minimal nonlinear dynamical-systems demo showing **bistability** in a triadic “interpretive” system with a **dwelling field**:
- **High dwelling / low coherence** basin (protected ambiguity)
- **High coherence / low dwelling** basin (integrated insight)
- A timed **catalytic nudge** can push the system across a separatrix (phase transition)

This repo is intended to be **runnable in one command** and easy to tweak.

## What it does
- Simulates a 4D ODE system: three facets *(x1, x2, x3)* plus a dwelling field *(d)*
- Compares trajectories **with** vs **without** a timed intervention
- Produces a 2×2 visualization panel and saves a PNG to `outputs/`

## Quick start

### 1) Install
```bash
python -m venv .venv
# mac/linux
source .venv/bin/activate
# windows
# .venv\Scripts\activate

pip install -r requirements.txt
```

### 2) Run
```bash
python run_simulation.py
```

Outputs:
- `outputs/simulation_plots.png`
- printed late-time averages (with/without nudge)

## Key equations (high-level)

State:
- `x1, x2, x3 ∈ [0,1]` (facet activations)
- `d ∈ [0,1]` (dwelling)

Coherence:
- `c = (x1 + x2 + x3)/3`

Dwelling dynamics:
- `d' = rise * story_depth * (1-c) * (1-d)  -  fade * c * d`

Dwelling modulates coupling and decay:
- `coupling = 1 + coupling_boost * d`
- `decay = base_decay * (1 - decay_relief * d)`

Facet dynamics (example for x1):
- `x1' = coupling * (act2 + act3)/2 * (1-x1) - decay * x1`
- where `act = Hill(x)` and `Hill(x) = gamma * x^n / (threshold^n + x^n)`

Intervention:
- **jump**: instant bump to `x1` at `t = nudge_time`
- **pulse**: temporary forcing on `x1'` for `nudge_duration`

## Tweak knobs
Open `run_simulation.py` and edit:
- `y0` (initial condition)
- `intervention_time`
- `nudge_mode` (`jump` or `pulse`)
- `model parameters` inside `simulate()`

## Repo layout
- `src/triadic_model.py` — model + simulation helpers
- `run_simulation.py` — single-command demo run
- `tests/` — quick smoke tests
- `outputs/` — generated plots

## License
MIT — see `LICENSE`.
