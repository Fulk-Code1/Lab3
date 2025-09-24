from flask import Flask, request, jsonify
from pydub import AudioSegment
import os

app = Flask(__name__)
audio = None
output_path = ""

@app.route('/process/load', methods=['POST'])
def load_audio_route():
    global audio, output_path
    file_path = request.json.get('file_path')
    try:
        audio = AudioSegment.from_file(file_path)
        output_path = os.path.splitext(file_path)[0] + "_edited.wav"
        return jsonify({"status": f"Сохранен: {os.path.basename(file_path)}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/process/trim', methods=['POST'])
def trim_audio_route():
    global audio
    if audio is None:
        return jsonify({"error": "Не был загружен аудиофайл"}), 400
    try:
        audio = audio[5000:]
        return jsonify({"status": "Аудиофайл обрезан (обрезал первые 5 секунд)"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/process/normalize', methods=['POST'])
def normalize_audio_route():
    global audio
    if audio is None:
        return jsonify({"error": "Не был загружен аудиофайл"}), 400
    try:
        audio = audio.normalize()
        return jsonify({"status": "Аудиофайл нормализован"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/process/echo', methods=['POST'])
def add_echo_route():
    global audio
    if audio is None:
        return jsonify({"error": "Не был загружен аудиофайл"}), 400
    try:
        echo = audio - 10
        echo = echo.fade_in(1000).fade_out(1000)
        delayed = AudioSegment.silent(duration=400) + echo
        audio = audio.overlay(delayed)
        return jsonify({"status": "Добавлено Эхо"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/process/save', methods=['POST'])
def save_audio_route():
    global audio, output_path
    if audio is None:
        return jsonify({"error": "Не был загружен аудиофайл"}), 400
    try:
        audio.export(output_path, format="wav")
        return jsonify({"status": f"Аудиофайл сохранен по пути {output_path}", "output_path": output_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(port=5001, debug=True)