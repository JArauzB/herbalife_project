# Organizational and Communication Questions:

### Meeting Frequency:
- How often would you like to meet with us for project updates and progress reviews?

---

### Demo Reviews:
- Would you prefer incremental demos (e.g., for each feature) or a larger demo after major milestones?
- What format do you prefer for the demos? (e.g., live presentations, recorded video walkthroughs, or written reports with screenshots).

---

## Feedback
- After we present demos, how quickly do you expect to provide feedback? If it is not live.

---

## Documentation and Reporting 
- Would you prefer detailed weekly reports on our progress, or would you like summaries after each project milestone? And if there is any structure prefered for the reporting?

  ---

## Stakeholder Involvement
- Who are the key decision-makers for the cubing and slotting algorithms?

---

## Escalation Process

- If we encounter significant challenges or delays, who should we contact to address the issue, and how quickly do you expect us to resolve it?

---

## Preffered Communication Channels

- Do you prefer day-to-day communication via email?

---

## Timelines and Deadlines

- Are there any specific deadlines or timelines we need to keep in mind for completing the slotting algorithm or cubing algorithm? Our deadline is end of December :)

---

## Expectations for Testing

- At what point should we conduct testing? Will your team be involved in testing or user acceptance?

---

## Approval Process

- How will final approvals be handled for each part of the project? Who needs to sign off on the completed slotting or cubing algorithm?


# Slotting Optimization for Pickline in Warehouse

---

## General Questions for the Project

### 1. Project Scope Clarification:
- Could you clarify the exact scope of this project? Should the focus be only on the slotting algorithm, or will it also involve additional systems, such as data visualization or integration with existing warehouse management systems?
- Is there a preference between working on Slotting Optimization or Cubing Algorithm, or do you expect a combination of both in the project?

---

### 2. Constraints Prioritization:
- What are the most critical constrains that should be considered when determining product placement?
- Are there any constraints that take precedence over others, such as prioritizing products with higher demand or those that are more difficult to handle?

---

### 3. Repofile List Details:
- How is the repofile list generated?
- What criteria are used to compile the list, and is it generated manually or by software?
- What key fields does the repofile list contain (e.g., Product IDs, Picking areas), and what format is used (CSV, JSON, etc.)?

---

### 4. Product and Location Master Data:
- Could you describe the structure of the product and location master data files?
- What key attributes (e.g., product dimensions, weights, demand frequency) are included?

---
### 5. Handling Similar Products:
- What is meant by "not placing similar products next to each other"? Does this refer to visual similarity (e.g., color/packaging) or product function (e.g., similar nutritional supplements)?
- Should similar products be separated due to confusion in the picking process?

---

### 6. Manual Override and Visualization:
- How detailed should the visual representation of product placement be? Should it show just the product position or also include factors like picker reachability and ergonomic factors?
- Should users have the ability to manually override product placement? What level of control is expected (e.g., drag-and-drop adjustments)?
- How should the output be presented for quick inspection and manual corrections?

---

### 7. Feedback Mechanism:
- Is there a feedback mechanism for users to interact with the system, such as learning from manual overrides?

---

### 8. KPIs for Success:
- What key performance indicators (KPIs) will be used to measure the success of the system? For example, picking speed, error rate, or space utilization?
- How will the system's performance be tracked post-deployment, and will there be ongoing adjustments?

### 9. Current Tools and Systems:
- What systems or tools are currently in place for data analytics, product master data, or location master data?
- Are there existing APIs, databases, or software systems we need to integrate with?
- What types of databases are used (SQL, NoSQL), and can we access them?

---

### 10. Development Environment:
- Is there an existing development environment (e.g., cloud services, servers) or do we need to set this up from scratch?
- Are there any preferred IDEs, programming languages, or development tools we should use?


---

# Cubing Algorithm

---

### 1. Clarification of Scope:
- Could you clarify the scope of the cubing algorithm project? Is the main focus on improving how products are fitted into boxes, or are there other goals like optimizing the packing process as a whole?
- Are there specific metrics, such as box utilization or error reduction, that we should aim to improve?

---

### 2. Current Algorithm and Challenges:
- Could you explain how the existing cubing algorithm works? How are products currently assigned to boxes?
- What limitations does the current cubing process have? Is it primarily about fitting dimensions into boxes, or are there other challenges?
- How often do errors occur when boxes fit volume-wise but not physically due to product dimensions?

---

### 3. Data and Inputs:
- Could you provide the structure of the product master data? What attributes are important for the cubing algorithm (e.g., weight, packaging type, fragile items)?
- What are the dimensions and constraints for each of the five box types (e.g., weight restrictions, volume capacity)?
- How is order data organized, and what key fields are included? Is there a standard format (e.g., CSV, JSON)?

---

### 4. Algorithm and Optimization Process:
- Could you describe the current workflow of the cubing process and how box types are selected for specific orders?
- Should the algorithm prioritize minimizing the number of boxes, maximizing box utilization, or both?
- Should constraints beyond volume and dimensions, such as product weight and orientation, be considered?
- Could you explain the **minimal bounding box** concept, and how this should be applied in the algorithm?
- What are your expectations for a 3D visualization of product placement? Should the system show how each item fits within the box, and account for product orientation?

---

### 5. Constraints and Prioritization:
- Are there any additional constraints we should consider, such as product weight, fragile items, or orientation limits?
- Should similar products be grouped together within the same box, or does it not matter as long as they fit?

---

### 6. Manual Override and Visualization:
- Should users be able to manually adjust the algorithm's box selections or product placement? What level of control should they have?
- Should the 3D visualization include real-time adjustments, where users can move products within the virtual box?
- Is the visualization intended for quick inspection and adjustments, or should it serve as a detailed tool for managing the packing process?

---

### 7. Development Environment and Tools:
- Is there a pre-existing development environment (cloud services, servers, etc.) we should use?
- Are there preferred frameworks or libraries for developing the cubing algorithm in Python?
- Should the new algorithm integrate with existing systems, such as an ERP or WMS? Are APIs available for integration?

---

### 8. KPIs for Success:
- What key performance indicators (KPIs) will be used to measure the success of the new cubing algorithm?
- Are there specific goals, such as increasing box utilization, reducing errors, or speeding up the packing process?

---

### 9. Future Scalability:
- Should the system be designed to handle future growth, such as an increase in products, box types, or regions served?
- Are there plans to add more complex packaging rules in the future that the system should be able to accommodate?

---

# Additional Questions for Both Assignments

- What options have already been considered and tested to improve the stock placement and cubing processes? What were the results of those tests?
- How does the current data analytics process support these processes?
- For manual corrections and overrides, how would you like the system to manage and track these adjustments?

---


