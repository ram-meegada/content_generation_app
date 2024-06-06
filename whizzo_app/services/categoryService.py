from ssl import SSL_ERROR_EOF
from typing import final
from django.http import JsonResponse
from whizzo_app.models.assignmentModel import AssignmentModel
from whizzo_app.models.categoryModel import CategoryModel
from whizzo_project import settings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import textwrap
import urllib.request as urlopener
from PyPDF2 import PdfReader
from io import BytesIO
import json
from whizzo_app.models import FaqModel,CmsModel, UserModel, FileSumarizationModel, NoteModel
from whizzo_app.utils import messages
from whizzo_app.serializers import categorySerializer, adminSerializer
from deep_translator import GoogleTranslator
import aspose.words as aw
from pdf2docx import Converter
import random
from whizzo_app.utils.saveImage import save_file_conversion
from whizzo_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer
import os
import tabula
import re
import json
import xlsxwriter
import pandas as pd
from reportlab.lib.pagesizes import letter,A3
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Image
from reportlab.lib import colors
from pdf2image import convert_from_path
from django.core.files.storage import FileSystemStorage
import speech_recognition as sr
from pydub import AudioSegment
from whizzo_app.utils.saveImage import save_image
from whizzo_app.utils import sendMail
from whizzo_app.services.uploadMediaService import UploadMediaService
from whizzo_app.utils.customPagination import CustomPagination
from docx import Document
from docx2pdf import convert
import fitz
from PIL import Image
import tempfile
from pptx.util import Inches
from pptx import Presentation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from rest_framework import status
import pdfkit
import pypandoc
from whizzo_app.utils.saveImage import saveFile
from whizzo_app.services.uploadMediaService import UploadMediaService
from whizzo_app.utils.sendMail import send_pdf_file_to_mail
from threading import Thread

upload_media_obj = UploadMediaService()

load_dotenv()
google_api_key = settings.GOOGLE_API_KEY



def to_markdown(text):
  text = text.replace('*', '')
  intent_text=(textwrap.indent(text, '', predicate=lambda _: True))
  return intent_text

# def to_markdown(text):
#     # Remove Markdown headers (e.g., # Header)
#     text = re.sub(r'^\s*#+\s+', '', text, flags=re.MULTILINE)
#     # Remove emphasis (e.g., *italic* or **bold**)
#     text = re.sub(r'(\*|_){1,2}(.*?)\1{1,2}', r'\2', text)
#     # Remove inline code (e.g., `code`)
#     text = re.sub(r'`(.*?)`', r'\1', text)
#     # Remove strikethrough (e.g., ~~text~~)
#     text = re.sub(r'~~(.*?)~~', r'\1', text)
#     # Remove links (e.g., [text](url))
#     text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
#     # Remove images (e.g., ![alt text](url))
#     text = re.sub(r'!\[(.*?)\]\(.*?\)', r'\1', text)
#     # Remove remaining special characters used in Markdown
#     text = re.sub(r'[*_~`]', '', text)
    
#     # Normalize indentation
#     text = textwrap.dedent(text)

#     # Split text into lines and clean up
#     lines = [line.strip() for line in text.splitlines() if line.strip()]

#     # Join lines to form a single JSON string
#     json_string = " ".join(lines)
    
#     # Attempt to parse as JSON
#     try:
#         json_list = json.loads(json_string)
#     except json.JSONDecodeError as e:
#         raise ValueError(f"Failed to decode JSON: {e}")
    
#     return json_list

# def to_markdown(text):
#     # Remove Markdown headers (e.g., # Header)
#     text = re.sub(r'^\s*#+\s+', '', text, flags=re.MULTILINE)
#     # Remove emphasis (e.g., *italic* or **bold**)
#     text = re.sub(r'(\*|_){1,2}(.*?)\1{1,2}', r'\2', text)
#     # Remove inline code (e.g., `code`)
#     text = re.sub(r'`(.*?)`', r'\1', text)
#     # Remove strikethrough (e.g., ~~text~~)
#     text = re.sub(r'~~(.*?)~~', r'\1', text)
#     # Remove links (e.g., [text](url))
#     text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
#     # Remove images (e.g., ![alt text](url))
#     text = re.sub(r'!\[(.*?)\]\(.*?\)', r'\1', text)
#     # Remove remaining special characters used in Markdown
#     text = re.sub(r'[*_~`]', '', text)
    
#     # Normalize indentation
#     text = textwrap.dedent(text)

#     # Split text into lines and clean up
#     lines = [line.strip() for line in text.splitlines() if line.strip()]
    
#     # Convert lines to JSON list
#     try:
#         json_list = json.loads("[" + ",".join(lines) + "]")
#     except json.JSONDecodeError:
#         json_list = lines  # Fallback: return lines as plain list if JSON decoding fails
    
#     return json_list


