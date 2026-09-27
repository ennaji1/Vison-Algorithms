# Vision Algorithms — Camera Projection

Personal Python implementation of **Exercise 01: Augmented reality wireframe cube**, from the [Vision Algorithms for Mobile Robotics (VAMR) course](https://rpg.ifi.uzh.ch/teaching.html#VAMR), Robotics and Perception Group, University of Zurich.

This exercise connects camera geometry with image processing: project known 3D checkerboard corners into an image, draw a virtual cube, model radial lens distortion, and reconstruct an undistorted image. Camera intrinsics and world-to-camera transformations are supplied with the exercise; the code uses these values rather than estimating calibration.

## Current implementation

- Project a grid of 9 × 6 checkerboard corners, spaced 4 cm apart.
- Convert an axis-angle rotation vector into a rotation matrix using Rodrigues' formula.
- Overlay an 8 cm wireframe cube on the checkerboard.
- Apply the provided radial distortion model to projected points.
- Undistort the first image using backward mapping and nearest-neighbor sampling.

The demos currently use `img_0001.jpg` and the first pose. The cube extends along negative world Z, according to the checkerboard frame used in the exercise. Its size and position are defined directly in `main.py`.

The vectorized implementation is still an empty template. Video generation and the bonus bilinear interpolation are not implemented. The numerical questions on PDF pages 9–10 are separate written exercises; their solutions are not included here.

## Libraries used

| Library | Role in this project |
| --- | --- |
| NumPy (`numpy`) | Arrays, matrix multiplication, norms, trigonometry, and image buffers. |
| OpenCV (`opencv-python`, imported as `cv2`) | Read and display images; draw projected points and cube edges. |
| Matplotlib (`matplotlib`) | Imported in the demo scripts, but currently unused; visualization uses OpenCV. |
| `pathlib` | Build file paths. Part of Python's standard library, so no separate installation is needed. |

`python_code/requirements.txt` records pinned dependencies, including supporting packages such as Pillow and Matplotlib dependencies. The statement specifies Python 3.12.3 as its reference version.

## Run the demos

With your virtual environment activated, start from the repository root:

```sh
cd "01_camera_projection - exercise/python_code"
python -m pip install -r requirements.txt
python main.py
```

Run from this directory because the calibration-loading functions use paths such as `../data/K.txt`.

`main.py` displays three results in sequence:

1. Checkerboard corners projected onto the supplied undistorted image.
2. A wireframe cube on that image.
3. Checkerboard corners projected onto the original distorted image.

Press any key while each image window is focused to advance. A desktop environment with OpenCV window support is required.

To run image undistortion separately:

```sh
python undistort_image.py
```

This script displays the corrected image. It uses nested pixel loops and currently reloads the distortion coefficients for each point, so it may take time to finish. Results are displayed rather than saved to disk.

## What each file does

Paths below are relative to `01_camera_projection - exercise/` unless stated otherwise.

| File or directory | Purpose |
| --- | --- |
| `python_code/main.py` | Runs the three projection demonstrations; constructs the checkerboard and cube, projects their points, and draws the overlays. |
| `python_code/project_points.py` | `project_points(points, K, R, t)` maps an `(N, 3)` array of world points to an `(N, 2)` array of pixel coordinates. Also contains duplicate calibration-loading helpers and prints the first rotation, translation, and intrinsic matrix when imported. |
| `python_code/pose_vector_to_transformation_matrix.py` | Provides `cacul_R(i)`, `calcul_t(i)`, and `calcul_K()` to load calibration and convert a pose's rotation vector. Despite its filename, it currently returns the components separately rather than assembling a 4 × 4 transformation. |
| `python_code/distort_points.py` | `distort_points(u, v, K)` applies the two-coefficient radial distortion model to scalar coordinates or arrays of coordinates. Reads coefficients from `D.txt`. |
| `python_code/undistort_image.py` | Creates an output image, maps each output pixel into the distorted source image, rounds to the nearest source pixel, and copies its color. Out-of-bounds samples remain black. |
| `python_code/undistort_image_vectorized.py` | Empty placeholder for the additional vectorization exercise. |
| `python_code/requirements.txt` | Pinned Python package dependencies. |
| `data/K.txt` | The 3 × 3 intrinsic matrix: focal lengths and principal-point coordinates in pixels. |
| `data/D.txt` | The radial distortion coefficients `k1` and `k2` for the exercise's pixel-coordinate model. |
| `data/poses.txt` | One world-to-camera transformation per image, stored as six values: rotation vector `(wx, wy, wz)` followed by translation `(tx, ty, tz)` in meters. |
| `data/images/` | Original images with lens distortion. Each `img_*.jpg` is a frame of the supplied sequence. |
| `data/images_undistorted/` | Supplied images with distortion already corrected, used for the first projection demonstrations. |
| `statement.pdf` | Original exercise instructions, mathematical definitions, reference figures, and numerical questions. |
| `preview.mp4` | Preview video supplied with the exercise material. |
| `/README.md` | This project guide at the repository root. |
| `/.gitignore` | Excludes virtual environments, Python caches, local helper files, and unused MATLAB templates from Git. |

## Mathematical model

For a world point `P = (X, Y, Z)`, the code first computes camera coordinates and then projects them:

```text
Pc = R @ P + t
q  = K @ Pc
u  = q[0] / q[2]
v  = q[1] / q[2]
```

Here `R` and `t` map the world frame to the camera frame. In `poses.txt`, the translation is the world origin expressed in the camera frame, not the camera position expressed in world coordinates. Checkerboard points use meters: `P(i, j) = (0.04*i, 0.04*j, 0)`.

The exercise defines radial distortion directly in pixel coordinates relative to the principal point `(u0, v0)`:

```text
r² = (u - u0)² + (v - v0)²
s  = 1 + k1*r² + k2*r⁴
ud = u0 + s*(u - u0)
vd = v0 + s*(v - v0)
```

Undistortion uses this forward distortion function to locate the source sample for each output pixel:

```text
I_undistorted[v, u] = I_distorted[round(vd), round(ud)]
```

Array indexing is `[row, column]`, or `[v, u]`. The current rotation conversion assumes a nonzero rotation-vector norm, and projection assumes nonzero camera depth.

## References and credits

- **Robotics and Perception Group, University of Zurich.** [Vision Algorithms for Mobile Robotics — teaching page](https://rpg.ifi.uzh.ch/teaching.html#VAMR), including Exercise 01, “Augmented reality wireframe cube.”
- **Exercise statement:** [Augmented reality wireframe cube](01_camera_projection%20-%20exercise/statement.pdf). Source for the camera conventions, projection equations, distortion model, and exercise tasks.

The exercise statement, dataset, and preview are supplied course materials. This repository contains a personal implementation of the Python exercises and is not an official course solution.
