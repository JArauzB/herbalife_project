## First Meeting

### Contact:
- Contact person: Marc Wilmsen
- Marc Wilmsen also wrote the assignments

### Company Goal:
- Selling weight losing/gaining products
- Multi level marketing business

### Assignment:
- Both assignments are of equal priority, but there is a potential resolution for the Product Slotting. Choosen for assignment: **Cubing**
- Issue: The current solution bases on the combined volume of the products.
- Why is this an issue: The current solution does not take into account the metrics per product.
- Example "false true": box is 12.5 x 12.5 x 25 cm, there are 3 products is 10 x 10 x 10 cm, the box's volume is 3906.25 cm^3, the products' volume is 3000 cm^3, which currently results in a false true. Whilst the products don't actually fit in the box.
- Assignment: Play tetris with the products in the box
- Nice To have: A visual representation of the products in the box
- Further research (post assignment): Cut the box into a perfectly fitting box instead of assigning one of the available boxes.
- Deadline: No clear deadlines, as a group we decided the week before the christmas/new year break is the deadline for the assignment.
- Input: We receive an excel sheet with actual orders (without precise product numbers and personal information) and the products' dimensions.
- Output: An excel sheet with the box to use for the order. (NTH - A visual representation of the products with orientation in the box)
- Lamguage: Python
- Most important focus: The smaller boxes (most problems occur with the smaller boxes)
- Box sizing: [Large,Medium,Small,Extra Small,Extra Extra Small,Envelope]

The assignment involves optimizing the packing of products into boxes, specifically focusing on smaller boxes where most issues occur. The current solution, which is based on the combined volume of products, is inadequate as it does not consider individual product dimensions, leading to incorrect fits. The task is to develop a Python-based solution that effectively plays "Tetris" with the products to ensure they fit into the designated boxes. A visual representation of the packing process is a desirable feature. For our assignment the output should be an Excel sheet indicating the appropriate box for each order, with a potential visual representation of product orientation within the box. The deadline is set for the week before the Christmas/New Year break. Input data will be provided in the form of an Excel sheet containing order details and product dimensions.

### Meetings:
- Bi-weekly meetings (every other week), once at campus then at the company's location (unless otherwise agreed upon)
- Meetings always on the same day and time (Thursday 12:00? TBC)

### Process:
- Boxes are weighed before products are added
- Products are added to the box
- Box is weighed again
- If the weight is too high/low, the box is controlled and if incorrect the box is sent over the belt again