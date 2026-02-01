## Learning Goal 1:

### Specific
- **Goal**: *“Analyse various algorithms to understand their strengths, weaknesses, and potential for optimisation, including investigating hybrid approaches.”*  
- **Action**: Concentrated on **3D bin-packing** algorithms (e.g., Best Fit, Best Fit Decreasing, First Fit Decreasing) and documented their rotation optimizations, space-splitting strategies, and data structures.

### Measurable
- **Goal**: *“Completing a comparative analysis report on at least 3 algorithms, identifying key areas for improvemens.”*  
- **Action**: **Analysis paper** (see [analysis.pdf](https://github.com/user-attachments/files/18218462/analysis.pdf)) compares:
  1. **Best Fit**  
  2. **Best Fit Decreasing (BFD)**  
  3. **First Fit Decreasing (FFD)**  
- Highlighting **areas for improvement** (e.g., rotation handling, advanced space partitioning).

### Achievable
- **Goal**: *“Use existing resources such as academic papers, online tutorials, and software documentations to perform thorough analysis.”*  
- **Action**:  
  1. **Codebase References**:  
     - [Bin-Packing Algorithms GitHub repository](https://github.com/Eisah-Jones/Bin-Packing-Algorithms/tree/master)  
     - Eisah Jones’ **sorting/packing** examples  
  2. **Online Resources**:  
     - GeeksforGeeks articles on bin packing  
     - Erick Dube’s paper “[Optimizing Three-Dimensional Bin Packing Through Simulation](https://github.com/user-attachments/files/18218464/erick_dube_507-034.2.pdf)”  
  3. **Academic Approach**:  
     - Learned how algorithms manage bin creation, rotation checks, and complexity analysis.  
- Reliance on **freely accessible** open-source code and scholarly papers ensures the analysis was both **doable** and **thorough**.

### Relevant
- **Goal**: *“This goal is relevant as it is the foundation of the algorithm that will be in use to achieve the end goal (cubing algorithm).”*  
- **Action**: By understanding how each heuristic handles 3D constraints and item rotations, we can make **informed decisions** for the Herbalife cubing algorithm. This will lead to:
  - More **accurate box usage** (fewer wasted materials).
  - Potential **time savings** in packing operations.
  - **Scalability** for large orders (e.g., 90,000+ order lines).


The analysis paper on cubing algorithms for Herbalife focuses on evaluating bin-packing strategies, with an emphasis on rotation optimization for 3D bin-packing problems. The methodology combines academic research, online resources, and pre-existing codebases, given that the experiments could not be conducted firsthand. Here's how it was constructed:

##  1. Codebase References
The analysis paper relies on pre-existing algorithm implementations to evaluate and compare various bin-packing strategies. These implementations come from open source, such as the [Bin-Packing Algorithms GitHub repository](https://github.com/Eisah-Jones/Bin-Packing-Algorithms/tree/master), and utilize modular components for specific tasks. 

* Algorithm Implementations: Includes algorithms like Best Fit and Best Fit Decreasing that assign items to bins based on their size and available space.

* Implements the logic to: Evaluate free space in bins.

* Dynamically assign items to the most suitable bin based on specific strategies (e.g., smallest remaining space for Best Fit).

* Dynamic Bin Handling: Manages the addition of new bins dynamically when no existing bin can accommodate the current item.

##  2. Online Resources
Since the experiments weren't conducted independently, the study draws on the following:

### Code and Examples:

The provided code snippet (e.g., best_fit and best_fit_decreasing) illustrates key algorithmic steps:
Iterating over items and bins to assign items to the best-fitting bin.
Using sorting techniques (e.g., shell sort) to enhance performance for decreasing variants.
Algorithms were tested and benchmarked in pre-existing studies to provide comparative insights.
Key Reference:

Eisah Jones' portfolio ([sorting algorithms](https://www.eisahjones.com/portfolio#/sorting-algorithms/)) contributed valuable insights into sorting and packing strategies.

GeeksforGeeks: Articles like "Bin Packing Problem - Minimize the Number of Used Bins" informed the theoretical framework for space optimization.

## 3. Structure of the Paper
### Introduction:

Defines the 3D Bin-Packing Problem and contextualizes it within Herbalife’s logistics.
Highlights the current inefficiencies (e.g., volume-only considerations).

## Background and Problem Definition:
Explores the challenges of bin-packing, including dimensional constraints, scalability, and rotation optimization.

## Algorithm Analysis:
Compares two primary heuristic algorithms, FFD and Best Fit, based on metrics like packing efficiency, computational complexity, and rotation handling.

## Testing and Benchmarking:
Adopts performance results from existing studies to evaluate algorithm behavior across different dataset sizes.
Discusses metrics such as:
* Waste minimization (unused space in bins).
* Processing time.
* Scalability (performance with larger datasets).

## Conclusion:
Summarizes findings and proposes solutions tailored to Herbalife’s needs (e.g., Best Fit Decreasing with optional rotation).

### Download the paper
[analysis.pdf](https://github.com/user-attachments/files/18218462/analysis.pdf)

### Another important source:
The analysis paper for Herbalife's optimization problem was influenced significantly by the insights and methods described in Erick Dube's paper, titled "Optimizing Three-Dimensional Bin Packing Through Simulation." This academic work served as a foundation for understanding the complexities of the 3D Bin-Packing Problem and guided the selection of heuristic algorithms for the cubing system.

### 1. Problem Formulation
Dube's paper provides a structured approach to formulating the 3D bin-packing problem:

* Items and bins are represented as rectangular boxes with specific width, height, and depth dimensions.
* Items can be rotated to fit better, with up to six possible orientations for each item.
* The primary objective is to minimize wasted volume while maximizing space utilization.
* This structured formulation influenced the Herbalife paper's emphasis on incorporating rotation optimization and dimensional constraints into the bin-packing algorithm.

### 2. Rotation Optimization
Dube's inclusion of rotation optimization, where each item is rotated to its best-fit orientation, was particularly impactful:
* The concept of trying all six rotations for each item and selecting the best configuration was integrated into the analysis as a critical enhancement for smaller orders.

### 3. Algorithm Complexity
The paper discusses the computational complexity of the algorithms:

* Best Fit Decreasing (BFD) and FFD have a worst-case complexity of 𝑂(𝑛log 𝑛) due to sorting and placement operations.
* For 3D packing with rotation, the complexity increases due to additional checks for all six orientations.
This understanding of complexity helped shape the Herbalife analysis, ensuring scalability for a dataset of 90,000 order lines.

### 4. Practical Implementation Insights
Dube's implementation of the simulation model provided insights into practical challenges:

* Pivot points for item placement.
* Handling unplaced items through iterative attempts.
* Separating textual results (bin counts, item assignments) from graphical representations.

[erick_dube_507-034 (2).pdf](https://github.com/user-attachments/files/18218464/erick_dube_507-034.2.pdf)
