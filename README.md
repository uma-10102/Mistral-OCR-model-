# 🏥 Handwritten Medical Prescription Structuring using Mistral OCR

# Objective
 Input: Scanned Handwritten Prescriptions
These are typically PDF or image files.
Contain unstructured data like drug names, dosages, patient info written by doctors.

Challenges: Handwritten Text is Difficult to Read
Variability in handwriting styles.
Layouts are not standardized.
Regular OCR often fails or produces noisy outputs.

Goal: Convert Unstructured Data into Structured Format
Extract key fields such as:

Patient Name
Date
Medicines
Dosage and Frequency
Doctor’s Name
Instructions


# Model Used
**Model:** `mistral-ocr-latest` via `mistralai` Python client  
**Tool Used**: Mistral's Multimodal OCR API
A powerful vision-language model that understands both images and text.

Capable of:
Reading handwritten content.
Returning markdown-structured results.
Embedding inline images if needed.

**Task:** Convert PDF prescription to image → OCR → Markdown → Structured output

# Pipeline
1. Convert first page of PDF to image
2. Upload to Mistral OCR API
3. Extract markdown + image assets
4. Save output to local directory

# Evaluation Strategy

**Why this model**
The model automates extracting structured data from handwritten medical prescriptions using a multimodal AI approach. It combines Optical Character Recognition (OCR) to convert text from images, along with Natural Language Processing (NLP) for entity recognition. Multimodal fusion integrates image features and text to enhance accuracy. The result is efficient, automated extraction of prescription details like medication, dosages, and instructions.

- **Manual validation** 
- across 10 samples
- Field-level accuracy ~85%
- f1 score - to check the accuracy level
- Future scope: Automate evaluation with labeled ground truth


# Project Structure
- `src/`: Core pipeline scripts
- `data/`: Sample input PDFs
- `outputs/`: OCR markdown + images
- `notebooks/`: Exploratory and visualization files

# Run
```bash
python src/main.py
```

# Requirements
```bash
pip install mistralai pdf2image python-dotenv
sudo apt-get install poppler-utils
```
