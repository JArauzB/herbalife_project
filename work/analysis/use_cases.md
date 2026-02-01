# Use case diagram

![Alt text](/analysis/images/use_case_diagram.png)


# Use case description


| **Field**             | **Details**                                                                                          |
|-----------------------|------------------------------------------------------------------------------------------------------|
| **Name**              | Calculate best fitting box(es) for order                                                             |
| **Actor**             | Machine                                                                                               |
| **Description**       | The algorithm that is responsible for the calculation of the cubing system within the box             |
| **Pre-condition**     | Having an excel document with order details                                                           |
| **Scenario**          | 1. The actor import the excel file<br>2. The system calculates the best fitting box which is returned as an Excel document                                         |
| **Result**            | An Excel document with the best fitting box for the products of one order                              |
| **Exception**         | None                                                                                                   |
| **Extension**         | None          

# Use case scenario


<table>
  <tr>
    <th><strong>Field</strong></th>
    <th><strong>Details</strong></th>
  </tr>
  <tr>
    <td><strong>Name</strong></td>
    <td>Calculate best fitting box(es) for order</td>
  </tr>
  <tr>
    <td><strong>Actor</strong></td>
    <td>Machine</td>
  </tr>
  <tr>
    <td><strong>Description</strong></td>
    <td>The algorithm that is responsible for the calculation of the cubing system within the box</td>
  </tr>
  <tr>
    <td><strong>Pre-condition</strong></td>
    <td>Having an Excel document with order details</td>
  </tr>
  <tr>
    <td><strong>Scenario</strong></td>
    <td>
      <ol>
        <li>The actor imports the following input:
          <table border="1">
            <tr>
              <th>Ordernr</th>
              <th>Weight</th>
              <th>ProductID</th>
            </tr>
            <tr>
              <td>2100388381</td>
              <td>1284</td>
              <td>5207</td>
            </tr>
            <tr>
              <td>2100388381</td>
              <td>665</td>
              <td>5590</td>
            </tr>
            <tr>
              <td>2100388381</td>
              <td>282</td>
              <td>4919</td>
            </tr>
          </table>
        </li>
        <li>The system responds with:
          <table border="1">
            <tr>
              <th>Date</th>
              <th>Ordernr</th>
              <th>Boxnr</th>
              <th>Picked</th>
              <th>Location</th>
              <th>Box Name</th>
              <th>Weight</th>
              <th>ID</th>
            </tr>
            <tr>
              <td>9-2-2024 00:00</td>
              <td>2100388381</td>
              <td>13916558</td>
              <td>2</td>
              <td>05D10</td>
              <td>XS</td>
              <td>1284</td>
              <td>5207</td>
            </tr>
            <tr>
              <td>9-2-2024 00:00</td>
              <td>2100388381</td>
              <td>13916558</td>
              <td>1</td>
              <td>08D12</td>
              <td>XS</td>
              <td>665</td>
              <td>5590</td>
            </tr>
            <tr>
              <td>9-2-2024 00:00</td>
              <td>2100388381</td>
              <td>13916558</td>
              <td>1</td>
              <td>02C08</td>
              <td>XS</td>
              <td>282</td>
              <td>4919</td>
            </tr>
          </table>
        </li>
      </ol>
    </td>
  </tr>
  <tr>
    <td><strong>Result</strong></td>
    <td>An Excel document with the best fitting box for the products of one order</td>
  </tr>
  <tr>
    <td><strong>Exception</strong></td>
    <td>None</td>
  </tr>
  <tr>
    <td><strong>Extension</strong></td>
    <td>None</td>
  </tr>
</table>
