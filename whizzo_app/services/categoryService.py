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
from whizzo_app.models.categoryModel import CategoryModel
from whizzo_app.utils import messages
from whizzo_app.serializers import categorySerializer
from deep_translator import GoogleTranslator
import aspose.words as aw
from pdf2docx import Converter
import random
from whizzo_app.utils.saveImage import save_file_conversion
from whizzo_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer
import os
import tabula
import pandas as pd
from reportlab.lib.pagesizes import letter,A3
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Image
from reportlab.lib import colors
from pdf2image import convert_from_path
from django.core.files.storage import FileSystemStorage
import speech_recognition as sr
from pydub import AudioSegment




load_dotenv()
google_api_key = settings.GOOGLE_API_KEY



def to_markdown(text):
  text = text.replace('*', '')
  intent_text=(textwrap.indent(text, '', predicate=lambda _: True))
  return intent_text

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
                if file.endswith((".jpeg",".png",".jpg")):
                    if sub_category == 1:
                        query = f"generate {settings.NUMBER_OF_QUESTIONS} mcqs with options and answers for this image and make in python json list format."
                        result = image_processing(file, query)
                        json_result = self.jsonify_response(result)
                        final_response += json_result
                    elif  sub_category == 2:
                        query = f"generate {settings.NUMBER_OF_QUESTIONS} flashcards for this image and make in python json list format. make a name is frontside and backside not any other name for this and also generate 4-5 backside answers."
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
                        query = f"generate {settings.NUMBER_OF_QUESTIONS} flashcards for this image and make in python json list format. make a name is frontside and backside not any other name for this and also generate 4-5 backside answers."
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
            save_file_summary_record = CategoryModel.objects.create(
                                                    user_id=request.user.id,
                                                    category=2,
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
        summary_history_objects = CategoryModel.objects.filter(
            user_id=request.user.id,
            category=2
        )
        serializer = categorySerializer.GetPreviousTestSerializer(summary_history_objects, many=True)
        return {"data": serializer.data, "message": messages.TESTING_CATEGORY_PAST_TESTS, "status": 200}
    
    def get_file_summary_by_id(self, request, file_id):
        try:
            get_summary_obj = CategoryModel.objects.get(id=file_id)
        except CategoryModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer = categorySerializer.GetFileSummarySerializer(get_summary_obj)
        return {"data": serializer.data, "message": messages.SUMMARY_FETCHED, "status": 200}
    

    ############# FILE CONVERSIONS ###############

    def word_to_pdf(self , request):
        """
            We have to provide the link of the doc file and after
            that we can convert the file into pdf file.
        """
        word_file = request.FILES.get("pdf_file")
        file_name = word_file.name

        doc = aw.Document(word_file)
        doc.save(f"{file_name}.pdf")
        return {"data": "", "message": "conversion is done", "status": 200}
    
    def pdf_to_word(self , request):
        pdf_file = request.FILES.get("pdf_file")
        
        file_name = "".join((pdf_file.name).split(" "))
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
        return {"data": serializer.data, "message": "conversion is done", "status": 200}                
    
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
        return {"data": saved_files, "message": "conversion is done", "status": 200}

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
            file_name = image_file.name

            doc = aw.Document()
            builder = aw.DocumentBuilder(doc)

            builder.insert_image(str(image_file))

            doc.save(f"{file_name}.pdf")

            return {"message":"convert image to pdf successfully", "status": 200}
        except Exception as e:
            return {"message": str(e), "status": 400}
        


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
        
    def add_notes_audio_to_text(self, request):
        try:
            file=request.data.get("pdf_file")
            category_obj=CategoryModel.objects.create(media=file, user=request.user.id, category=3, sub_category=5)
            category_obj.save()
            return {"data": request.data, "message": "note uploaded successfully", "status": 200}
        
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
        
    def get_all_listing_notes(self,request,id):
        try:
            notes_obj=CategoryModel.objects.filter(user_id=request.user.id, category=id)
            serializer=categorySerializer.GetNoteListSerializer(notes_obj, many=True)
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
            image_link=request.data.get("image_link")
            data=f"generate solution from the file of give link{image_link} "
            query = data
            llm = ChatGoogleGenerativeAI(model="gemini-pro")
            try:
                response = llm.invoke(query)
                result = to_markdown(response.content)
                return{"data":result,"message":messages.FETCH,"status":200}
            except Exception as e:
                return{"data":str(e),"message":messages.WENT_WRONG,"status":400}
            
        except Exception as e:
            return{"data":str(e),"message":messages.WENT_WRONG,"status":400}


        

