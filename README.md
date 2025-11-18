# Image FT Mixer Pro

> **Image FT Mixer Pro** analyzes, visualizes, and manipulates images in the Fourier domain, allowing users to mix up to four images’ Fourier Transform components.
> ![Project Overview](https://github.com/user-attachments/assets/b8ffaf4a-2fec-4b79-bf3a-53575c012cdb)

---

## Video Demo

https://github.com/user-attachments/assets/cad8e300-f260-4d07-84e3-59fb6c6d8f17

---

## Core Features

### Multi-Image Viewports & Preprocessing

* **Four Viewports**: Load and view four images in separate windows.
* **Automatic Grayscale Conversion**: Colored images are converted to grayscale on load.
* **Unified Sizing**: All images resized to match the smallest image, ensuring consistent FT processing.

### Interactive Fourier Transform Analysis

* **Dynamic Component Mode**: Switch globally between `Magnitude/Phase` or `Real/Imaginary` modes.
* **Optimized Visualization**:

  * Magnitude: Log-scaled, normalized, color-mapped (e.g., INFERNO).
  * Phase: Scaled and color-mapped (e.g., MAGMA).
  * Real/Imaginary: Log-scaled absolute values with gamma correction (PLASMA/CIVIDIS).

### Brightness & Contrast Adjustment

* **Mouse Drag Controls**: Vertical drag adjusts brightness, horizontal drag adjusts contrast.
* **Reset Option**: Restore default B/C per image.

### Image Mixing

* **Component Mixer**: Set contribution of each image's FT component with weight sliders (0-100%).
* **Region Mixer**: Apply a 2D Gaussian filter for smooth, high-fidelity frequency-domain mixing.

  * **Inner (Low-Freq)**: Preserves low-frequency content (smoothness of the Gaussian filter).
  * **Outer (High-Freq)**: Preserves high-frequency content (inverse of the Gaussian filter).
  * **Adjustable Sigma**: Modify the smoothness and cutoff frequency using the Gaussian Standard Deviation ($\sigma$) slider.

### Output & Asynchronous Operation

* **Two Output Ports**: `Output 1` and `Output 2` display the mixed images.
* **Asynchronous Mixing**: Dedicated worker thread ensures GUI remains responsive. Previous mixing jobs cancel automatically.
* **Progress Bar**: Displays ongoing mixing status.
* **Save Output**: Save the selected output viewport as `.png` or `.jpg`.

---

## Technical Highlights

### Architecture

* **UI Layer (`app/gui`)**: Handles GUI layout and user interactions.
* **Application Logic (`main.py`)**: Manages state, file I/O, events, and thread orchestration.
* **Core Logic (`app/core`)**:

  * `ImageProcessor`: Normalization, resizing, brightness/contrast.
  * `FFTAnalyzer`: FT computation and visualization.
  * `Mixer`: Mixing algorithms and region masking.
* **Asynchronous Processing (`app/workers`)**: Uses PyQt signals for cross-thread communication.

### Technologies Used

| Component            | Technology         | Purpose                                                          |
| -------------------- | ------------------ | ---------------------------------------------------------------- |
| GUI Framework        | PyQt5              | Cross-platform interface                                         |
| Image Processing     | OpenCV (`cv2`)     | Grayscale conversion, resizing, B/C adjustment, FT visualization |
| Scientific Computing | NumPy              | FFT/IFFT and high-performance array operations                   |
| Custom UI            | `SegmentedControl` | Compact alternative to radio buttons                             |

---

### **Application Interface**

Below are illustrative screenshots of the application showcasing its key features:

1. **Main Interface with Four Image Viewports**

   ![UI Interface](https://github.com/user-attachments/assets/b4f81aeb-54a1-4780-9c40-849ada4cde75)


2. **Fourier Transform Component Selection**

   ![FT Component Selection](https://github.com/user-attachments/assets/a18335fb-0016-44fe-a850-437da611f069)


3. **Brightness/Contrast Adjustment**

   ![Brightness & Contrast](https://github.com/user-attachments/assets/1cb4f1b4-9b91-42f6-9a74-9d31fe7d79e8)


4. **Region Selection for FT Components**

   * **Inner Region**
     ![Inner Region](https://github.com/user-attachments/assets/0f064076-52aa-433c-95d2-d52918e9508e)

   * **Outer Region**
     ![Outer Region](https://github.com/user-attachments/assets/4b5bf23e-21a1-458e-ab92-e245726e3aec)


---

## Setup & Installation

1. **Clone Repository**:

```
git clone https://github.com/madonna-mosaad/FT-Magnitude-Phase-Mixer.git
```

2. **Navigate to Directory**:

```
cd FT-Magnitude-Phase-Mixer
```

3. **Install Dependencies**:

```
pip install -r requirements.txt
```

4. **Run Application**:

```
python Main.py
```

---

## Usage Instructions

1. **Load Images**: Double-click any viewport to open and load an image.
2. **Adjust B/C**: Drag inside a viewport to adjust brightness (vertical) and contrast (horizontal). Reset via `Reset B/C`.
3. **Select FT Mode**: Switch between `Magnitude/Phase` or `Real/Imaginary`.
4. **Select Components**: Choose which FT component of each image contributes to mixing.
5. **Set Weights**: Use sliders to control component influence.
6. **Apply Region Mask**: Choose `Inner`, `Outer`, or `None` and adjust the Gaussian Sigma ($\sigma$).
7. **View Output**: Result appears in selected output port.
8. **Save Result**: Click `Save Mixed Output` to store the image.

---

## Contributors

<div>
<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/YassienTawfikk" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/126521373?v=4" width="150px" alt="Yassien Tawfik"/>
        <br /><sub><b>Yassien Tawfik</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/madonna-mosaad" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/127048836?v=4" width="150px" alt="Madonna Mosaad"/>
        <br /><sub><b>Madonna Mosaad</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/nancymahmoud1" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/125357872?v=4" width="150px" alt="Nancy Mahmoud"/>
        <br /><sub><b>Nancy Mahmoud</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/yousseftaha167" target="_blank">
        <img src="https://avatars.githubusercontent.com/u/128304243?v=4" width="150px" alt="Youssef Taha"/>
        <br /><sub><b>Youssef Taha</b></sub>
      </a>
    </td>
  </tr>
</table>
</div>
