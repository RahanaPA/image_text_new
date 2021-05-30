import os
from flask import Flask,flash, render_template, request,redirect,url_for
import urllib.request
from werkzeug.utils import secure_filename

# import our OCR function
from ocr_core import ocr_core

app = Flask(__name__)

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/api/v2/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.secret_key = "secretkey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# function to check the file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/api/v2/')

def home():
    return render_template('index.html')


# # route and function to handle the upload page
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_page():
#     if request.method == 'POST':
#         # check if there is a file in the request
#         if 'file' not in request.files:
#             return render_template('upload.html', msg='No file selected')
#         file = request.files['file']
#         # if no file is selected
#         if file.filename == '':
#             return render_template('upload.html', msg='No file selected')

#         if file and allowed_file(file.filename):

#             # call the OCR function on it
#             extracted_text = ocr_core(file)

#             # extract the text and display it
#             return render_template('upload.html',
#                                    msg='Successfully processed',
#                                    extracted_text=extracted_text,
#                                    img_src=UPLOAD_FOLDER + file.filename)
#     elif request.method == 'GET':
#         return render_template('upload.html')

@app.route('/api/v2/', methods=['POST'])
def upload_image():
    # check if there is a file in the request
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
     # if no file is selected
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below ↷')

        # call the OCR function on it
        extracted_text = ocr_core(file)
        return render_template('index.html', filename=filename,extracted_text=extracted_text)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/api/v2/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='/api/v2/static/uploads/' + filename), code=301)






