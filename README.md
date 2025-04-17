%%{init: {'theme': 'base', 'themeVariables': { 'background': '#ffffff' }}}%%
flowchart TD
    A[Dataset Loading] --> B[Data Preprocessing]
    B --> C[Multi-label Encoding]
    C --> D[Dataset Splitting]
    D --> E[TF Dataset Creation]
    
    E --> F[Image Processing]
    F --> G[Model Architecture]
    
    G --> I[Transfer Learning]
    I --> J[ResNet50 Base]
    I --> K[Custom Top Layers]
    
    J --> L[Phase 1: Feature Extraction]
    K --> L
    
    L --> M[Phase 2: Fine-tuning]
    
    M --> R[Model Evaluation]
    R --> S[Performance Metrics]
    R --> U[Visualization]
where do i run this code
