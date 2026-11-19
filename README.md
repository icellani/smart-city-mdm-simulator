# Smart City MDM Simulator

**Agent-Based Modeling for Urban Data Interoperability**

An academic prototype developed in the context of IA006 — Science and Engineering of Complex Multi-Agent Systems, at the University of Campinas (UNICAMP).

## Overview

This project explores how Master Data Management (MDM) can support semantic interoperability and information coordination across urban systems.

Inspired by smart city infrastructure in Wrocław, Poland, the prototype simulates interactions between transportation, water infrastructure, and energy systems.

## Research Question

Under what conditions can shared master data improve information consistency and coordination among autonomous urban agents?

## Simulation Scenarios

**Without MDM:** Urban agents operate with fragmented identifiers, requiring additional reconciliation to associate events with shared entities.

**With Federated MDM:** Agents use common master references to identify urban entities across systems.

## Technologies

- Python
- JupyterLab
- Plotly
- ipywidgets
- Agent-based modeling concepts
- Master Data Management

## Running the Simulator

1. Open `Smart_City_MDM_JupyterLab.ipynb` in JupyterLab.
2. Install dependencies: `%pip install ipywidgets plotly`
3. Run all notebook cells.
4. Select an urban incident.
5. Execute and compare both scenarios.

## Scientific Context

The prototype draws on concepts such as complex adaptive systems, network topology, emergence, distributed coordination, and computational simulation.

The current simulation is conceptual and deterministic. Its parameters and results are illustrative, not empirical evidence of MDM effectiveness in real cities.

## Future Work

Future research may incorporate stochastic agent behavior, parameter sensitivity analysis, repeated experimental runs, real urban datasets, and statistical comparisons.

## Author

Igor Gustavo Cellani

UNICAMP — IA006, 2026.
