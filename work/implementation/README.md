# 3D Bin Packing Implementation

## Overview
This implementation provides a sophisticated 3D bin packing algorithm designed to efficiently pack products into boxes while respecting various constraints. The algorithm uses a layer-based approach with parallel processing capabilities for handling large-scale packing operations.

## 🏗 Project Structure

```
implementation/
├── algorithm/              # Core algorithm components
│   ├── data/              # Configuration and definition files
│   │   ├── box_definition.json     # Box specifications
│   │   ├── orderline_definitions.csv  # Order data
│   │   └── product_definitions.csv    # Product specifications
│   ├── box_definition.py  # Box constraint definitions
│   ├── box_result.py      # Box packing results
│   ├── fragment.py        # Space management
│   ├── layer_result.py    # Layer packing logic
│   ├── order.py           # Order management
│   ├── packer.py          # Core packing algorithm
│   ├── position.py        # Product positioning
│   └── system.py          # System coordination
├── visualization/         # Visualization components
│   ├── stylesheet/       # UI styling
│   │   ├── default.css              # Default color scheme
│   │   ├── protanopia_deuteranopia.css  # Color-blind friendly scheme 1
│   │   └── tritanopia.css          # Color-blind friendly scheme 2
│   ├── box.py           # Box visualization logic
│   ├── csv_reader.py    # Data import handling
│   ├── item.py          # Item visualization
│   ├── order.py         # Order visualization
│   ├── painter.py       # 3D rendering logic
│   └── order_visualizer.py  # Main visualization interface
├── tests/                # Test suite
│   ├── test_algorithm_packer.py
│   ├── test_algorithm_order.py
│   └── ...
└── docs/                # Documentation
    ├── algorithm/       # Algorithm documentation
    │   ├── packing_strategy.md     # Packing algorithm details
    │   ├── optimization.md         # Optimization techniques
    │   └── constraints.md          # System constraints
    └── visualization/   # Visualization documentation
        ├── usage.md              # Usage guide
        └── color_schemes.md      # Color scheme documentation
```

## 🔄 Algorithm Workflow

1. **Input Processing**
   - Load box definitions from JSON
   - Parse order data from CSV
   - Load product specifications

2. **Order Processing**
   - Group orders by order number
   - Sort products within orders
   - Prepare for parallel processing

3. **Packing Algorithm**
   - Layer-based packing approach
   - Space optimization using fragments
   - Rotation handling for optimal fit
   - Collision detection

4. **Output Generation**
   - CSV format results
   - Detailed placement coordinates
   - Box utilization statistics

## 🔑 Key Components

### Box Definition
- Defines available box types
- Specifies dimensions and constraints
- Handles weight limits and fill ratios

### Layer Management
- Organizes products in horizontal layers
- Optimizes space utilization
- Manages remaining spaces

### Position Handling
- Tracks product coordinates
- Manages product rotations
- Ensures proper placement

### Fragment System
- Tracks available spaces
- Manages space splitting
- Optimizes space utilization

## 🚀 Getting Started

### Prerequisites
```bash
python 3.8+
pip
virtual environment (recommended)
```

### Installation
1. Clone the repository:
```bash
git clone https://github.com/FontysVenlo/sofa-2024-herbalife-sofa
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Algorithm
```bash
python main.py
```

## 📊 Code Coverage

### Running Coverage Tests
Complete coverage analysis:
```bash
python -m coverage run -m unittest discover -p "test*.py" && python -m coverage report
```

Generate HTML coverage report:
```bash
python -m coverage run -m unittest discover -p "test*.py" && python -m coverage html
```

### Coverage Commands Explained
- `coverage run`: Executes tests and collects coverage data
- `unittest discover`: Automatically finds all tests
- `coverage report`: Generates terminal summary
- `coverage html`: Creates detailed HTML report

## 🔍 Key Features

- **Parallel Processing**: Efficiently handles multiple orders
- **Layer-Based Packing**: Optimizes space utilization
- **Rotation Optimization**: Considers all possible orientations
- **Constraint Handling**: Respects weight and dimension limits
- **Progress Tracking**: Real-time packing progress visualization

## 📝 Documentation

Detailed documentation is available in the `docs/` directory:
- Algorithm specifications
- API documentation
- Visualization guides
- Performance metrics

## 🧪 Testing

Run the test suite:
```bash
python -m unittest discover -p "test*.py"
```

## 📈 Performance Considerations

- Utilizes multi-core processing
- Implements caching mechanisms
- Optimizes memory usage
- Provides progress tracking
- Handles large-scale orders efficiently

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎨 Visualization System

### Key Features
- Interactive 3D visualization of packed boxes
- Color-blind friendly interface with multiple themes
- Real-time packing progress visualization
- Order and box navigation
- Detailed item placement view
- Support for large-scale orders

### Components
1. **Order Visualizer**
   - Main interface for visualization
   - Interactive controls
   - Multi-theme support
   - Progress tracking

2. **3D Painter**
   - 3D rendering of boxes and items
   - Dynamic view angles
   - Color-coded item placement
   - Space utilization visualization

3. **Data Management**
   - CSV data import
   - Order tracking
   - Box and item management
   - Position coordination

### Color Schemes
- **Default**: Standard color scheme
- **Protanopia/Deuteranopia**: Optimized for red-green color blindness
- **Tritanopia**: Optimized for blue-yellow color blindness
