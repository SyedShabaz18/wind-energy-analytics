# WindCast Analytics

### Wind Energy Forecasting & Generation Intelligence Platform

WindCast Analytics is a full-stack energy intelligence application designed to analyze wind power generation, evaluate forecast accuracy, and support data-driven decision-making in electricity markets.

The platform combines historical wind generation records with forecast data to provide interactive visualizations, performance metrics, and insights into forecasting uncertainty.

## Overview

Wind power generation is inherently variable, making accurate forecasting essential for energy planning and grid operations.

WindCast Analytics helps users explore the relationship between predicted and actual wind generation, identify forecasting deviations, and evaluate historical forecast performance through a modern, interactive dashboard.

## Key Features

- **Wind Generation Analysis** — Explore historical wind electricity generation and forecasting trends.
- **Forecast vs. Actual Comparison** — Visualize differences between forecasted and observed generation.
- **Forecast Accuracy Metrics** — Evaluate performance using MAE, RMSE, bias, and WAPE.
- **Interactive Analytics Dashboard** — Explore energy data through visualizations and date-based controls.
- **Historical Decision Analysis** — Examine forecast information available before a selected decision cutoff.
- **Live Data Integration** — Retrieve publicly available electricity market data from Elexon BMRS.
- **Demo Mode** — Explore illustrative scenarios without depending on live API availability.
- **Containerized Architecture** — Run the application using Docker.

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI |
| Data Source | Elexon BMRS API |
| Containerization | Docker, Docker Compose |
| Web Server | Nginx |
| Version Control | Git, GitHub |

## System Architecture

The application follows a frontend–backend architecture.

**React Dashboard → FastAPI Backend → Elexon BMRS API**

The backend retrieves and processes energy market data, calculates forecasting performance metrics, and exposes the results through API endpoints.

The frontend presents these results through interactive analytics views.

## Data Source

WindCast Analytics uses publicly available data from the **Elexon Balancing Mechanism Reporting Service (BMRS)**.

The platform works with historical wind generation and forecast records to support analytical comparisons.

Data availability and completeness depend on the source API and selected analysis period. Demo scenarios are illustrative and should not be interpreted as verified historical observations.

Official source: https://bmrs.elexon.co.uk/

## Getting Started

### Prerequisites

- Git
- Docker
- Docker Compose

### Installation

Clone the repository:

```bash
git clone https://github.com/SyedShabaz18/wind-energy-analytics.git
cd wind-energy-analytics
```

Build and start the application:

```bash
docker compose up --build
```

Open the application:

```text
http://localhost:8080
```

The backend API runs within the Docker environment and is accessible through the configured frontend reverse proxy.

## Forecast Evaluation

WindCast uses standard statistical measures to assess forecasting performance:

- **MAE (Mean Absolute Error):** Average absolute difference between forecasts and observations.
- **RMSE (Root Mean Squared Error):** Error measure that places greater emphasis on larger deviations.
- **Bias:** Indicates systematic overestimation or underestimation.
- **WAPE (Weighted Absolute Percentage Error):** Absolute forecast error relative to total observed generation.

These metrics provide complementary perspectives on historical forecast reliability.

## Deployment

WindCast is designed for containerized execution and can be deployed using services that support Python APIs and modern JavaScript frontends.

**Live Application:** Deployment link to be added.

**API Health Check:** Backend deployment link to be added.

## Intended Use

WindCast Analytics is a historical energy analytics and decision-support prototype.

It is intended for exploring wind generation data and forecast accuracy. It is not a real-time electricity trading system or a substitute for operational forecasting and market-risk controls.

## License

No open-source license has been assigned. All rights are reserved unless a license is added to the repository.