def assignment_to_markdown(text):
    # Remove Markdown headers (e.g., # Header)
    text = re.sub(r'^\s*#+\s+', '', text, flags=re.MULTILINE)
    # Remove emphasis (e.g., *italic* or **bold**)
    text = re.sub(r'(\*|_){1,2}(.*?)\1{1,2}', r'\2', text)
    # Remove inline code (e.g., `code`)
    text = re.sub(r'`(.*?)`', r'\1', text)
    # Remove strikethrough (e.g., ~~text~~)
    text = re.sub(r'~~(.*?)~~', r'\1', text)
    # Remove links (e.g., [text](url))
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    # Remove images (e.g., ![alt text](url))
    text = re.sub(r'!\[(.*?)\]\(.*?\)', r'\1', text)
    # Remove remaining special characters used in Markdown
    text = re.sub(r'[*_~`]', '', text)
    
    # Normalize indentation
    text = textwrap.dedent(text)

    # Split text into lines and clean up
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    # Remove commas from each line
    lines = [line.replace(',', '') for line in lines]
    
    # Convert lines to JSON list
    try:
        json_list = json.loads("[" + ",".join(lines) + "]")
    except json.JSONDecodeError:
        json_list = lines  # Fallback: return lines as plain list if JSON decoding fails
    
    return json_list

def image_processing(image_link , query):
    '''processing the image and generate the mcq with options and answer 
       image_link is the s3 bucket link of image and query is string 
       which we use to generate the mcq of flashcards'''
    llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")
        # example
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": query,
            },
            {"type": "image_url", "image_url": str(image_link)},
        ]
    )
    response = llm.invoke([message])
    result_qu = to_markdown(response.content)
    print(result_qu,"asdfkhaskdfjhalskfjdh")
    return result_qu

def pdf_processing(pdf_file , query):
    '''processing the pdf and generate the mcq and flash cards based on the user requirement 
       pdf_link is the s3 bucket link where we store the pdf file 
       query is based on the user selection if he select mcq then query based on mcq else based on flash card'''

    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    def extract_text(pdf_file):
        '''extract all the text from the pdf '''
        pdf_text = ''
        # Wrap the file content in BytesIO to treat it as a bytes-like object
        url_obj = urlopener.urlopen(pdf_file)

        # with open(pdf_file, 'r') as f:
        pdf_stream = BytesIO(url_obj.read())
        pdf_reader = PdfReader(pdf_stream)
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        return pdf_text
            

    if pdf_file:
        try:
            text_data = extract_text(pdf_file)
            message = HumanMessage(
                content=[
                    {"type": "text", 
                    "text": query},
                    {"type": "text", "text":text_data}
                ]
            )

            # Process the message
            response = llm.invoke([message])
            result = to_markdown(response.content)
            print(result,"hellasjdhfkajhsdflkjahslkdfjhalskjfhdalksjhflakjs")
            return result
        except Exception as e:
            return (str(e))
    else:
        return ("No PDF file provided")

class CategoryService:
    def generate_testing_category_result(self, request):
        try:
            check_incomplete_test = CategoryModel.objects.filter(user_id=request.user.id, 
                                                           category=1, #static because this api is for testing category
                                                           sub_category=request.data["sub_category"],
                                                           is_active=True
                                                           )
            if check_incomplete_test.exists():
                return {"data": check_incomplete_test.first().result, "message": messages.INCOMPLETE_PREVIOUS_TEST, "status": 200}

            file_links = request.data["file_links"]
            sub_category = request.data["sub_category"]
            final_response = []
            for file in file_links:
                if file.endswith((".jpeg",".png",".jpg",".webp")):
                    if sub_category == 1:
                        query = f"generate {settings.NUMBER_OF_QUESTIONS} mcqs with options and answers for this image and make in python json list format."
                        result = image_processing(file, query)
                        json_result = self.jsonify_response(result)
                        final_response += json_result
                    elif  sub_category == 2:
                        query = f"generate {settings.NUMBER_OF_QUESTIONS} flashcards for this image and make in python json list format. make a name is frontside and backside not any other name for this and give me only one answer for this."
                        result = image_processing(file, query)
                        json_result = self.jsonify_response(result)
                        final_response += json_result

            create_category = CategoryModel.objects.create(user_id=request.user.id, 
                                                           category=1, #static because this api is for testing category
                                                           sub_category=request.data["sub_category"],
                                                           result=final_response
                                                           )

            return {"data": final_response, "message": "Result generated successfully", "status": 200}
        except Exception as error:
            return {"data": str(error), "message": "Something went wrong", "status": 400}
    
    def generate_testing_category_result_pdf(self , request):
            file_links = request.data["file_links"]
            sub_category = request.data["sub_category"]
            final_response = []
            for file in file_links:         
                if file.endswith(".pdf"):
                    if sub_category == 1:
                        query = f"generate {settings.NUMBER_OF_QUESTIONS} mcqs with options and answers for this image and make in python json list format."
                        result = pdf_processing(file , query)
                        json_result = self.jsonify_response(result)
                        final_response.append(json_result)
                        print(result, '-----result----')
                    elif  sub_category == 2:
                        query = f"generate {settings.NUMBER_OF_QUESTIONS} flashcards for this image and make in python json list format. make a name is frontside and backside not any other name for this and give me only one answer for this."
                        result = pdf_processing(file , query)
                        json_result = self.jsonify_response(result)
                        final_response.append(json_result)
            create_category = CategoryModel.objects.create(user_id=request.user.id, 
                                                           category=1, #static because this api is for testing category
                                                           sub_category=request.data["sub_category"],
                                                           result=final_response
                                                           )            
            return {"data": final_response, "message": "Result generated successfully", "status": 200}

    def jsonify_response(self, result):
        for i, j in enumerate(result):
            if j == "[":
                break
        for end in range(len(result)-1, -1, -1):
            if result[end] == "]":
                break
        final_result = json.loads(result[i:end+1])
        return final_result

    def submit_test_and_update_result(self, request):
        get_test_objects = CategoryModel.objects.filter(user_id=request.user.id,
                                                            category=1, #static because this api is for testing category
                                                            sub_category=request.data["sub_category"],
                                                            is_active=True
                                                           )
        get_test_obj = get_test_objects.first()
        get_test_obj.correct_answers = request.data["correct_answers"]
        get_test_obj.is_active = False
        get_test_obj.save()
        return {"data": "", "message": messages.TEST_SUBMITTED, "status": 200}
    
    def previous_tests_listing(self, request):
        previous_tests = CategoryModel.objects.filter(user_id=request.user.id,
                                                      is_active=False,
                                                      category=1
                                                      )
        serializer = categorySerializer.GetPreviousTestSerializer(previous_tests, many=True)
        return {"data": serializer.data, "message": messages.TESTING_CATEGORY_PAST_TESTS, "status": 200}


