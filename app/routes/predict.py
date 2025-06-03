from flask import Blueprint, request, jsonify
from app.services.forecast_service import predict_prices

predict_bp = Blueprint("predict", __name__, url_prefix="/api")

@predict_bp.route("/predict", methods=["POST"])
def predict():
    """
    Faz previsão dos preços futuros com LSTM
    ---
    parameters:
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
    responses:
      200:
        description: Previsão realizada com sucesso
    """
    input_data = request.get_json()
    predictions = predict_prices(input_data["data"])
    return jsonify({"prediction": predictions})
