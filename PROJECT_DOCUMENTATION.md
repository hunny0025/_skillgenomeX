# Baryonic Perseverance / SkillGenome X - Project Documentation

## 1. Project Overview

**SkillGenome X** (project repository: *baryonic-perseverance*) is a full-stack, AI-powered National Talent Intelligence System. It aims to analyze, predict, and map the skill landscape across various states and domains, identifying "hidden talent," calculating migration risks, and simulating the impact of skill-related policies.

The system is designed with a premium, dashboard-style interface and a robust AI backend capable of data handling, prediction, and risk assessment.

## 2. Technology Stack

### Backend
- **Framework**: Python with Flask
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-Learn (`GradientBoostingRegressor` for skill prediction, `IsolationForest` for anomaly detection)
- **Deployment & Infra**: Configurations for Docker and Render (`render.yaml`, `Dockerfile`)

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Data Visualization**: Recharts (Charts/Graphs), React Simple Maps (Geographical Data)
- **Routing & Networking**: React Router DOM, Axios

## 3. Core Features & Capabilities

### 3.1. AI-Driven Talent Intelligence Engine
- **Predictive Skill Scoring**: Evaluates a user's true skill score (0-100) based on multiple input vectors (e.g., learning behavior, economic activity, innovation, digital presence) using a Gradient Boosting Regressor.
- **Explainable AI (XAI)**: Breaks down the prediction into top positive and negative contributing factors, providing transparent reasoning for the generated scores.
- **Anomaly Detection**: Uses Isolation Forest to flag suspicious data inputs or extremely irregular profiles, providing a fallback safety net.

### 3.2. National Dashboard & Real-Time KPIs
- **System Health & AI Status**: Real-time monitoring of the AI model's training accuracy, dataset size, and operational status.
- **Macro Analytics**: Pan-level calculation of the National Stability Index, Skill Velocity, Critical Zones, and overall Hidden Talent Rates.

### 3.3. Regional & Geographical Intelligence
- **State-by-State Breakdown**: Analyzes specific states to determine their primary domain specialization, average skill levels, and rural talent rates.
- **Visual Mapping**: Interactive maps (`RegionalMap.jsx`) charting talent distribution, innovation intensity, and ecosystem balance scores across the region.

### 3.4. Risk Analysis & Migration Tracking
- **Risk Calculation Logic**: Evaluates states based on the Digital Divide (low digital access), Skill Deficits, and Talent Migration Risk (high-skilled individuals in low-opportunity areas).
- **Risk Severity**: Categorizes regional risks into Low, Moderate, and Critical brackets.

### 3.5. Market Intelligence & Skill Gap Analysis
- Calculates the real-time gap between industry demand and current talent supply across major domains (Technology, Agriculture, Healthcare, etc.).
- Categorizes domains automatically into Shortage, Balanced, or Surplus.

### 3.6. Policy Simulation Engine ("What If" Scenarios)
- Allows administrators to simulate the application of specific socio-economic policies (e.g., "Deploy Rural Broadband", "Launch Skilling Programs", "Establish Hubs").
- Dynamically recalculates the region's risk scores and predicts the multi-factor reduction in the digital divide, skill deficit, and migration risks based on the chosen policy.

### 3.7. Hidden Talent & Economic Impact Calculator
- Actively seeks out "Hidden Talent" (individuals with skill scores > 70 who reside in areas with low opportunity or limited digital access).
- Calculates the projected economic impact (in thousands INR) of discovering and utilizing this hidden talent pool.

### 3.8. Proof of Work Verification
- A verification subsystem that parses provided URLs (GitHub, LinkedIn, Portfolios).
- Generates a "Proof Strength" score based on the presence of verified links, completed projects, learning hours, and certifications.

## 4. Architecture Structure

### `backend/`
- `app.py`: The core monolithic Flask server containing ML model logic, data ingestion from CSV, and all REST API endpoints.
- `app/api/`: Versioned API structure setup (FastAPI traces, likely from an earlier or concurrent iteration).
- `data/`: Contains the synthetic talent dataset used to train the local models.

### `frontend/`
- `src/App.jsx`: The main dashboard layout orchestrator, managing state between the Sidebar, Main View, Alerts Panel, and handling real-time API communication.
- `src/components/`: Houses all the modular UI components, broadly split into visual data panels (`GenomeMap`, `RegionalMap`, `Forecast`) and interactive panels (`PolicyPanel`, `WhatIf`, `InputPanel`).

## 5. System Workflows

1. **Initialization**: On backend startup, the AI models (`GradientBoostingRegressor`, `IsolationForest`) are trained in-memory using the provided dataset (`synthetic_talent_data.csv`).
2. **Data Interaction**: The user toggles through the React dashboard, interacting with sliders and policy drop-downs.
3. **Inference Execution**: Changes stream via Axios to the Flask backend which runs live inference, calculates new weights, and attaches reasoning logic.
4. **Visualization**: Changes are animated onto the screen using Framer Motion and charted using Recharts.