# filesumarization

    def generate_file_summary(self, request):
        file_link = request.FILES.get("file_link")
        llm = ChatGoogleGenerativeAI(model="gemini-pro")
        try:
            text_data = self.extract_text(file_link)
            message = HumanMessage(
                content=[
                    {"type": "text",
                    "text": f"generate a summary of this pdf file and the length of the summary should be strictly atleast 2000 words and give me only text no * and extra symbols"},
                    {"type": "text", "text":text_data}
                ]
            )
            response = llm.invoke([message])
            result = to_markdown(response.content)
            save_file_summary_record = FileSumarizationModel.objects.create(
                                                    user_id=request.user.id,
                                                    sub_category=5,
                                                    result=result
            )
            return {"data": result, "message": messages.SUMMARY_GENERATED, "status": 200}
        except Exception as e:
            return {"error": str(e), "message": messages.WENT_WRONG, "status": 400}
    def extract_text(self, file_link):
        pdf_text = ""
        with file_link.open() as f:
            pdf_stream = BytesIO(f.read())
            pdf_reader = PdfReader(pdf_stream)
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
        return pdf_text
    
    def file_summary_history(self, request):
        summary_history_objects = FileSumarizationModel.objects.filter(
            user_id=request.user.id,
            sub_category=5
        )
        serializer = categorySerializer.GetFileSumarizationSerializer(summary_history_objects, many=True)
        return {"data": serializer.data, "message": messages.TESTING_CATEGORY_PAST_TESTS, "status": 200}
    
    def get_file_summary_by_id(self, request, file_id):
        try:
            get_summary_obj = FileSumarizationModel.objects.get(id=file_id)
        except FileSumarizationModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer = categorySerializer.GetFileSummarizationIdSerializer(get_summary_obj)
        return {"data": serializer.data, "message": messages.SUMMARY_FETCHED, "status": 200}
    

    ############# FILE CONVERSIONS ###############

    # def word_to_pdf(self , request):
    #     """
    #         We have to provide the link of the doc file and after
    #         that we can convert the file into pdf file.
    #     """
    #     word_file = request.FILES.get("pdf_file")
    #     file_name = word_file.name

    #     doc = aw.Document(word_file)
    #     doc.save(f"{file_name}.pdf")
    #     return {"data": "", "message": "conversion is done", "status": 200}
    
    def pdf_to_word(self , request):
        pdf_file = request.FILES.get("pdf_file")
        f_name = pdf_file.name
        file_name = "".join((f_name).split(" "))
        file_name = f"{file_name}_{random.randint(10000, 99999)}"
        output_word_file = f"{file_name}.docx"
        input_name = f"{file_name}_{random.randint(10000, 99999)}"
        input_pdf_file = f"{input_name}.pdf"
        delete_files = [input_pdf_file, output_word_file]
        
        fs = FileSystemStorage()
        fs.save(input_pdf_file, pdf_file)
        cv = Converter(input_pdf_file)
        # cv = Converter(BytesIO(pdf_content))
        cv.convert(output_word_file, start=0, end=None)
        cv.close()
        SAVED_FILE_RESPONSE = save_file_conversion(output_word_file, output_word_file, "word")
        data = {
                    "media_url": SAVED_FILE_RESPONSE[0],
                    "media_type": "word",
                    "media_name": SAVED_FILE_RESPONSE[1]
                }
        serializer = CreateUpdateUploadMediaSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
        for file in delete_files:
            if os.path.exists(file):
                os.remove(file)
        return {"data": data, "message": messages.PDF_TO_WORD, "status": 200}

    def convert_pdf_to_excel(self , request):
        excel_file = request.FILES.get("pdf_file")
        file_name = f"output_{random.randint(10000, 99999)}"

        pdf_content = excel_file.read()

        # Convert the PDF content to a byte stream
        pdf_byte_stream = BytesIO(pdf_content)

        # excel_path = str(excel_file)
        output_path = f"{file_name}.xlsx"

        self.pdf_to_excel(excel_file, output_path)
        SAVED_FILE_RESPONSE = save_file_conversion(output_path, output_path, "excel")
        data = {
                    "media_url": SAVED_FILE_RESPONSE[0],
                    "media_type": "excel",
                    "media_name": SAVED_FILE_RESPONSE[1]
                }
        serializer = CreateUpdateUploadMediaSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
        if os.path.exists(output_path):
            os.remove(output_path)
        return {"data": data, "message": messages.PDF_TO_EXCEL, "status": 200}
    
    def word_to_pdf(self, request):
        word_file = request.FILES.get("word_file")
        if not word_file:
            return {"message": "No Word file provided", "status": 400}

        # Generate unique file names
        file_name = "".join((word_file.name).split(" "))
        base_name = f"output_{random.randint(10000, 99999)}"
        temp_dir = tempfile.gettempdir()
        input_word_file = os.path.join(temp_dir, f"{base_name}.docx")
        # output_pdf_file = os.path.join(temp_dir, f"{base_name}.pdf")
        output_pdf_file = os.path.join( f"{base_name}.pdf")

        # Save the uploaded Word file temporarily
        with open(input_word_file, 'wb') as f:
            for chunk in word_file.chunks():
                f.write(chunk)

        print(f"Input Word file path: {input_word_file}")

        # # Convert Word to PDF
        # doc = aw.Document(input_word_file)
        # doc.save(output_pdf_file)
        # print(f"Output PDF file path: {output_pdf_file}")


        # Read the Word document and extract its contents
        document = Document(input_word_file)
        content = []
        for paragraph in document.paragraphs:
            content.append(paragraph.text)

        # Generate PDF using ReportLab
        doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
        styles = getSampleStyleSheet()
        paragraphs = [Paragraph(text, styles["Normal"]) for text in content]
        doc.build(paragraphs)
        # Convert Word to PDF
        convert(input_word_file, output_pdf_file)
        # Handle the converted PDF
        SAVED_FILE_RESPONSE = save_file_conversion(output_pdf_file, output_pdf_file, "application/pdf")
        data = {
            "media_url": SAVED_FILE_RESPONSE[0],
            "media_type": "pdf",
            "media_name": SAVED_FILE_RESPONSE[1]
        }
        serializer = CreateUpdateUploadMediaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        save_file_in_model = CategoryModel.objects.create(
                                                            user_id=request.user.id,
                                                            media_id=serializer.data["id"],
                                                            category=6,
                                                            sub_category=11
                                                        )
        # Save a copy of the output PDF file to a designated directory on your system
        # designated_dir = os.path.join(settings.BASE_DIR, 'saved_pdf_files')
        # os.makedirs(designated_dir, exist_ok=True)
        # final_pdf_path = os.path.join(designated_dir, f"{base_name}.pdf")
        
        # Copy the PDF file to the designated directory
        # with open(final_pdf_path, 'wb') as final_pdf_file:
        #     with open(output_pdf_file, 'rb') as temp_pdf_file:
        #         final_pdf_file.write(temp_pdf_file.read())

        # Clean up temporary files
        if os.path.exists(input_word_file):
            os.remove(input_word_file)
        if os.path.exists(output_pdf_file):
            os.remove(output_pdf_file)

        return {
            "data": data,
            "message": "done",
            "status": 200
        }
    
    def pdf_to_excel(self, pdf_path, excel_path):
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

        # Create an Excel writer object
        with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
            # Iterate through each table and write it to a separate sheet
            for i, table in enumerate(tables):
                # Write the table to the Excel sheet
                table.to_excel(writer, sheet_name=f"Sheet {i+1}", index=False)

                # Access the worksheet object
                worksheet = writer.sheets[f"Sheet {i+1}"]

                # Iterate through each column and set its width
                for idx, col in enumerate(table.columns):
                    series = table[col]
                    max_len = max((
                        series.astype(str).map(len).max(),
                        len(str(series.name))
                    )) + 1
                    worksheet.set_column(idx, idx, max_len)

    def excel_to_pdf(self , request):
        excel_file  = request.FILES.get("excel_file")
        file_name = excel_file.name

        # excel_path = str(excel_file)
        file_save_path= f"{file_name}_{random.randint(10000, 99999)}.pdf"

        self.Excel_To_Pdf(excel_file, file_save_path)
        SAVED_FILE_RESPONSE = save_file_conversion(file_save_path, file_save_path, "application/pdf")
        data = {
                    "media_url": SAVED_FILE_RESPONSE[0],
                    "media_type": "excel",
                    "media_name": SAVED_FILE_RESPONSE[1]
                }
        serializer = CreateUpdateUploadMediaSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
        if os.path.exists(file_save_path):
            os.remove(file_save_path)
        return {"data": serializer.data, "message": messages.CONVERT_SUCCESS, "status": 200}                
    
    def Excel_To_Pdf(self, excel_file, pdf_file):
        # Read Excel file into pandas DataFrame
        df = pd.read_excel(excel_file)
        # Convert DataFrame to list of lists (2D array)
        data = [df.columns.tolist()] + df.values.tolist()
        # Create PDF
        doc = SimpleDocTemplate(pdf_file, pagesize=A3)
        table = Table(data)
        # Style the table
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

        table.setStyle(style)
        # Add table to PDF
        doc.build([table])

    def convert_pdf_to_image(self, request):
        pdf_file = request.FILES.get("pdf_file")
        file_name = "".join(str(pdf_file).split(" "))
        # file_save_path= f"image_{random.randint(10000, 99999)}.jpg"
        file_name = f"{random.randint(10000, 99999)}_{file_name}"
        input_pdf_file = f"{random.randint(10000, 99999)}_{file_name}"
        # input_pdf_file = f"{input_name}"
        
        fs = FileSystemStorage()
        fs.save(input_pdf_file, pdf_file)
        image_path_prefix = file_name.replace("pdf", "jpg")
        saved_files = self.pdf_to_image(input_pdf_file, image_path_prefix)
        if os.path.exists(input_pdf_file):
            os.remove(input_pdf_file)
        return {"data": saved_files, "message": messages.CONVERT_SUCCESS, "status": 200}

    def pdf_to_image(self, pdf_path, image_path_prefix):
        # Convert PDF to a list of PIL Image objects
        images = convert_from_path(pdf_path)
        images_data = []
        # Save each page as an image
        for i, image in enumerate(images):
            image_path = f"{random.randint(10000, 99999)}_{image_path_prefix}"  # Change the extension as needed
            image.save(image_path, 'JPEG')  # Change the format as needed
            SAVED_FILE_RESPONSE = save_file_conversion(image_path, image_path, "jpg")
            data = {
                        "media_url": SAVED_FILE_RESPONSE[0],
                        "media_type": "image",
                        "media_name": SAVED_FILE_RESPONSE[1]
                    }
            serializer = CreateUpdateUploadMediaSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                images_data.append(serializer.data)
            if os.path.exists(image_path):
                os.remove(image_path)
        return images_data    
    
    def image_to_pdf(self , request):
        try:
            image_file = request.FILES.get("image")
            fs = FileSystemStorage()
            f_name= image_file.name
            input_image_file = fs.save(f_name, image_file)
            
            # Create a new Aspose Words document
            doc = aw.Document()
            builder = aw.DocumentBuilder(doc)

            # Insert the image into the document
            builder.insert_image(fs.path(input_image_file))

            # Generate a unique file name for the PDF
            file_name = os.path.splitext(f_name)[0]
            output_pdf_file = f"{file_name}_{random.randint(10000, 99999)}.pdf"
            file_save_path = fs.path(output_pdf_file)

            # Save the document as a PDF
            doc.save(file_save_path)

            # Generate the URL for the PDF file
            # pdf_url = fs.url(output_pdf_file)
            SAVED_FILE_RESPONSE = save_file_conversion(file_save_path, file_save_path, "application/pdf")
            data = {
                    "media_url": SAVED_FILE_RESPONSE[0],
                    "media_type": "pdf",
                    "media_name": SAVED_FILE_RESPONSE[1]
                }
            serializer = CreateUpdateUploadMediaSerializer(data = data)
            if os.path.exists(file_save_path):
                os.remove(file_save_path)
            if serializer.is_valid():
                serializer.save()
            return {"data":serializer.data,"status":200}

        except Exception as e:
            return {"message": str(e), "status": 400}

        #     file_name = image_file.name

        #     doc = aw.Document()
        #     builder = aw.DocumentBuilder(doc)

        #     builder.insert_image(str(image_file))

        #     doc.save(f"{file_name}.pdf")

        #     return {"message":messages.CONVERT_SUCCESS, "status": 200}
        # except Exception as e:
        #     return {"message": str(e), "status": 400}

    def ppt_to_pdf(self, request):
        ppt_file = request.FILES.get("ppt_file")
        file_name = ppt_file.name

        # Generate a unique file save path
        base_name = f"output_{random.randint(10000, 99999)}"
        temp_dir = tempfile.gettempdir()
        ppt_path = os.path.join(temp_dir, f"{base_name}.pptx")
        pdf_path = os.path.join( f"{base_name}.pdf")

        # Save the uploaded PPT file temporarily
        with open(ppt_path, 'wb') as f:
            for chunk in ppt_file.chunks():
                f.write(chunk)

        # Convert PPT to PDF using images
        conversion_result = self.convert_ppt_to_pdf_with_images(ppt_path, pdf_path)

        if conversion_result["status"] != 200:
            return conversion_result
        

        # Handle the converted PDF
        SAVED_FILE_RESPONSE = save_file_conversion(pdf_path, pdf_path, "application/pdf")
        data = {
            "media_url": SAVED_FILE_RESPONSE[0],
            "media_type": "ppt",
            "media_name": SAVED_FILE_RESPONSE[1]
        }
        save_file_in_model = CategoryModel.objects.create(
                                                            user_id=request.user.id,
                                                            media_id=serializer.data["id"],
                                                            category=6,
                                                            sub_category=17
                                                        )
        serializer = CreateUpdateUploadMediaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

        # Save a copy of the output PDF file to a designated directory on your system
        # designated_dir = os.path.join(tempfile.gettempdir(), 'saved_ppt_pdf_files')
        # os.makedirs(designated_dir, exist_ok=True)
        # final_pdf_path = os.path.join(designated_dir, f"{base_name}.pdf")
        # with open(final_pdf_path, 'wb') as final_pdf_file:
        #     with open(pdf_path, 'rb') as temp_pdf_file:
        #         final_pdf_file.write(temp_pdf_file.read())

        # Clean up temporary files
        if os.path.exists(ppt_path):
            os.remove(ppt_path)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        return {
            "data": serializer.data,
            "message": messages.CONVERT_SUCCESS,
            "status": status.HTTP_200_OK
        }

    def convert_ppt_to_pdf_with_images(self, ppt_path, pdf_path):
        try:
            prs = Presentation(ppt_path)
            temp_dir = tempfile.gettempdir()
            slide_images = []

            for slide in prs.slides:
                slide_img_base = os.path.join(temp_dir, f"slide_{prs.slides.index(slide)}")
                success = self.save_slide_as_image(slide, slide_img_base)
                if success:
                    slide_images.append(slide_img_base)

            if slide_images:
                first_image = Image.open(slide_images[0] + "_0.png")  # Assuming the first image's index is 0
                first_image.save(pdf_path, save_all=True, append_images=[Image.open(f"{img}_0.png") for img in slide_images[1:]])

            # Clean up temporary image files
            for slide_img_base in slide_images:
                for idx in range(len(slide.shapes)):
                    os.remove(f"{slide_img_base}_{idx}.png")

            return {"message": "Conversion successful", "status": 200}
        except Exception as e:
            return {"message": f"Conversion failed: {str(e)}", "status": 500}

    def save_slide_as_image(self, slide, img_path_base):
        try:
            os.makedirs(os.path.dirname(img_path_base), exist_ok=True)
            for idx, shape in enumerate(slide.shapes):
                if not hasattr(shape, 'image'):
                    continue
                image = shape.image
                image_bytes = image.blob
                img_path = f"{img_path_base}_{idx}.png"
                with open(img_path, 'wb') as img_file:
                    img_file.write(image_bytes)
            return True  # Indicate successful operation
        except Exception as e:
            print(f"Error saving slide as image: {str(e)}")
            return False  # Indicate failure    
        


