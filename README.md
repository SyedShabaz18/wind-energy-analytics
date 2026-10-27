# WindCast Analytics

### Wind Energy Forecasting & Generation Intelligence Platform

**WindCast Analytics** is a full-stack energy intelligence application designed to analyze historical wind power generation, evaluate forecast accuracy, and support data-driven decision-making in electricity markets.

The platform combines publicly available wind generation observations with historical forecasts to provide interactive visualizations, forecasting performance metrics, and insights into uncertainty.

**[View Live Dashboard](https://windcast-dashboard.onrender.com)** | **[API Health Check](https://wind-energy-analytics.onrender.com/api/health)**

## Overview

Wind power generation is inherently variable, making accurate forecasting important for electricity procurement, energy planning, and grid operations.

WindCast Analytics helps users:

- Compare forecasted and actual wind generation.
- Identify forecasting deviations and uncertainty.
- Examine historical forecast information available at a selected decision cutoff.
- Evaluate forecast performance using statistical metrics.
- Explore publicly available electricity market data through an interactive dashboard.

## Key Features

- **Wind Generation Analysis** — Explore historical wind electricity generation and forecasting trends.
- **Forecast vs. Actual Comparison** — Visualize differences between forecasted and observed generation.
- **Forecast Accuracy Metrics** — Evaluate performance using MAE, RMSE, bias, and WAPE.
- **Interactive Analytics Dashboard** — Navigate between overview, generation, forecast accuracy, and detailed records.
- **Historical Decision Analysis** — Examine forecast information available before a selected decision cutoff to support point-in-time analysis.
- **Elexon BMRS Integration** — Retrieve publicly available electricity market data.
- **Synthetic Preview Mode** — Explore illustrative dashboard scenarios when live API data is unavailable.
- **Containerized Architecture** — Run the frontend and backend using Docker Compose.
- **Cloud Deployment** — Access the deployed frontend and backend through Render.

## Live Application

**Dashboard:** https://windcast-dashboard.onrender.com

**Backend API:** https://wind-energy-analytics.onrender.com

**API Health Check:** https://wind-energy-analytics.onrender.com/api/health

The live application is deployed using Render, with the React frontend hosted as a Static Site and the FastAPI backend hosted as a Web Service.

The backend may require additional time to respond after an inactive period, depending on hosting conditions.

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI |
| Data Source | Elexon BMRS API |
| Containerization | Docker, Docker Compose |
| Local Web Server / Proxy | Nginx |
| Cloud Hosting | Render |
| Version Control | Git, GitHub |

## System Architecture

WindCast follows a frontend–backend architecture.

**React Dashboard → FastAPI Backend → Elexon BMRS API**

1. The user selects a historical decision date and cutoff time.
2. The React frontend sends an analysis request to the FastAPI backend.
3. The backend retrieves relevant forecast and actual generation data from Elexon BMRS.
4. The backend processes the records and calculates forecast evaluation metrics.
5. The frontend displays the analytical results through interactive charts, metrics, and records.

The backend also provides a health-check endpoint and uses caching to reduce repeated data retrieval.

## Data Source

WindCast Analytics uses publicly available data from the **Elexon Balancing Mechanism Reporting Service (BMRS)**.

Official source: https://bmrs.elexon.co.uk/

The platform analyzes historical wind generation observations and forecasts.

### Data Interpretation and Limitations

- Historical forecast analysis is intended to use forecast information available at the selected decision cutoff.
- Actual generation records are used for retrospective evaluation.
- Forecast and actual records may have different time resolutions.
- Data completeness depends on the selected period and source availability.
- Missing records or incomplete forecast coverage can affect the interpretation of results.
- Synthetic preview data is illustrative and must not be treated as verified Elexon observations.

## Forecast Evaluation

WindCast uses the following statistical metrics:

- **MAE (Mean Absolute Error):** Average absolute difference between forecasted and actual generation.
- **RMSE (Root Mean Squared Error):** Error measure that gives greater weight to larger deviations.
- **Bias:** Indicates the direction of systematic forecasting error.
- **WAPE (Weighted Absolute Percentage Error):** Total absolute forecast error relative to total observed generation.

These metrics provide complementary perspectives on historical forecast reliability.

## Getting Started

### Prerequisites

- Git
- Docker with Docker Compose support

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

Open the local dashboard:

```text
http://localhost:8080
```

In the Docker deployment, the frontend uses the configured Nginx reverse proxy to communicate with the backend.

To stop the containers:

```bash
docker compose down
```

## Cloud Deployment

The application is deployed using two Render services.

| Component | Hosting | URL |
|---|---|---|
| Frontend | Render Static Site | https://windcast-dashboard.onrender.com |
| Backend | Render Web Service | https://wind-energy-analytics.onrender.com |

The frontend is built using Vite and published from its `dist` directory.

The backend runs as a FastAPI application using Uvicorn.

### Frontend Environment Variable

```text
VITE_API_URL=https://wind-energy-analytics.onrender.com
```

### Backend Environment Variable

```text
CORS_ORIGINS=https://windcast-dashboard.onrender.com,http://localhost:5173,http://127.0.0.1:5173
```

These variables configure communication between the independently deployed frontend and backend.

## Validation and Testing

The project has undergone development and deployment checks, including:

- Python backend automated tests.
- Frontend production build verification.
- Local Docker-based execution.
- Backend health endpoint testing.
- Live frontend and backend connectivity checks.
- Manual dashboard navigation and visual inspection.
- Manual viewing on a mobile browser using desktop-site mode.

Successful deployment and functional checks do not guarantee complete data coverage or forecasting accuracy for every historical period.

## Intended Use

WindCast Analytics is a historical energy analytics and decision-support prototype.

It is designed for educational, analytical, and demonstration purposes.

It is not a live electricity trading platform, a production forecasting service, or a substitute for operational market-risk controls.

## Project Demonstration

A recorded walkthrough can be provided to demonstrate the application's functionality, architecture, data flow, and technical implementation.

## License

No open-source license has been assigned to this repository. All rights are reserved unless a license is added.
