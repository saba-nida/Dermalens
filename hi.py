import tensorflow as tf

# Load the model
try:
    model = tf.keras.models.load_model('model.h5')
except Exception as e:
    print("Error loading model:", e)
    exit()

# Rename layers with invalid names
for layer in model.layers:
    if '/' in layer.name:
        new_name = layer.name.replace('/', '_')  # Replace `/` with `_`
        layer._name = new_name  # Rename layer

# Save the modified model
fixed_model_path = 'model'
model.save(fixed_model_path)
print(f"Model saved with updated layer names: {fixed_model_path}")
