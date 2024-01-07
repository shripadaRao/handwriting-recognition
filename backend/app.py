from flask import Flask, jsonify, request
from flask_cors import CORS  
from generate_scrabblegan_img import generator, generate_image
from predict_module import predict_handwritten_text  

app = Flask(__name__)
CORS(app)  

@app.route('/generate_image', methods=['GET'])
def generate_image_route():
    result = generate_image()
    return jsonify(result)

@app.route('/predict_image', methods=['POST'])
def predict_image_route():
    try:
        data = request.get_json()
        base64_image = data["imageData"]

        result = predict_handwritten_text(base64_image)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
