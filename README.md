# smart-image-enhancer

Smart, folder-to-folder image enhancement CLI with multiple algorithms like CLAHE, AHE, and auto gamma correction.

Give it an input folder of images, choose one or all algorithms, and it writes enhanced versions to an output folder with clear, suffix-based filenames.

---

## Features

- **Folder in → folder out**: Batch-process entire directories (and subdirectories) of images.
- **Multiple algorithms** (extensible):
  - `clahe` – smart CLAHE with simple auto-tuned parameters.
  - `ahe` – placeholder for Adaptive Histogram Equalization.
  - `gamma_auto` – automatic gamma correction based on image brightness.
- **Smart parameters**: `--auto-params` uses image statistics to pick reasonable defaults.
- **Consistent naming**: For an input `image1.jpg` and algorithm `clahe`, output is `image1_clahe.jpg`.
- **Run all algorithms at once**: Use `--algo all` to get one output per algorithm per input image.

Planned additions include Retinex-based methods, tone mapping operators (Reinhard, log), homomorphic filtering, and deep-learning-based enhancers.

---

## Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/sharvinvarghese/smart-image-enhancer.git
cd smart-image-enhancer
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

---

## Usage

### Basic: single algorithm

```bash
python enhance.py \
  --input /path/to/input_folder \
  --output /path/to/output_folder \
  --algo clahe
```

- Takes every supported image from `input_folder`.
- Writes outputs into `output_folder`.
- For an input file `image1.jpg`, you get:
  - `image1_clahe.jpg`

### Smart parameters

```bash
python enhance.py \
  --input /path/to/input_folder \
  --output /path/to/output_folder \
  --algo clahe \
  --auto-params
```

This enables simple heuristics that adjust CLAHE and gamma parameters based on image brightness and contrast.

### Run all algorithms

```bash
python enhance.py \
  --input /path/to/input_folder \
  --output /path/to/output_folder \
  --algo all \
  --auto-params
```

For an input `image1.jpg`, this will produce:

- `image1_clahe.jpg`
- `image1_ahe.jpg`
- `image1_gamma_auto.jpg`

---

## Supported formats and limitations

- **Supported input formats**: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tif`, `.tiff` (8-bit images are recommended).
- **Output formats**: Match the input file extension.
- **Not yet supported**:
  - RAW camera formats (CR2, NEF, etc.).
  - Animated GIFs / multi-page TIFFs.
  - 16-bit or floating-point workflows (images will be treated as standard 8-bit).

If an unsupported file is found in the input folder, it is simply skipped.

---

## Roadmap

- True AHE, BBHE/DSIHE implementations.
- Retinex family (SSR, MSR, MSRCP).
- Tone mapping (logarithmic, Reinhard, HDR-style operators).
- Homomorphic filtering for uneven illumination.
- Optional deep-learning backends (Zero-DCE, EnlightenGAN, RetinexNet) behind an extra dependency flag.
- Small web demo / notebook examples.

---

## Contributing

Contributions are welcome! If you find a bug, want a new algorithm, or have a better heuristic:

1. **Open an issue** describing the problem or proposal.
2. **Submit a pull request (PR)** with a clear description and small, focused changes.

Please make sure to:

- Keep `enhance.py` as the main CLI entry point.
- Add new algorithms in `src/algorithms.py` and register them in `AVAILABLE_ALGOS`.
- Include a short note in this README if you add a new algorithm or flag.

---

## License

MIT