# note
    def voice_to_text(self, request):
        try:
            audio = request.FILES.get("audio")
            recognizer = sr.Recognizer()
            audio = AudioSegment.from_mp3(audio)
            audio.export("audio.wav", format="wav")
            with sr.AudioFile("audio.wav") as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language='en-US')
            return {"message":text, "status": 200}
        except Exception as e:
            return {"message": str(e), "status": 400}
        
    def add_notes(self, request):
        try:
            serializers=categorySerializer.AddNoteSerializer(data=request.data)
            if serializers.is_valid():
                user_obj = serializers.save()
                user_obj.user_id=request.user.id
                user_obj.save()
            return {"data": serializers.data, "message": "note uploaded successfully", "status": 200}
        
        except Exception as e:
            return {"error": str(e), "message": messages.WENT_WRONG, "status": 400}
        

    def ai_explanation(self, request):
        text=request.data.get("text")
        llm = ChatGoogleGenerativeAI(model="gemini-pro")
        try:
            response = llm.invoke(text)
            result_qu = to_markdown(response.content)
            return {"data": result_qu, "message": messages.FETCH, "status": 200}
        except Exception as e:
            return {"error": str(e), "message": messages.WENT_WRONG, "status": 400}
        

    def change_language_note(self, request):
        try:
            text= request.data.get("text")
            translator = GoogleTranslator(source="auto", target="ar")
            answer = translator.translate(text)
            return {"data": answer, "message": messages.FETCH, "status": 200}
        except Exception as e:
            return {"error": str(e), "message": messages.WENT_WRONG, "status": 400}
        
    def get_all_listing_notes(self,request):
        try:
            notes_obj=NoteModel.objects.filter(user_id=request.user.id)
            serializer=categorySerializer.GetNoteSerializer(notes_obj, many=True)
            return{"data":serializer.data,"message":messages.FETCH,"status":200}
        except:
            return{"data":None,"message":messages.WENT_WRONG,"status":400}
        
    def get_notes_by_id(self,request,id):
        try:
            notes_obj=NoteModel.objects.filter(user_id=request.user.id)
            serializer=categorySerializer.GetNoteSerializer(notes_obj)
            return{"data":serializer.data,"message":messages.FETCH,"status":200}
        except:
            return{"data":None,"message":messages.WENT_WRONG,"status":400}




