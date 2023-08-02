# EMOD --> Gen-Epi workflow

## Overview


## Features

- Archetypes: flat (no seasonality), maka_like, magude_like (same seasonality but no interventions), maka_historical, magude_historical (full model with interventions included)
- For flat/maka_like/magude_like scenarios, can set a target (RDT) prevalence (5%, 10%, 20%, 30%, 40%). User does not need to worry about larval habitats.
- Set population size (1k,10k,20k,50k,100k)
- Set importation rate per 1000 people in population. These infections are added randomly throughout population at close-to-specified rate 
- Set max_individual_infections. 
- Realistic biting heterogeneity included
- If running maka_historical or magude_historical, the data comparison plots are automatically generated on COMPS for quick sanity checking.

## Quirks/Things to be aware of
- Historical sims run for 60 years; non-historical sims run for 40 years. The long run-times are for "burn-in", with the goal of reaching equilibrium population immunity.
- Runtime for 1k population size is ~20 minutes. Runtime for 10k population size is a few hours. Runtime for 100k population size can be a few days.
- Maka_historical is a model of Ndoga Babacar/Makacoulibantang in central Senegal. It includes health-seeking, bednet distributions, seasonal chemoprevention, IRS sprays, and active PECADOM sweeps.
- Magude_historical is a model of Magude-Sede and Facazissa in southern Mozambique. It includes health-seeking, bednet distributions, MDA campaigns, IRS sprays, and household-level treatment when cases are reported.
- All sims are a single node (well-mixed population). There is no spatial structure.
- Importation events are discrete events that choose N individuals every T timesteps and attempt to add a new infection object to them. This discreteness means that even if you want 370 importations per year, the code currently rounds to the closest discrete situation and will import 365 times that year.
- Target prevalence can only be set if running a non-historical scenario. The target prevalence will only reached towards the end of the simulation after equilibrium immunity has been reached.
- The population size will stay approximately equal to the specified value, but up to ~10% fluctuations are possible as births and deaths stochastically balance each other.
- The transmission model has been calibrated for max_individual_infections = 3, but for explorations you can set this higher and the "antigenic space" will automatically be scaled linearly. This might be useful to explore when running higher prevalence values to avoid having a large segment of the population artifically unable to receive new infections.

## Potential future items to revisit
- Importations are dropped on anyone in sim, not restricted to travelers.
- Importations are not seasonal, but occur uniformly throughout the year.
- Simulations always include burn-in. Serialization is not currently included, simplifies running for new users (especially if the executable changes) at the cost of slower runtime.

## Other items of note
- The "target prevalence" feature was created with some pre-processing by sweeping over larval habitats and finding the approximate larval habitat value that gave the desired annual average prevalence.