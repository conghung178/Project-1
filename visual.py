import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# Hàm vẽ hình các đối tượng trong không gian 3D
def draw_box(ax, origin, size, color):
    x, y, z = origin
    dx, dy, dz = size
    
    vertices = [
        [x, y, z],
        [x + dx, y, z],
        [x + dx, y + dy, z],
        [x, y + dy, z],
        [x, y, z + dz],
        [x + dx, y, z + dz],
        [x + dx, y + dy, z + dz],
        [x, y + dy, z + dz]
    ]

    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],
        [vertices[4], vertices[5], vertices[6], vertices[7]],
        [vertices[0], vertices[1], vertices[5], vertices[4]],
        [vertices[2], vertices[3], vertices[7], vertices[6]],
        [vertices[1], vertices[2], vertices[6], vertices[5]],
        [vertices[4], vertices[7], vertices[3], vertices[0]]
    ]
    
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='r', alpha=.25))

def visual_plot(lst_box, size_bin):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    large_box = ((0, 0, 0), (size_bin[0], size_bin[1], size_bin[2]), 'cyan')
    draw_box(ax, *large_box)
    color = ['blue', 'green', 'red', 'purple', 'yellow', 'orange']

    for box in lst_box:
        origin = (box[0], box[1], box[2])
        size = (box[3], box[4], box[5])
        box_color = color[np.random.randint(0, len(color))]
        draw_box(ax, origin, size, box_color)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Bin Packing Visualization')

    ax.set_xlim(0, size_bin[0])
    ax.set_ylim(0, size_bin[1])
    ax.set_zlim(0, size_bin[2])

    plt.show()

def main():
    lst_box = [[2,2,2,3,4,5],[0,0,0,1,2,3],[0,0,3,1,2,3]]
    size_bin = [10,10,10]
    visual_plot(lst_box,size_bin)
if __name__ == '__main__':
    main()