# research
    def to_markdown(text):
        text = text.replace('*', '')
        intent_text=(textwrap.indent(text, '', predicate=lambda _: True))
        return intent_text
    
    def get_research_answer(self, request):
        reduce_citation=request.data.get("reduce_citation")
        description=request.data.get("description")
        if not request.data.get('upload_reference'):
            topic = request.data.get("topic")
            page = request.data.get("page")
            words=int(page)*300
            tone = request.data.get("tone")
            reference = request.data.get("reference")
            

            data=f"generate esaay of {topic} having minimum {words} words answer with tone of voice {tone} by using reference from {reference} and also reduce recitation should be {reduce_citation} and also related to the give description that it {description}"
            query = data
            llm = ChatGoogleGenerativeAI(model="gemini-pro")
            try:
                response = llm.invoke(query)
                result = to_markdown(response.content)
                return{"data":result,"message":messages.FETCH,"status":200}
            except Exception as e:
                return{"data":str(e),"message":messages.WENT_WRONG,"status":400}
        
        pdf_link =request.data['upload_reference']
        data=f"generate esaay of mininimum 500 words from given link {pdf_link} and it should define with this {description} and reduce citation will be {reduce_citation}"
        query = data
        llm = ChatGoogleGenerativeAI(model="gemini-pro")
        try:
            response = llm.invoke(query)
            result = to_markdown(response.content)
            return{"data":result,"message":messages.FETCH,"status":200}
        except Exception as e:
            return{"data":str(e),"message":messages.WENT_WRONG,"status":400}
        

    def save_rsearch_file(self, request):
        try:
            save_pdf=CategoryModel.objects.create(user_id=request.user.id,category=4, sub_category=5,media_id = request.data.get("pdf_file"))
            save_pdf.save()
            return{"data":request.data,"message":"saved successfully","status":200}
        except Exception as e:
            return{"data":str(e),"message":messages.WENT_WRONG,"status":400}
        
    def get_history_research(self, request, id):
        try:
            notes_obj=CategoryModel.objects.filter(user_id=request.user.id, category=id)
            serializer=categorySerializer.GetNoteListSerializer(notes_obj, many=True)
            return{"data":serializer.data,"message":messages.FETCH,"status":200}
        except:
            return{"data":None,"message":messages.WENT_WRONG,"status":400}





