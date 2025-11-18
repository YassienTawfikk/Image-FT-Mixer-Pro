import numpy as np
import cv2


class Mixer:
    """
    Handles the complex Fourier Transform mixing process and mask application.
    Decoupled from UI display logic.
    """

    def __init__(self):
        self._region_mode = "None"
        self._output_label_1 = None
        self._output_label_2 = None
        # Removed _output_selector as it's no longer necessary

    # --- Properties ---
    @property
    def region_mode(self):
        return self._region_mode

    def set_region_mode(self, mode):
        # Map segmented control text to internal mode
        if "Inner" in mode:
            self._region_mode = "Inner"
        elif "Outer" in mode:
            self._region_mode = "Outer"
        else:
            self._region_mode = "None"

    def set_output_labels(self, label1, label2):
        """
        Set references to UI output image elements.
        The selector reference is now handled solely in ApplicationLogic.
        """
        self._output_label_1 = label1
        self._output_label_2 = label2

    # --- Core Methods ---

    def mix_images(self, images, weights, component_selections, selector_region, min_height, min_width):
        """Mixes images based on selected components, weights, and region mode."""
        if min_width is None or min_height is None:
            return np.zeros((100, 100), dtype=np.uint8)

        # Initialize complex FT array
        combined_ft = np.zeros((min_height, min_width), dtype=np.complex128)

        # Extract the sigma value from the repurposed selector_region
        # selector_region is now [center_x, center_y, sigma, 0]
        sigma = selector_region[2]

        # Create the 2D Gaussian mask (Low-Pass Filter)
        gaussian_mask = self.__create_gaussian_mask(min_height, min_width, sigma)

        for i in range(4):
            if images[i] is None or weights[i] == 0.0:
                continue

            weight = weights[i]
            ft_image = np.fft.fft2(images[i])
            ft_image_shifted = np.fft.fftshift(ft_image)

            # 1. Apply Region Mask (using the pre-calculated Gaussian)
            ft_image_masked = self.__apply_region_mask(ft_image_shifted, gaussian_mask)

            # 2. Extract and Weight Component
            selected = component_selections[i]

            if selected in ["FT Magnitude", "FT Phase"]:
                # Magnitude/Phase mixing relies on combining weighted complex numbers
                magnitude = np.abs(ft_image_masked)
                phase = np.angle(ft_image_masked)

                if selected == "FT Magnitude":
                    # Weight the contribution of the full complex number
                    weighted_complex = weight * magnitude * np.exp(1j * phase)

                elif selected == "FT Phase":
                    # Use weighted phase information, maintaining original magnitude scale (1)
                    weighted_complex = weight * np.exp(1j * phase)

                combined_ft += weighted_complex

            elif selected in ["FT Real", "FT Imaginary"]:
                # Real/Imaginary mixing combines the complex parts directly

                real_part = np.real(ft_image_masked)
                imag_part = np.imag(ft_image_masked)

                if selected == "FT Real":
                    combined_ft += weight * (real_part + 0j)
                elif selected == "FT Imaginary":
                    combined_ft += weight * (0 + 1j * imag_part)

        # 3. Inverse Fourier Transform
        combined_ft_shifted = np.fft.ifftshift(combined_ft)
        mixed_image_complex = np.fft.ifft2(combined_ft_shifted)

        # Take magnitude for the final output image
        mixed_image = np.abs(mixed_image_complex)

        # 4. Normalize and return
        mixed_image_normalized = cv2.normalize(mixed_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        return mixed_image_normalized

    def __apply_region_mask(self, ft_data, gaussian_mask):
        """Apply a mask based on region mode (Inner, Outer, None)."""

        if self._region_mode == "None":
            # Mask remains all 1s (no masking)
            return ft_data

        if self._region_mode == "Inner":
            # Inner (Low-Freq) is the Gaussian mask itself (Low-Pass Filter)
            mask = gaussian_mask

        elif self._region_mode == "Outer":
            # Outer (High-Freq) is the inverse of the Gaussian mask (High-Pass Filter)
            mask = 1.0 - gaussian_mask

        # Apply the mask
        return ft_data * mask

    def __create_gaussian_mask(self, height, width, sigma):
        """Generates a centered 2D Gaussian mask (Low-Pass Filter) of the given size and sigma."""
        center_x = width // 2
        center_y = height // 2

        x = np.arange(width) - center_x
        y = np.arange(height) - center_y
        X, Y = np.meshgrid(x, y)

        distance_sq = X ** 2 + Y ** 2

        # Gaussian formula: G(u, v) = exp( - (u^2 + v^2) / (2 * sigma^2) )
        # Add epsilon (1e-6) to sigma**2 for stability
        mask = np.exp(-distance_sq / (2.0 * (float(sigma) ** 2 + 1e-6)))

        return mask
