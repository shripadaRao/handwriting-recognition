from flask import Flask, jsonify, request
from flask_cors import CORS  
from generate_scrabblegan_img import generator, generate_image
from predict_module import predict_handwritten_text  
from autocorrect import autocorrect_model

app = Flask(__name__)
CORS(app)  

@app.route('/generate_image/random', methods=['GET'])
def generate_random_image_route():
    result = generate_image()
    #result = {"label": word_labels[0], "image": image_data}
    return jsonify(result)

@app.route('/generate_image/<string:input_word>', methods=['GET'])
def generate_input_image_route(input_word):
    result = generate_image(input_word)
    #result = {"label": word_labels[0], "image": image_data}
    return jsonify(result)

@app.route('/predict_image', methods=['POST'])
def predict_image_route():
    try:
        data = request.get_json()
        base64_image = data["imageData"]
        contextUsage = data["contextUsage"]

        predicted_word = predict_handwritten_text(base64_image)
        # apply autocorrect
        autocorrected_word = autocorrect_model.autocorrect(predicted_word, contextUsage)
        return jsonify({"predictedWord": predicted_word, "autocorrectedWord": autocorrected_word})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
