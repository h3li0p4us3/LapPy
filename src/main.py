from flask import Flask, request, jsonify, send_file, render_template
import pyperclip
import os

app = Flask(__name__, template_folder='front')

os.makedirs('uploads', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send-text', methods=['POST'])
def send_text():
    data = request.form
    text = data.get('text', '')
    savetoClipboard(text)
    return jsonify({'message': 'Text sent successfully'}), 200



def savetoClipboard(text):
    try:
        pyperclip.copy(text)
        print(f"Text '{text}' saved to clipboard")
    except pyperclip.get_errno as e:
        print(f"Failed to save text to clipboard: {e}")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        try:
            filename = os.path.basename(file.filename)
            # save file in uploads/ folder
            file.save(os.path.join('uploads', filename))
            return f"File '{filename}' uploaded successfully"
        except IOError as e:
            return f"Error uploading file: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080) # if you set to 80, you will need root permission.

# defining host as 0.0.0.0 is required for running the program on all addresses.