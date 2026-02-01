import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d

class Painter:

    def __init__(self, box):
        ''' '''
        self.items = box.get_items()
        self.width = box.get_dimentions()[0]  # Width (X-axis)
        self.length = box.get_dimentions()[1]  # Length (Y-axis)
        self.height = box.get_dimentions()[2]  # Depth/Height (Z-axis)

    def _plotCube(self, ax, x, y, z, dx, dy, dz, color=None, mode=2, linewidth=1, text="", fontsize=15, alpha=0.6):
        """
        Auxiliary function to plot a cube with corrected axis mappings:
        X = Width, Y = Length, Z = Height.
        """
        xx = [x, x, x + dx, x + dx, x]
        yy = [y, y + dy, y + dy, y, y]
        zz = [z, z + dz]

        # Generate a random color if none is provided
        def random_color():
            return (x / self.width, y / self.length, z / self.height)

        if color is None:
            color = random_color()
            alpha = 0.1

        kwargs = {'alpha': alpha, 'color': color, 'linewidth': linewidth}

        # Plot wireframe for cube boundaries
        for z_val in zz:
            ax.plot3D(xx, yy, [z_val] * 5, **kwargs)  # Plot top and bottom faces
        for i in range(4):
            ax.plot3D([xx[i], xx[i]], [yy[i], yy[i]], [zz[0], zz[1]], **kwargs)  # Plot vertical edges

            # Vertices of the cube
        vertices = [
            # Bottom face
            [x, y, z], [x + dx, y, z], [x + dx, y + dy, z], [x, y + dy, z],
            # Top face
            [x, y, z + dz], [x + dx, y, z + dz], [x + dx, y + dy, z + dz], [x, y + dy, z + dz]
        ]

        # Faces of the cube
        faces = [
            # Bottom face
            [vertices[0], vertices[1], vertices[2], vertices[3]],
            # Top face
            [vertices[4], vertices[5], vertices[6], vertices[7]],
            # Front face
            [vertices[0], vertices[1], vertices[5], vertices[4]],
            # Back face
            [vertices[2], vertices[3], vertices[7], vertices[6]],
            # Left face
            [vertices[0], vertices[3], vertices[7], vertices[4]],
            # Right face
            [vertices[1], vertices[2], vertices[6], vertices[5]],
        ]

        # Add faces to the plot with color and transparency
        poly3d = art3d.Poly3DCollection(faces, alpha=alpha, facecolors=color, linewidths=linewidth, edgecolor='black')
        ax.add_collection3d(poly3d)

        # Add text label
        if text != "":
            if alpha < 0.5:
                ax.text( (x+ dx/2), (y+ dy/2), (z+ dz/2), str(text),color='black', fontsize=fontsize, ha='center', va='center')
            else:
                ax.text(
                    (x+ dx/2), (y+ dy/2), (z+ dz/2), text,
                    color='black', fontsize=fontsize, ha='center', va='center',
                    transform=ax.transData, bbox=dict(facecolor='white', alpha=1, boxstyle='round,pad=0.2'),
                    zorder=100  # Ensure the text is drawn on top
                )

    def plotBoxAndItems(self, title="", alpha=0.2, fontsize=10, limit=None, old_limit=None):
        """
        Plot the box and its items with corrected axis mappings.
        """
        fig = plt.figure()
        axGlob = plt.axes(projection='3d')

        # Plot the box
        self._plotCube(
            axGlob, 0, 0, 0,
            float(self.width),  # Width (X-axis)
            float(self.length),  # Length (Y-axis)
            float(self.height),  # Height (Z-axis)
            color="blue",  # Transparent fill
            mode=1, linewidth=1, alpha=0.1, text=""  # Edges with light transparency
        )

        # Plot items
        for i, item in enumerate(self.items):
            if limit is not None and i >= limit:
                break
            x, y, z = item.position  # X = Width, Y = Length, Z = Height
            dx, dy, dz = item.dimension  # Width, Length, Height

            sub_alpha = alpha

            # Check if the item is the last in the list
            if (limit is not None and i == limit - 1) or (old_limit is not None and old_limit - 1 <= i):
                color = 'red'  # Highlight the last item with a different color
                sub_alpha = 0.6  # Increase transparency for the last item
            else:
                color = None

            self._plotCube(
                axGlob, float(x), float(y), float(z),
                float(dx), float(dy), float(dz),
                color=color, mode=2, text=item.name, fontsize=fontsize, alpha=sub_alpha
            )

        # Set axis limits and labels
        axGlob.set_xlim(0, self.width)  # X = Width
        axGlob.set_ylim(0, self.length)  # Y = Length
        axGlob.set_zlim(0, self.height)  # Z = Depth/Height

        axGlob.set_xlabel("Width (X)")
        axGlob.set_ylabel("Length (Y)")
        axGlob.set_zlabel("Height/Depth (Z)")

        # Ensure equal scaling for all axes
        self.setAxesEqual(axGlob)

        # Add small circle and origin
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = 0.1 * np.outer(np.cos(u), np.sin(v))  # x = radius * cos(u) * sin(v)
        y = 0.1 * np.outer(np.sin(u), np.sin(v))  # y = radius * sin(u) * sin(v)
        z = 0.1 * np.outer(np.ones(np.size(u)), np.cos(v))  # z = radius * cos(v)

        axGlob.plot_surface(x, y, z, color='b', alpha=0.3)  # Plot the small circle around (0,0,0)
        axGlob.scatter(0, 0, 0, color="green", s=100, label="Origin")  # A point at (0, 0, 0)

        # Close the figure to free memory
        plt.close(fig)

        return fig

    def setAxesEqual(self, ax):
        """
        Set axes to equal scale.
        """
        x_limits = [0, self.width]
        y_limits = [0, self.length]
        z_limits = [0, self.height]

        ax.set_xlim(x_limits)
        ax.set_ylim(y_limits)
        ax.set_zlim(z_limits)

        # Enforce aspect ratio manually
        x_range = x_limits[1] - x_limits[0]
        y_range = y_limits[1] - y_limits[0]
        z_range = z_limits[1] - z_limits[0]
        max_range = max(x_range, y_range, z_range)

        ax.set_box_aspect((x_range / max_range, y_range / max_range, z_range / max_range))