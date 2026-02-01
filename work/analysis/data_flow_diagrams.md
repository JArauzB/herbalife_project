## Data Flow Diagrams
This part will contain all diagrams used for the project analysis provided by the customer and new diagramss created by the team


#### PSA(Standard process flow)
![Alt text](/analysis/images/standard_process_flow_current_alg.png)

#### Explanation
All pick lines of an order are pre-sorted by location in ascending order and quantity in descending order and the volume calculation process starts working order line by order line. The system calculates the quantity of the ordered item that will fit in a container using the dimensions and the weight. A container is generated and the calculated quantity is assigned to it. If parts of the pick line fail to be assigned to this container due to volumetric values a new carton/tote is used. When the total quantity of a pick line is processed and the last generated container is not filled up completely, the system will try to use this container for the next line as long as the weight and volume restrictions of the container are not exceeded. Whenever the maximum allowed weight of a carton/tote is reached, a new container is generated. Unused volume of container will not be filled with partial ordered quantity of smaller items. The two situations where non-item-clean container are built are:
 

One line is processed and a new line or parts of a new line can use the remaining space of the container

 

The total ordered quantity of a smaller item fits into a already used carton/tote

 

therefore the criteria of using the minimum quantity of necessary container is overruled by the requirement of preferred item-clean cartons/totes. The percentage of a container’s volume that will be used is maintainable as a system parameter.