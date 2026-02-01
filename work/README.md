# Herbalife Cubing Algorithm Project

## 🎯 Project Overview
This repository contains a sophisticated 3D bin packing algorithm developed for Herbalife's distribution center in Venray. The solution optimizes product packing by efficiently arranging items within boxes, reducing packaging costs, and maximizing space utilization.

## ✨ Key Features
- **Advanced 3D Packing Algorithm**
  - Layer-based packing strategy
  - Multi-rotation product placement
  - Weight and dimension constraints
  - Space optimization

- **Interactive Visualization**
  - Real-time 3D visualization
  - Color-blind friendly interface
  - Progress tracking
  - Multiple view angles

- **Performance Optimization**
  - Parallel processing
  - Memory optimization
  - Caching mechanisms
  - Large-scale order handling

## 📁 Repository Structure
```
├── analysis/               # Analysis documentation
│   ├── requirements/       # System requirements
│   └── feasibility/       # Feasibility studies
│
├── design/                # System design
│   ├── architecture/      # System architecture
│   ├── class_diagram/     # UML diagrams
│   └── workflow/          # Process workflows
│
├── implementation/        # Source code
│   ├── algorithm/        # Core packing algorithm
│   ├── visualization/    # 3D visualization system
│   ├── tests/           # Test suite
│   └── docs/            # Implementation documentation
│
└── project_management/    # Project documentation
    ├── agile/            # Scrum artifacts
    ├── meetings/         # Meeting notes
    └── timeline/         # Project timeline
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/FontysVenlo/sofa-2024-herbalife-sofa
```

2. Set up virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r implementation/requirements.txt
```

### Running the Application
```bash
cd implementation
python main.py
```

## 🧪 Testing
Run the test suite:
```bash
cd implementation
python -m unittest discover -p "test*.py"
```

Generate coverage report:
```bash
python -m coverage run -m unittest discover -p "test*.py"
python -m coverage report
python -m coverage html  # For detailed HTML report
```

## 📊 Visualization
The application includes an interactive 3D visualization system:
- Real-time packing visualization
- Multiple color schemes for accessibility
- Order and box navigation
- Detailed item placement view

## 👥 Development Team
- **Julian Köser**
  - Role: Scrum Master & Developer
  - Focus: System Architecture

- **Gabriele Lavinskaitė**
  - Role: Developer
  - Focus: Algorithm Implementation

- **Jorge Arauz**
  - Role: Developer
  - Focus: Visualization System

- **Tim Baars**
  - Role: Developer
  - Focus: Algorithm Implementation

## 📅 Development Timeline
- **Sprint 1-2**: System Analysis & Design
- **Sprint 3-4**: Core Algorithm Implementation
- **Sprint 5-6**: Visualization System
- **Sprint 7-8**: Testing & Optimization
- **Sprint 9-10**: Documentation & Deployment

## 📚 Documentation
Comprehensive documentation is available in the following locations:
- `/analysis`: Requirements and system analysis
- `/design`: System architecture and design decisions
- `/implementation/docs`: Technical documentation
- `/project_management`: Project planning and progress

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
