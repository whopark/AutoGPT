# Chest X-Ray Analysis Web Application

This application allows users to upload a chest X-ray image (PNG, JPG, JPEG, or DICOM) and receive a mock analysis report. The backend is built with Flask, and it currently simulates a call to a hypothetical LLaVA-Med model API.

## Features

- Image upload for chest X-rays.
- Frontend display of the uploaded image.
- Mock analysis results displayed on the web page.

## Project Structure

- `app.py`: The Flask backend server.
- `templates/index.html`: The main HTML page for the frontend.
- `uploads/`: A directory for storing uploaded files (though currently, files are not saved permanently in the mock setup).
- `requirements.txt`: Python dependencies.
- `README.md`: This file.

## Setup and Installation

1.  **Clone the repository (if you haven't already).**

2.  **Navigate to the application directory:**
    ```bash
    cd chest_xray_app
    ```

3.  **Create a Python virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
    *Note: During development, there were issues creating a virtual environment in the sandbox. If you face similar issues, you might need to install packages globally or use a different Python environment management tool.*

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Ensure you are in the `chest_xray_app` directory and your virtual environment is activated (if used).**

2.  **Run the Flask application:**
    ```bash
    python app.py
    ```

3.  **Open your web browser and navigate to:**
    [http://127.0.0.1:5001/](http://127.0.0.1:5001/) or [http://localhost:5001/](http://localhost:5001/)

## API Interaction (Mocked)

The application is designed to interact with an API for the LLaVA-Med model. Currently, this interaction is mocked within `app.py`.

-   **Hypothetical API Endpoint:** `https://api.hypothetical-llavamed.com/v1/analyze_xray`
-   **HTTP Method:** `POST`
-   **Request Format:** `multipart/form-data` with an `image` file part.
-   **Authentication:** If a real API were used, an `api_key` might be required. This would typically be configured via an environment variable (e.g., `LLAVAMED_API_KEY`) and passed in the request headers or body. The current mock does not implement authentication.

### Example Mock Success Response (`200 OK`):
```json
{
  "report_id": "mock_report_12345",
  "model_version": "llava-med-v1.5-mistral-7b-hypothetical-mock",
  "analysis": {
    "findings": [
      {"observation": "Cardiomegaly (Mocked)", "confidence": 0.90, "details": "The cardiac silhouette appears enlarged based on mock analysis."},
      {"observation": "Pulmonary Opacity (Mocked)", "confidence": 0.75, "location": "Right lower lobe (Mocked)", "details": "Patchy opacity noted (mocked)."}
    ],
    "impression": "Mock analysis suggests cardiomegaly and a possible RLL opacity. Clinical correlation always recommended.",
    "raw_text_output": "Mock raw output: Enlarged cardiac silhouette. RLL opacity. No pneumothorax."
  },
  "processing_time_ms": 250
}
```

### Example Error Response (`400 Bad Request`):
```json
{
  "error_code": "INVALID_FILE_TYPE",
  "message": "File type not allowed. Allowed types: png, jpg, jpeg, dicom"
}
```

## Future Development

-   Integrate with a real LLaVA-Med API endpoint.
-   Implement actual API key handling.
-   Enhance UI/UX, including more detailed display of analysis results.
-   Add more robust error handling and logging.
-   Develop unit and integration tests.
-   Consider saving uploaded files securely if required by the workflow.
```
