from flask import Flask, request, send_file
import subprocess
import tempfile
import os
import soundfile as sf

app = Flask(__name__)

@app.route('/stretch', methods=['POST'])
def stretch_audio():
    if 'file' not in request.files or 'target_duration' not in request.form:
        return {"error": "Missing required data"}, 400

    file = request.files['file']
    target_duration = float(request.form['target_duration'])

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.wav")
        output_path = os.path.join(tmpdir, "stretched.wav")

        file.save(input_path)

        # Get duration
        data, sr = sf.read(input_path)
        original_duration = len(data) / sr
        tempo_ratio = original_duration / target_duration

        try:
            subprocess.run([
                "sox", input_path, output_path, "tempo", f"{tempo_ratio:.6f}"
            ], check=True)

            return send_file(output_path, mimetype="audio/wav")
        except subprocess.CalledProcessError as e:
            return {"error": f"sox failed: {str(e)}"}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
