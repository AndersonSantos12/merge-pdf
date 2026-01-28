
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = '/tmp/uploads'
MERGED_FOLDER = '/tmp/merged'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MERGED_FOLDER'] = MERGED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('pdfs')
        add_blank = request.form.get('add_blank') == 'on'
        output_name = request.form.get('output_name', '').strip() or 'merged.pdf'
        if not output_name.lower().endswith('.pdf'):
            output_name += '.pdf'
        output_name = secure_filename(output_name)
        if not files or files[0].filename == '':
            return 'Selecione ao menos um arquivo PDF ou DOC.', 400
        invalid = [f.filename for f in files if not allowed_file(f.filename)]
        if invalid:
            return f'Arquivo(s) não permitido(s): {", ".join(invalid)}. Apenas PDF e DOC/DOCX são aceitos.', 400
        merger = PdfMerger()
        temp_files = []
        filenames = []
        try:
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    filenames.append(filepath)
            for filepath in filenames:
                if filepath.lower().endswith('.pdf'):
                    if add_blank:
                        reader = PdfReader(filepath)
                        num_pages = len(reader.pages)
                        if num_pages % 2 == 1:
                            writer = PdfWriter()
                            for page in reader.pages:
                                writer.add_page(page)
                            last_page = reader.pages[-1]
                            width = last_page.mediabox.width
                            height = last_page.mediabox.height
                            writer.add_blank_page(width=width, height=height)
                            temp_stream = io.BytesIO()
                            writer.write(temp_stream)
                            temp_stream.seek(0)
                            merger.append(temp_stream)
                            temp_files.append(temp_stream)
                        else:
                            merger.append(filepath)
                    else:
                        merger.append(filepath)
                else:
                    # Para .doc/.docx: apenas salva, não mescla (poderia converter para PDF se desejado)
                    pass
            merged_path = os.path.join(app.config['MERGED_FOLDER'], output_name)
            merger.write(merged_path)
            merger.close()
            return send_file(merged_path, as_attachment=True, download_name=output_name)
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print('Erro ao processar arquivos:', tb)
            return f'Erro ao processar arquivos: {str(e)}', 500
        finally:
            # Limpa uploads
            for f in filenames:
                try:
                    os.remove(f)
                except Exception:
                    pass
            for t in temp_files:
                try:
                    t.close()
                except Exception:
                    pass
    return render_template('index.html')

# Não inclua bloco if __name__ == '__main__' aqui!
