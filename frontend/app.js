const GENERATE_RANDOM_IMAGE_API_URL =
  "http://127.0.0.1:5000/generate_image/random";
const GENERATE_INPUT_WORD_IMAGE_API_URL =
  "http://127.0.0.1:5000/generate_image/";

const PREDICT_IMAGE_API_URL = "http://127.0.0.1:5000/predict_image";

let global_base64ImageData = "";

async function generateRandomImage() {
  const generateImageApiUrl = GENERATE_RANDOM_IMAGE_API_URL;

  try {
    const response = await fetch(generateImageApiUrl);
    const data = await response.json();

    global_base64ImageData = data.image;

    const label = data.label;

    const generatedImage = document.getElementById("generatedImage");
    generatedImage.height = 200;
    generatedImage.width = label.length * 60 + 10;

    generatedImage.src = "data:image/png;base64," + data.image;

    const displayLabel = document.getElementById("generatedLabel");
    displayLabel.textContent = "Generated Label: " + label;

    // Show the 'Predict Img' button
    const predictImgBtn = document.getElementById("predictImgBtn");
    predictImgBtn.style.display = "inline";
  } catch (error) {
    console.error("Error generating image:", error);
  }
}

async function generateUserTextImage() {
  const generateImageApiUrl = GENERATE_INPUT_WORD_IMAGE_API_URL;

  const userText = prompt("Enter text for image generation:");
  if (userText) {
    try {
      const response = await fetch(generateImageApiUrl + userText);
      const data = await response.json();

      global_base64ImageData = data.image;

      const label = data.label;

      const generatedImage = document.getElementById("generatedImage");
      generatedImage.height = 200;
      generatedImage.width = label.length * 60 + 10;

      generatedImage.src = "data:image/png;base64," + data.image;

      const displayLabel = document.getElementById("generatedLabel");
      displayLabel.textContent = "Generated Label: " + label;

      // Show the 'Predict Img' button
      const predictImgBtn = document.getElementById("predictImgBtn");
      predictImgBtn.style.display = "inline";
    } catch (error) {
      console.error("Error generating image:", error);
    }
  }
}

async function predictImage() {
  const predictImageApiUrl = PREDICT_IMAGE_API_URL;

  try {
    // Make POST request to the predict image API with base64 image data
    const response = await fetch(predictImageApiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ imageData: global_base64ImageData }),
    });

    const data = await response.json();
    const { predictedWord, autocorrectedWord } = data;

    console.log("Prediction Result:", predictedWord);
    console.log("Autocorrected Word: ", autocorrectedWord);

    const displayPredictionLabel = document.getElementById("predictionLabel");
    displayPredictionLabel.textContent = "Predicted Label: " + predictedWord;

    const displayAutoCorrectedLabel =
      document.getElementById("autocorrectedLabel");
    displayAutoCorrectedLabel.textContent =
      "Autocorrected Label: " + autocorrectedWord;
  } catch (error) {
    console.error("Error predicting image:", error);
  }
}
