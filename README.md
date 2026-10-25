# DermaLens – Intelligent Skin Disease Identification and Care Guidance System

DermaLens is an AI-powered web application developed to support the identification of potential skin diseases and improve skin health awareness. The project uses deep learning and image processing techniques to analyze uploaded skin images and predict possible skin conditions, making preliminary skin health information more accessible to users.

The system employs a Convolutional Neural Network (CNN) based on the DenseNet architecture, trained using the DermNet dataset containing approximately 19,600 images across 23 skin disease categories. To address class imbalance in the dataset, oversampling and undersampling techniques were applied during preprocessing. The dataset was divided into training, validation, and testing sets in an 80:10:10 ratio. The model was trained for 48 epochs and achieved approximately 90.5% accuracy.

DermaLens provides a user-friendly interface where users can upload images of affected skin areas for analysis. Based on the model's predictions, the platform offers relevant educational resources, including articles and videos, to help users understand potential skin conditions. It also incorporates location-based services to recommend nearby dermatologists, encouraging users to seek professional medical advice when necessary. Additionally, the platform supports user feedback to help improve its functionality and overall user experience.

**Key Features:**
- AI-based classification of 23 skin disease categories.
- Skin image analysis using CNN and DenseNet architecture.
- Image preprocessing and dataset balancing techniques.
- Educational articles and videos related to predicted conditions.
- Location-based recommendations for nearby dermatologists.
- User feedback support for continuous improvement.

**Technologies Used:** Python, Convolutional Neural Networks (CNN), DenseNet, TensorFlow, Keras, deep learning, and image processing.

This project demonstrates the potential of artificial intelligence in healthcare by combining automated image classification with accessible educational resources and dermatologist recommendations. The goal is to promote awareness, support early recognition of possible skin conditions, and help users make informed decisions about seeking medical care.

**Research Publication:** The project was published as *Intelligent Skin Disease Identification and Care Guidance System* in the International Journal of Progressive Research in Engineering Management and Science (IJPREMS), Volume 05, Issue 01, January 2025, pages 1080–1085. The authors are Ankitha R, Saba Nida, Chandana S, Vaishnavi Pai N, and Sahana P. Shankar.

**Disclaimer:** DermaLens is an educational and research project. Its predictions are not a substitute for professional medical diagnosis or treatment.
