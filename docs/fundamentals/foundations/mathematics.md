# Mathematics

> Linear algebra, calculus, probability, and optimisation. The minimum for the AI / ML and biophysics chapters.

This is a "what you need to recognise" page, not a textbook. Treat each section as a vocabulary check.

## Linear algebra

- **Vectors and matrices** — basis, span, rank, null space.
- **Norms** — \(L_1\), \(L_2\), max. Sparsity follows from \(L_1\); Euclidean geometry from \(L_2\).
- **Eigenvalues / eigenvectors** — PCA, kernel methods, dimensionality reduction.
- **Singular value decomposition (SVD)** — the workhorse decomposition; low-rank approximation.
- **Matrix calculus** — gradient of a scalar, Jacobian of a vector, Hessian, chain rule with matrices.

Where it shows up in drug discovery:

- PCA on descriptors / fingerprints for visualisation.
- Kernel methods (Gaussian processes) for QSAR with uncertainty.
- Attention as scaled-dot-product on key/query matrices.

## Calculus

- **Differential** — partial derivatives, gradient, total derivative.
- **Integral** — substitution, by parts, multiple integrals. Probability needs this.
- **Chain rule** — the engine of back-prop.
- **Taylor expansion** — local approximations of force fields and free-energy surfaces.

Where it shows up:

- Backprop and autograd everywhere ML appears.
- MD integration (Verlet, Langevin) requires derivatives of the potential.
- FEP derivations use Zwanzig's identity and statistical mechanics — see [Free-energy methods](../../molecular-design/free-energy.md).

## Probability and stochastic processes

- **Random variables, expectations, variance.**
- **Joint, marginal, conditional distributions.** Bayes' rule.
- **Common distributions** — Bernoulli, binomial, Poisson, Gaussian, log-normal (IC50!), beta (the "rate of rate" intuition), Dirichlet.
- **Markov chains** — MCMC, hidden Markov models, MD as a Markov process at coarse-graining.
- **Information theory** — entropy, KL divergence, mutual information. KL appears in every generative-chemistry training loss.

## Optimisation

- **Convex vs non-convex.** Convex problems have global minima; deep nets are non-convex but practical.
- **Gradient descent + variants** — SGD, momentum, Adam, AdamW. AdamW is the default for the generative-chemistry models in this handbook.
- **Constrained optimisation** — Lagrangians, KKT conditions. Used in MPO with hard property constraints.
- **Bayesian optimisation** — sample-efficient black-box optimisation, the canonical method for active-learning-driven screening.

## A useful self-check

If you can answer each of these in two minutes without notes, you have the minimum:

1. Why does a covariance matrix have non-negative eigenvalues?
2. What is the gradient of \(\|x\|_2^2\)? Of \(x^T A x\)?
3. State Bayes' rule and apply it to "P(active | hit)" given a prior and a likelihood.
4. Why is cross-entropy a sensible loss for classification?
5. Why does AdamW often outperform SGD with momentum on small-data, fine-tuning regimes?

If any are uncomfortable, fill the gap before reading the AI / ML chapters in detail. [Goodfellow et al., 2016](https://www.deeplearningbook.org/) chapters 2–4 are the right level.

## Where to next

[Biology](biology.md) — the central dogma, signalling, immune basics.
