# Bin Packing Algorithm: Performance Acceptance Procedure

###  Demonstrating How the Acceptance Procedure Meets the SMART Criteria

## Specific
- The acceptance procedure is **clearly defined** for the cubing (bin packing) algorithm, detailing:
  - **What** is tested: performance, correctness, scalability, and stability.
  - **How** it is tested: specifying test environment, data sets, and the branches under investigation.
- It is specific as, it is shown **step-by-step** actions (e.g., cloning specific branches, measuring total time and worker time, logging errors or anomalies, etc.).

## Measurable
- The procedure establishes **measurable targets**:
  - **Under 200 seconds** of total time on at least 8 cores.
  - **≥ 95%** correctness in box packing (minimal repacking).
- By logging total time, worker time, and correctness metrics, each branch can be **objectively measured** against these criteria.

## Achievable
- The tests use **real-world data** (e.g., 136,570 order lines) and a **feasible plan**:
  1. Check out each branch.
  2. Run the algorithm on the same data set.
  3. Log and compare results.
- Because the data and procedures are replicable (anyone can clone the repo and run the tests), the goals are **doable** and **realistic**.

## Relevant
- The procedure guarantees the final cubing algorithm is ready for **real operational use**, covering:
  - **Performance**: Ensures no excessive runtimes.
  - **Correctness**: Validates accurate box selections.
  - **Scalability**: Confirms large data handling without crashes.
- This aligns precisely with **stakeholder requirements**: they need confidence in both performance and accuracy before deployment.


This document outlines the **Acceptance Procedure** for bin packing (cubing) algorithm, focusing specifically on **performance** and **correctness**. We leverage multiple algorithm variations and measure their speed, scalability, and accuracy against predefined criteria.

---

## 1. Purpose

- **Why**: Ensure that each branch or implementation meets the real-world demands of time efficiency, concurrency, and correctness before merging or deploying.
- **Scope**: This acceptance procedure covers:
  1. **Performance Metrics** (e.g., total time, worker time, throughput).
  2. **Correctness Metrics** (e.g., correctness of box assignments, minimal repacking).
  3. **Scalability** (handling large data sets and multi-core usage).

---

## 2. Acceptance Criteria

1. **Performance (Speed)**
   - **Threshold**: Must process 136,570 order lines in **under 200 seconds** using at least 8 logical cores.
   - **Worker Time**: Total worker time (summed across threads) should remain within a reasonable factor of real time, demonstrating effective concurrency.

2. **Correctness**
   - **Threshold**: At least **95%** of boxes selected must be the correct size for the items, minimizing repacking errors.

3. **Scalability**
   - **Threshold**: Must handle datasets of **200,000+ order lines** without timing out or crashing.
   - Should maintain stable performance on machines with fewer cores (down to 2), albeit with potentially longer total time.

4. **Stability & Logging**
   - Must not produce unhandled exceptions.
   - Must log key steps (e.g., start/end times) to allow easy debugging.

---

## 3. Test Environment Setup

- **Hardware**: 10 logical cores (e.g., Intel/AMD CPU), 16 GB RAM, typical SSD storage.
- **OS & Python Version**: Tested on Linux or Windows, Python 3.9+.
- **Branches Under Test**:
  1. `performance-speed`
  2. `performance-improvements`
  3. `improved_speed_and_performance`
  4. (Others as needed, e.g., `retry_with_queues`, etc.)

---

## 4. Test Data & Procedure

1. **Data Files**:  
   - A large set of 136,570 order lines (15,809 orders).
   - Additional test sets as needed (edge cases, smaller or bigger volumes).

2. **Execution Steps**:
   1. **Clone/checkout** each branch locally.
   2. **Run the same input** on each implementation, capturing:
      - **Total Time** (wall-clock).
      - **Total Worker Processing Time** (summed across threads).
      - **Boxes** assigned, item distribution accuracy, etc.
   3. **Log results** to `.csv` or `.md` in `./acceptance-tests/results/`.

3. **Pass/Fail Evaluation**:
   - Compare measured times to **200s** threshold.
   - Verify if 95% of boxes are correctly assigned.
   - Record any errors or anomalies (e.g., memory issues, exceptions).

---

## 5. Example Results

| Implementation                                         | XS    | S     | M    | XSD  | L    | ENV  | Total Boxes | Total Worker Time (sec) | Total Time (sec) | Meets 200s? | Accuracy ≥95%? |
|--------------------------------------------------------|-------|-------|------|------|------|------|-------------|-------------------------|-------------------|-------------|----------------|
| `output_orderline_definitions_improved_speed.csv`      | 6423  | 6153  | 1737 | 1095 | 676  | 58   | 16142       | 830.64                  | 161.37            | ✅ Yes       | ✅ Yes         |
| `output_orderline_definitions_improved_speed_and_performance.csv` | 6414  | 6161  | 1743 | 1097 | 658  | 58   | 16131       | 954.05                  | 209.62            | ❌ No        | ✅ Yes         |
| `output_orderline_definitions_retry_with_queues.csv`   | 7094  | 5541  | 1681 | 1143 | 723  | 45   | 16227       | 1047.76                 | 232.79            | ❌ No        | ✅ Yes         |

### Explanation
- **`improved_speed`**: Finishes in **161.37s**, under our 200s threshold.  
- **`improved_speed_and_performance`**: Takes **209.62s**, exceeding 200s.  
- **`retry_with_queues`**: Takes **232.79s**.  

All achieve acceptable correctness (≥95%), but only `improved_speed` meets the 200s limit in this test scenario.

---

## 6. Stakeholder Review & Sign-Off

- **Recommended Implementation**: `improved_speed` meets the 200s requirement and has high accuracy.  
- **Conditional Acceptance**: If hardware is upgraded or minor optimizations are done, `improved_speed_and_performance` might also pass the threshold.  

- **External Stakeholder Approval**:  
  - [X] **External Stakeholder**: “Approved”

> **Code Walkthrough**  
> As part of ensuring transparency and maintainability, I will **lead a code walkthrough** with the external stakeholder and team. During this session, we’ll explain how the algorithm logic handles item placing, item orientation, and leftover space calculations. This walkthrough provides an opportunity for everyone to ask questions, understand design decisions, and confirm alignment with stakeholder expectations.


### Real-world test cases and communication
<img width="1347" alt="Screenshot 2025-01-10 at 11 54 33" src="https://github.com/user-attachments/assets/23d73944-3355-4067-bac3-62f44d3583d3" />

Confirmation was in live and we got to see the picture on customer's phone.
---

## 7. Conclusion

**Final Recommendation**: Based on the above tests and thresholds, **`improved_speed`** is the current best overall branch for production. It satisfies the <200s total time acceptance requirement, while maintaining high correctness. Should the dataset grow substantially or the system run on fewer cores, additional optimization (or a fallback approach) might be needed.

With the **code walkthrough** planned, we will ensure all stakeholder has a clear understanding of the implementation details, making the base for further improvements and smooth future maintenance.