# assignment solution
    def get_assignment_solution(self, request):
        try:
            # file_link = request.data.get("file_link")
            file_link = request.FILES.get("file_link")
            print(request.data,"kdfahlkjsdhflakjshdflakjshdflkjh")
            llm = ChatGoogleGenerativeAI(model="gemini-pro")
            try:
                text_data = self.extract_text(file_link)
                message = HumanMessage(
                    content=[
                        {"type": "text",
                         "text": "I am an invligator to mark the questions i need correct answers ,provide me correct answers for these questions and when needed diagrams and figures or explanations just give concise answers and give answers to remaining questions,lastly provide the answers in json list format (question no. ,question, options(this field will will only be there if options are present else no need ), correct answer)"},
                        #  "text": f"list the answers for all questions present  in these given file's (don't leave any question ,even if there is breaks between questions)and provide in  json  format (questtions which have no options just give correct answers in concise manner) try writing answer in this way  (question no. ,question, options(this field will will only be there if options are present else no need ),correct answer) "},
                        {"type": "text", "text":text_data}
                    ]
                )
                response = llm.invoke([message])
                result = to_markdown(response.content)
                print(result, '--------result------------')
                # data = self.jsonify_response(result)
              
                final_response = ""
                for i in range(len(result)-1, -1, -1):
                    if result[i] == "}":
                        break
                final_response = result[result.index("["): i+1] + "]"
                final_response = json.loads(final_response)
                for i in final_response:
                    if not i["options"]:
                        i["question_type"] = 1
                    elif i["options"]:
                        i["question_type"] = 2

                # image_info = upload_media_obj.upload_media(request)
                image_info = upload_media_obj.upload_media(request)
                print(image_info["data"],"333333333333333333333333333333333333333333")
                # if image_info["status"] == 200:
                final_data = AssignmentModel.objects.create(
                    user_id=request.user.id,
                    result = final_response
                )
                final_data.save()
                # elif image_info["status"] == 400:
                #     return {"data": image_info["data"], "message": "Something went wrong", "status": 400}
                return {"data": final_response, "record_id": final_data.id, "message": "RESPONSE", "status": 200}
            except Exception as e:
                return{"data":str(e),"message":messages.WENT_WRONG,"status":400}
        except Exception as e:
            return{"data":str(e),"message":messages.WENT_WRONG,"status":400}

    def get_all_assignment(self, request):
        try:
            data = AssignmentModel.objects.all()
            pagination_obj = CustomPagination()
            search_keys = []
            result = pagination_obj.custom_pagination(request, search_keys, categorySerializer.CreateAssignmentSerializers, data)
            return {"data":result,"message":messages.FETCH,"status":200}
        except Exception as e:
            return {"data":None,"message":messages.WENT_WRONG,"status":400}

    def update_download_file(self, request,id):
        try:
            assignment = AssignmentModel.objects.get(id=id)
            if request.data["type"] == 1:
                if assignment.download_file:
                    return {"data": assignment.download_file, "message":messages.UPDATED,"status":200}
                file = self.html_to_pdf(request)
                assignment.download_file = file    
                assignment.save()
            if request.data["type"] == 2:
                if assignment.download_doc_file:
                    return {"data": assignment.download_doc_file, "message":messages.UPDATED,"status":200}
                file = self.html_to_doc(request)
                assignment.download_doc_file = file    
                assignment.save()
            elif request.data["type"] == 3:
                file = self.html_to_pdf(request)
                Thread(target=send_pdf_file_to_mail, args=(assignment.user.email, file)).start() 
                return {"data":None, "message": "File send to your email successfully", "status":200}
            return {"data": file, "message":messages.UPDATED,"status":200}
        except Exception as e:
            return {"data":None,"message":messages.WENT_WRONG,"status":400}

    def html_to_pdf(self, request):
        try:
            html_text = request.data["html_text"]
            path_to_wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'  # Update this path as necessary
            config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
            file_name = f'{random.randint(10000, 99999)}_file.pdf'
            pdfkit.from_string(html_text, file_name, configuration=config)
            cv = Converter(file_name)
            cv.convert("output_word_file.docx", start=0, end=None)
            cv.close()
            saved_file = saveFile(file_name, "application/pdf")    
            if os.path.exists(file_name):
                os.remove(file_name)
            return saved_file[0]
        except Exception as e:
            return {"data":None,"message":str(e),"status":status.HTTP_400_BAD_REQUEST}
    
    def html_to_doc(self, request):
        try:
            delete_files = []
            html_text = request.data["html_text"]
            path_to_wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'  # Update this path as necessary
            config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
            file_name = f'{random.randint(10000, 99999)}_file.pdf'
            doc_file_name = f'{random.randint(10000, 99999)}_file.docx'
            delete_files = [file_name, doc_file_name]
            pdfkit.from_string(html_text, file_name, configuration=config)
            cv = Converter(file_name)
            cv.convert(doc_file_name, start=0, end=None)
            cv.close()
            saved_file = saveFile(doc_file_name, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")    
            for i in delete_files:
                if os.path.exists(i):
                    os.remove(i)
            return saved_file[0]
        except Exception as e:
            return {"data":None,"messages":str(e),"status":status.HTTP_400_BAD_REQUEST}

    def get_assignment_by_id(self, request, id):
        try:
            data = AssignmentModel.objects.get(id=id)
        except:
            return {"data":None,"message":messages.RECORD_NOT_FOUND, "status":400}

        serializer = categorySerializer.CreateAssignmentSerializers(data)
        return {"data":serializer.data, "message":messages.FETCH, "status":200}
    
            

        

############## settings app ###########

    def get_list_faq(self, request):
        try:   
            user = FaqModel.objects.all()
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer=adminSerializer.FaqModelSerializer(user, many=True)
        return {"data": serializer.data, "message": messages.FETCH, "status": 200}


    def get_terms_condition(self, request):
        try:   
            user = CmsModel.objects.all()
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer=adminSerializer.GetAllTermsConditionSerializer(user, many=True)
        return {"data": serializer.data, "message": messages.FETCH, "status": 200}
    

    def delete_user(self, request):
        try:
            user_obj = UserModel.objects.get(id=request.user.id)
        except UserModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        user_obj.delete()
        return {"data": None, "message": messages.USER_DELETED, "status": 200}
    


# articles

    def get_article_response(self, request):
        
        # topic = request.data.get("topic")
        # words = request.data.get("words")
        # language = request.data.get("language")
        # region = request.data.get("region")
        # tone = request.data.get("tone")
        # pronouns = request.data.get("pronouns")
        image_link = request.data.get("image_link")

        data=f"i want all the data from pdf link {image_link} in json"
        query = data
        llm = ChatGoogleGenerativeAI(model="gemini-pro")
        try:
            response = llm.invoke(query)
            result = to_markdown(response.content)
            return{"data":result,"message":messages.FETCH,"status":200}
        except Exception as e:
            return{"data":str(e),"message":messages.WENT_WRONG,"status":400}


###common for all ####

    def send_file_to_mail(self, request):
        try:
            data = UserModel.objects.get(id = request.user.id)
            email = data.email
            file_link = request.data["file_link"]
            sendMail.send_pdf_file_to_mail(email,file_link)

            return {"data":None,"message":messages.FILE_LINK_SEND, "status":200}
        except Exception as e:
            return{"data":None,"message":messages.WENT_WRONG,"status":400}


       