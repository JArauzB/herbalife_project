# Visualization with PyQt6

I've significantly upgraded visualization by **transitioning from Tkinter** to **PyQt6**. The screenshots below demonstrate both the **default theme** and a **color-blind-friendly** theme. The move to PyQt6 not only gives the interface a more modern look and feel, but it also resolves a series of compatibility problems I encountered with Tkinter on macOS—especially on Apple Silicon (M chip) devices, where Tkinter windows would sometimes fail to appear entirely.

## Visualisation using Tkinter
![image_2024-12-10_14-04-16 (1)](https://github.com/user-attachments/assets/23a24ed9-add9-47e0-be47-005249792265)

---

## Why I Moved from Tkinter to PyQt6

- **Superior Mac Compatibility**  
  When I tested my Tkinter-based application on an Apple M2 MacBook, the GUI often displayed blank windows or simply wouldn’t render at all—indicating architectural conflicts or incomplete library support. Conversely, PyQt6 has proven to be rock-solid on Windows, macOS (including Apple Silicon), and Linux.

- **Modern, Feature-Rich Widgets**  
  - **High-DPI Support**: PyQt6 automatically adapts to high-resolution monitors, including Retina displays, ensuring crisp, clear visuals.  
  - **Advanced Layouts**: Layout managers like `QVBoxLayout` and `QHBoxLayout` allow building sophisticated UIs without manual widget positioning.  
  - **Refined Effects**: Built-in drop shadows (`QGraphicsDropShadowEffect`) and stylesheet-based theming help me create a polished, professional interface.

- **Cleaner Code & Architecture**  
  - **Signals and Slots**: PyQt6’s communication model is both powerful and straightforward, making the code more modular and maintainable.  
  - **Modular Design**: It’s now easier to spread the application’s logic across multiple files, which is critical as the project grows.

---

## Introducing the `OrderVisualizer` Class

### Key Responsibilities

1. **Order Loading and Display**  
   - Reads data from a CSV file (via my custom `Reader` class).  
   - Manages a list of `Order` objects. Each order can have multiple boxes, and each box holds several items.  
   - Presents the orders in a scrollable `QListWidget`, so you can pick the one you want to explore.

2. **Box and Item Navigation**  
   - Allows quick switching to the **next** or **previous** box within an order (helpful when orders contain multiple boxes).  
   - Each box can contain many items, so you can step through items one by one or in groups of ten—making it straightforward to review packing arrangements.

3. **Matplotlib Visualization**  
   - Embeds a Matplotlib 3D plot in a `FigureCanvasQTAgg`.  
   - Dynamically updates the scene as you navigate between boxes or items, making it easy to see how items occupy the box space.

4. **Themes and Accessibility**  
   - Employs external stylesheets, including a **color-blind-friendly theme** (protanopia, deuteranopia, tritanopia). Simply **click the logo** in the corner to cycle through available themes.  
   - High-DPI scaling ensures everything looks sharp on modern monitors.

5. **Security Measures**  
   - Since it’s a local visualization tool, it primarily reads CSV data in a controlled format—no arbitrary code execution.  
   - I keep dependencies like PyQt6, Matplotlib, and pandas up to date to ensure any security patches are applied.  
   - I avoid embedding sensitive credentials or other private data in the code or CSV.

---

## How It Works

1. **Startup**  
   - A `QApplication` is created, and an `OrderVisualizer` object is instantiated.  
   - If you pass a CSV file path in the command line, it automatically loads the orders on launch.

2. **Order Selection**  
   - The left-hand side includes a `QListWidget` displaying all available order IDs. Choosing one triggers `select_order()`, which updates the display.

3. **Box Display & Item Navigation**  
   - The top bar shows the current order ID and how many items (out of the total) are being visualized.  
   - **Next/Previous Box** buttons move between boxes in the order.  
   - **Item Navigation** allows you to move backward or forward by 1 or 10 items.

4. **Matplotlib 3D Plot**  
   - Leveraging the `Painter` class, each box is drawn in a wireframe style, while items appear as colored cuboids labeled with their IDs and dimensions.  
   - Every time you click a navigation button, `update_plot()` refreshes the scene accordingly.

5. **Theme Switching**  
   - Clicking the application logo cycles through different stylesheets, including color-blind-friendly options.  
   - Colors, text, and backgrounds are adjusted automatically for better contrast and accessibility.

---

## Screenshots

Below are three images showcasing different themes, including color-blind-friendly variations. Observe the shadowed panels, item labeling in the 3D plot, and intuitive layout for reviewing orders and boxes.

![Default Theme](https://github.com/user-attachments/assets/df0c6e11-89c3-4b06-b3bb-21d8b18c807b)
![Color-Blind-Friendly 1](https://github.com/user-attachments/assets/6cd2dff2-1e0c-4ea9-a0fa-dd0429193300)
![Color-Blind-Friendly 2](https://github.com/user-attachments/assets/4c191e23-b10f-4315-abd8-d5451450a582)

---

## Why PyQt6 Delivers a Better Experience

1. **Smooth Performance**  
   - Handles large datasets gracefully thanks to Qt’s efficient event loop and Matplotlib’s robust rendering engine.

2. **Adaptive Layouts**  
   - Changes in UI elements—such as adding fields—are handled seamlessly, freeing you from manual geometry adjustments.

3. **Apple Silicon Support**  
   - No more blank windows or UI glitches on M1 Macs; PyQt6 is well-supported on Apple Silicon.

4. **Improved Aesthetics and Accessibility**  
   - CSS-based styling offers straightforward customization, while color-blind-friendly palettes ensure inclusivity.

---

## Conclusion

Switching to **PyQt6** has transformed this visualization tool into a far more **professional, stable,** and **accessible** application. It runs smoothly on macOS (including M1 devices), Windows, and Linux, allowing me to focus on enhancing functionality rather than troubleshooting platform quirks. If you’re curious about the code or have any questions, feel free to check out the repository—or just drop me a line!
