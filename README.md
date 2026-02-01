# Herbalife Packing Optimization Project

## 🏢 Project Background
This project was developed for **Herbalife**, specifically for their distribution center in Venray. The primary goal was to address critical inefficiencies in their product packing process that the existing system could not handle effectively.

## ⚠️ Problem Statement
The packing algorithm previously in use had a significant failure rate. Approximately **10% of the time, the products did not fit into the selected box at all**. This led to manual intervention, repackaging delays, and increased operational costs. The core issue was the algorithm's inability to efficiently handle complex 3D bin packing constraints for varied order sizes.

## 💡 Solution
We developed a new, sophisticated **3D bin packing algorithm** designed to overcome these limitations. This solution:
- Optimizes space utilization within boxes.
- Respects improved rotation and layer-based placement rules.
- drastically reduces the "non-fitting" scenarios compared to the legacy system.

## 🔗 Project Resources & Documentation
Please refer to the following resources for detailed implementation and usage instructions:

*   **[Sofa Herbalife Algorithm](./sofa-2024-herbalife-sofa/README.md)**  
    *The core algorithm implementation and technical details.*

*   **[Project Documentation (Wiki)](./sofa-2024-herbalife-sofa.wiki/Home.md)**  
    *Comprehensive documentation including requirements, architecture, and user guides.*

*   **[Visualization UI](./UI/Visualization_test)**  
    *The user interface used to generate visual outputs of the packing algorithm and verify results.*
