from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
MERGED_FOLDER = 'merged'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MERGED_FOLDER'] = MERGED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ...existing code...
# Todas as rotas e funções do app.py devem ser copiadas para cá
# O objeto Flask deve ser chamado 'app' para Vercel

# ...existing code...
