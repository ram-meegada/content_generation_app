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
        print(pdf_file.content_type, '---------------------')
        input_pdf_file = str(pdf_file)
        file_name = "".join((pdf_file.name).split(" "))
        file_name = f"{file_name}_{random.randint(10000, 99999)}"
        output_word_file = f"{file_name}.docx"

        cv = Converter(pdf_file)
        cv.convert(output_word_file, start=0, end=None)
        cv.close()
        SAVED_FILE_RESPONSE = save_file_conversion(output_word_file, f"{file_name}.docx", "word")
        data = {
                    "media_url": SAVED_FILE_RESPONSE[0],
                    "media_type": "word",
                    "media_name": SAVED_FILE_RESPONSE[1]
                }
        serializer = CreateUpdateUploadMediaSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
        if os.path.exists(output_word_file):
            os.remove(output_word_file)
        return {"data": data, "message": messages.PDF_TO_WORD, "status": 200}

    def convert_pdf_to_excel(self , request):
        excel_file = request.FILES.get("pdf_file")
        print(excel_file)
        
        file_name = f"output_{random.randint(10000, 99999)}"

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
        with pd.ExcelWriter(excel_path) as writer:
            for i, table in enumerate(tables):
                table.to_excel(writer, sheet_name=f"Sheet {i+1}", index=False)
                worksheet = writer.sheets[f"Sheet {i+1}"]
                for idx, col in enumerate(table.columns):
                    series = table[col]
                    max_len = max((
                        series.astype(str).map(len).max(),
                        len(str(series.name))
                    )) + 1
                    worksheet.set_column(idx, idx, max_len)