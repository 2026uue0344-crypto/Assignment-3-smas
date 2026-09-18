import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

img = Image.open("sample_image.png").convert("RGB")

A1 = np.array([[2, 0], [0, 0.5]])
A2 = np.array([[0, -1], [1, 0]])
A3 = np.array([[1, 1], [0, 1]])
A4 = np.array([[-1, 0], [0, 1]])
A5 = np.array([[1, 0], [0, 0]])

matrices = [A1, A2, A3, A4, A5]
names = ["A1 Scaling", "A2 Rotation", "A3 Shear",
         "A4 Reflection", "A5 Projection"]

def transform(img, A):
    w, h = img.size
    cx, cy = w // 2, h // 2

    if np.linalg.det(A) == 0:
        A = np.array([[1, 0], [0, 0.1]])

    B = np.linalg.inv(A)

    corners = np.array([
        [0-cx, 0-cy],
        [w-cx, 0-cy],
        [0-cx, h-cy],
        [w-cx, h-cy]
    ])

    new = corners @ A.T
    minx, miny = new.min(axis=0)
    maxx, maxy = new.max(axis=0)

    nw = int(maxx - minx) + 1
    nh = int(maxy - miny) + 1

    a, b = B[0]
    c, d = B[1]

    return img.transform(
        (nw, nh),
        Image.Transform.AFFINE,
        (a, b, cx - a*minx - b*miny,
         c, d, cy - c*minx - d*miny)
    )

for name, A in zip(names, matrices):
    print("\n", name)
    print("T(e1) =", A[:, 0])
    print("T(e2) =", A[:, 1])
    print("Rank =", np.linalg.matrix_rank(A))

    if np.linalg.matrix_rank(A) == 1:
        print("Information lost: YES")
    else:
        print("Information lost: NO")

    plt.figure()
    plt.imshow(transform(img, A))
    plt.title(name)
    plt.axis("off")
    plt.show()