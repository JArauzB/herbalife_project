# MoSCoW Prioritization

The MoSCoW prioritization method helps us define which features and requirements are essential for the project, ensuring that critical aspects are delivered first.

## Must-have
These are the requirements that are critical to the success of the cubing algorithm project. Without these, the system would not function or meet the business objectives.

| Requirement Description                                            | Reason for Priority                  |
|--------------------------------------------------------------------|--------------------------------------|
| The cubing algorithm must account for both product volume and dimensions. | Essential for accurate box selection. |
| The system must output an Excel sheet with the correct box type.   | Required for daily operations at the distribution center. |
| The program must handle smaller boxes effectively.                 | Most packing issues occur with smaller boxes. |
| The solution must be developed in Python.                          | Company requirement for compatibility and future maintainability. |

## Should-have
These requirements are important but not absolutely essential. If time or resources are limited, they can be deferred to a later phase but are still valuable for improving efficiency or user experience.

| Requirement Description                                            | Reason for Priority                  |
|--------------------------------------------------------------------|--------------------------------------|
| Visual representation of product placement (3D Tetris).            | Improves user understanding and efficiency in packing. |
| The system should be optimized for performance with large datasets. | Ensures the solution scales effectively. |
| Seamless integration with existing Excel-based systems.            | Simplifies data input/output and user interaction. |

## Could-have
These are nice-to-have requirements that will enhance the system but can be implemented later if resources allow. Their absence will not significantly impact the core functionality.

| Requirement Description                                            | Reason for Priority                  |
|--------------------------------------------------------------------|--------------------------------------|
| Feature to cut boxes to perfectly fit products.                    | Provides further optimization of packaging, but is not essential. |
| Customizable options for visual representations.                   | Enhances the user interface, but is not critical. |
| Suggestions for efficient packing order based on product categories. | Could improve the packing process, but is not a core need. |

##  Won't-have (for now)
These requirements are explicitly out of scope for this phase of the project but may be considered for future releases or projects.

| Requirement Description                                            | Reason for Priority                  |
|--------------------------------------------------------------------|--------------------------------------|
| Integration with warehouse automated machinery.                    | Out of scope for the current project. |
| Advanced 3D modeling tools for visual outputs.                     | Not necessary for the project’s objectives. |
| Expanding the number of box types beyond the current selection.     | Current focus is on optimizing existing box types. |
