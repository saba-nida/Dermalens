from flask import Flask, render_template, request, redirect,flash
from werkzeug.utils import secure_filename
import os
import numpy as np
import tensorflow as tf
from PIL import Image
import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Initialize Flask app
app = Flask(__name__)

app.secret_key = 'Ankitha@123'

# Set upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load trained model
MODEL_PATH = 'model/model.h5'
model = tf.keras.models.load_model(MODEL_PATH)

# Class names for predictions
CLASS_NAMES = [
    "Acne and Rosacea Photos", "Actinic Keratosis and Malignant Lesions",
    "Atopic Dermatitis", "Bullous Diseases", "Bacterial Infections",
    "Eczema", "Exanthems and Drug Eruptions", "Hair Loss and Disorders",
    "Herpes and STDs", "Light Pigmentation Disorders", "Lupus and Connective Diseases",
    "Melanoma and Moles", "Nail Diseases", "Contact Dermatitis", "Psoriasis",
    "Scabies and Infestations", "Benign Tumors", "Systemic Diseases",
    "Fungal Infections", "Urticaria", "Vascular Tumors", "Vasculitis",
    "Viral Infections"
]

# Severity mapping
# Severity factors for each disease
SEVERITY_MAPPING = {
    "Acne and Rosacea Photos": "Severity depends on lesion count and inflammation.",
    "Actinic Keratosis and Malignant Lesions": "Highly severe if untreated, risk of malignancy.",
    "Atopic Dermatitis": "Mild to severe depending on itchiness and body area affected.",
    "Bullous Diseases": "Severe if widespread or blistering affects mucous membranes.",
    "Bacterial Infections": "Severity depends on systemic spread or localized nature.",
    "Eczema": "Mild to moderate based on the extent of itch and scaling.",
    "Exanthems and Drug Eruptions": "Can range from mild rashes to severe reactions.",
    "Hair Loss and Disorders": "Mild unless associated with systemic conditions.",
    "Herpes and STDs": "Severity varies with recurrence and immune status.",
    "Light Pigmentation Disorders": "Mild and mostly cosmetic concerns.",
    "Lupus and Connective Diseases": "Severe, can involve multiple organs.",
    "Melanoma and Moles": "Severe, especially if asymmetry or size >6mm.",
    "Nail Diseases": "Mild but can indicate systemic diseases.",
    "Contact Dermatitis": "Mild unless chronic or involving large areas.",
    "Psoriasis": "Moderate to severe depending on body surface area.",
    "Scabies and Infestations": "Mild unless secondary infections occur.",
    "Benign Tumors": "Mild but may require monitoring.",
    "Systemic Diseases": "Highly severe, often life-threatening.",
    "Fungal Infections": "Mild to moderate depending on depth and site.",
    "Urticaria": "Moderate, severe if associated with angioedema.",
    "Vascular Tumors": "Moderate to severe depending on size and complications.",
    "Vasculitis": "Severe, can cause organ damage.",
    "Viral Infections": "Mild to moderate unless systemic involvement occurs."
}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def prepare_image(image_path):
    """Preprocess the image for model prediction."""
    img = Image.open(image_path).resize((224, 224))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

def get_real_resources(disease_name):
    """Fetch real articles and videos for the disease."""
    # YouTube Data API setup
    YOUTUBE_API_KEY = "AIzaSyD26D3_-9OXx3BdCRPVdDA4oxQtY6E9ZuE"
    youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={disease_name}&type=video&key={YOUTUBE_API_KEY}"
    youtube_response = requests.get(youtube_url)
    youtube_videos = youtube_response.json().get('items', [])
    videos = [
        {"title": video['snippet']['title'], "url": f"https://www.youtube.com/watch?v={video['id']['videoId']}"}
        for video in youtube_videos[:5]
    ]

    # Google Custom Search API setup
    GOOGLE_API_KEY = "AIzaSyD26D3_-9OXx3BdCRPVdDA4oxQtY6E9ZuE"
    SEARCH_ENGINE_ID = "d2d85d260d4f64b9c"
    search_url = f"https://www.googleapis.com/customsearch/v1?q={disease_name}&cx={SEARCH_ENGINE_ID}&key={GOOGLE_API_KEY}"
    google_response = requests.get(search_url)
    search_results = google_response.json().get('items', [])
    articles = [
        {"title": result['title'], "url": result['link']}
        for result in search_results[:5]
    ]

    return articles, videos

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        filename = secure_filename(file.filename)
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image = prepare_image(filepath)
            predictions = model.predict(image)
            predicted_class = CLASS_NAMES[np.argmax(predictions)]
            confidence = np.max(predictions) * 100
            severity = SEVERITY_MAPPING.get(predicted_class, "Unknown severity level.")
            articles, videos = get_real_resources(predicted_class)

            if confidence <= 25:
                error_message = "The image uploaded does not appear to be related to skin health. Please upload a valid skin image."
                flash(f"Error processing image: {error_message}","error")
                return redirect(request.url)
            
            elif confidence <=70:
                success_message = "You are perfectly all right."
                flash(f"There is no disease detected. : {success_message}","success")
                return redirect(request.url)

            return render_template(
                'result.html',
                class_name=predicted_class,
                confidence=confidence,
                image_url=f"/{UPLOAD_FOLDER}/{filename}",
                severity=severity,
                articles=articles,
                videos=videos
            )
        else:
            flash("Invalid file type. Please upload an image.", "error")
            return redirect(request.url)

    return render_template('index.html')

@app.route('/dermatologists', methods=['GET'])
def dermatologists():
    # Static map with redirect
    return render_template('dermatologists.html',
                           map_src=f"https://maps.googleapis.com/maps/api/staticmap?center=Bangalore,India&zoom=12&size=800x500&maptype=roadmap&markers=color:red%7Clabel:B%7CBangalore,India&key=AIzaSyDoagGTD2QgJ47lMltr4Da3bOcSzPshdBY",
                           redirect_url="https://www.google.com/maps/search/dermatologists+near+me")

@app.route('/find_dermatologists', methods=['GET'])
def find_dermatologists():
    location = request.args.get('location')
    if not location:
        return jsonify({"error": "Location not provided"}), 400

    # Geocode the location to get lat and lng
    geocode_url = f"https://maps.gomaps.pro/maps/api/geocode/json?address={location}&key=AIzaSyDoagGTD2QgJ47lMltr4Da3bOcSzPshdBY"
    geocode_response = requests.get(geocode_url)
    geocode_data = geocode_response.json()

    if geocode_data['status'] != 'OK':
        return jsonify({"error": "Geocoding failed"}), 400

    lat = geocode_data['results'][0]['geometry']['location']['lat']
    lng = geocode_data['results'][0]['geometry']['location']['lng']

    # Now search for dermatologists nearby using Google Places API
    places_url = f"https://maps.gomaps.pro/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=doctor&keyword=dermatologist&key=AIzaSyDoagGTD2QgJ47lMltr4Da3bOcSzPshdBY"
    places_response = requests.get(places_url)
    places_data = places_response.json()

    places = [
        {
            "name": place.get("name"),
            "vicinity": place.get("vicinity"),
            "google_maps_url": f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}"
        }
        for place in places_data.get('results', []) if place.get("place_id")
    ]

    return render_template('find_dermatologists.html', places=places)

@app.route('/feedback', methods=['GET'])
def feedback():
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)
