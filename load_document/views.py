import json
import io
import os
from drf_spectacular.utils import extend_schema, OpenApiResponse
import google.generativeai as genai
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PDFUploadSerializer, TextToJsonSerializer
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential


endpoint = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")
api_key = os.getenv("DOCUMENT_INTELLIGENCE_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

class OCRFileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    @extend_schema(
        request={"multipart/form-data": PDFUploadSerializer},
        responses={
            200: OpenApiResponse(response={"type": "object", "properties": {"extracted_text": {"type": "string"}}}, description="Extraction successful"),
            400: OpenApiResponse(response={"type": "object", "properties": {"error": {"type": "string"}}}, description="Validation error"),
            500: OpenApiResponse(response={"type": "object", "properties": {"error": {"type": "string"}}}, description="Server error"),
        },
    )
    def post(self, request):
        serializer = PDFUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            pdf_file = serializer.validated_data["pdf_file"]
            client = FormRecognizerClient(endpoint, AzureKeyCredential(api_key))
            file_stream = io.BytesIO(pdf_file.read())
            poller = client.begin_recognize_content(file_stream)
            result = poller.result()

            extracted_text = "\n".join(line.text for page in result for line in page.lines)

            if not extracted_text.strip():
                return Response({"extracted_text": "No text found in the document."}, status=status.HTTP_200_OK)

            return Response({"extracted_text": extracted_text}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TextToJsonView(APIView):
    @extend_schema(
        request=TextToJsonSerializer,
        responses={
            200: OpenApiResponse(response={"type": "object", "properties": {"extracted_text": {"type": "string"}}}, description="Extraction successful"),
            400: OpenApiResponse(response={"type": "object", "properties": {"error": {"type": "string"}}}, description="Validation error"),
            500: OpenApiResponse(response={"type": "object", "properties": {"error": {"type": "string"}}}, description="Server error"),
        },
    )
    def post(self, request):
        serializer = TextToJsonSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                generation_config={
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                    "response_mime_type": "text/plain",
                },
            )

            chat_session = model.start_chat(history=[
                {"role": "user", "parts": ["You are an AI model designed to transform plain text from menus into JSON. You will only include the following fields: 'products':list of strings, 'price':double, 'is_more_than_one_menu':boolean and 'complementary_prices':boolean. Note that you will have to analyze the data in order to determine if there is more than one menu, this could be because the user inputed menus for multiple days or multiple menu options for the same day. Complementary prices usually come next to a product with or without parenthesis. Transform the text to lower case. Use my next message as a template for the JSON, you will only respond with the JSON as for now respond with 'OK'."]},
                {"role": "model", "parts": ["OK"]},
                {"role": "user", "parts": [r"""menú del día
                            la mordida
                            menú válido desde apertura a 16:00
                            festivos no incluidos
                            comidas y bebidas de méxico
                            lunes
                            miércoles
                            viernes
                            primeros
                            s
                            segundos
                            nachos con pico de gallo
                            crujientes totopos bañados con frijol refrito molido,
                            cochinita pibil taquería
                            ?
                            cubiertos con nuestra mezcla de quesos y pico de gallo
                            envidioso puerco cocinado despacito durante horas en
                            ensalada de aguacate
                            un aderezo traído desde yucatán, acompañado de frijol
                            y arroz.
                            pocos secretos acompañan a esta ensalada de
                            un imprescindible de nuestra carta
                            lechuga, tomate, elote y aguacate fresco
                            pollo con chipotle
                            ?
                            sincronizada de verduras
                            ?
                            dicen que pico, pero no te creas, no es para tanto. dados
                            dos tortillas. en medio, queso y verduras a la plancha,
                            de pechuga de pollo en salsa de chile chipotle con crema
                            acompañadas de pico de gallo
                            de leche. acompañado de arroz
                            lentejas de olla
                            tinga de guajolote
                            ?
                            lentejas guisadas con cebolla, ajo, batata, chorizo,
                            guiso de pavo con cebolla, tomate, orégano y un toque de
                            especias y un pelín de jalapeño
                            chile chipotle, acompañado de arroz y tortillas
                            huevos rancheros
                            fajitas de verdura
                            ?
                            en tortillas de maíz tostadas, un par de huevos
                            bañados con salsa de jitomate tatemado
                            la misma locura de nuestras fajitas, pero en este caso
                            solo con vegetales. cocinados a la plancha y
                            acompañados de arroz y tortillas
                            bebidas
                            chili con carne
                            ?
                            sor chili inspiró la receta desde el más allá, así que
                            agua
                            no le hagas un feo y regodéate con este guiso de carne
                            picada con frijoles y chili
                            caña de cerveza
                            refresco
                            copa de vino
                            postres
                            pide tu jarra de cerveza, 1/2 litro +1€
                            café de olla
                            crepa con nata y chocolate
                            auténtica cocina mexicana también para llevar
                            a elegir
                            entre:
                            helado
                            ¡abierto todos los días!
                            chupito de margarita (1€ extra)
                            si tienes alguna alergia o intolerancia ,
                            por favor coméntaselo a nuestro personal
                            vegetariano
                            sin gluten
                            x
                            ? puede ser sin gluten
                            pica poco
                            pica medio
                            pica mucho
                            menú del día
                            la mordida
                            menú válido desde apertura a 16:00
                            festivos no incluidos
                            comidas y bebidas de méxico
                            martes \ | /jueves
                            primeros
                            segundos
                            ensalada de pollo con manzana
                            x
                            pollo yucateco
                            ?
                            una base de lechuga cubierta con tiras de pollo y tiras
                            de tortilla de maíz fritas, flanqueada por manzana,
                            pollo marinado en zumo de naranja, vinagre de manzana,
                            cebolla encurtida y salsa mariachi
                            achiote y especias. cocinado muy lento, acompañado de
                            frijol, arroz y tortillas.
                            nachos con pico de gallo
                            x
                            crujientes totopos bañados con frijol refrito molido,
                            tostadas de tinga
                            cubiertos con nuestra mezcla de quesos y pico de gallo
                            dos tortillas de maíz tostadas, con frijol, tinga de
                            sincronizada pibil
                            ?
                            guajolote, lechuga y aguacate.
                            dos tortillas. en medio, queso y nuestra cochinita pibil
                            cochinita pibil taquería
                            ?
                            taquería, acompañada de pico de gallo
                            sopa azteca
                            envidioso puerco cocinado despacito durante horas en
                            x
                            un aderezo traído desde yucatán, acompañado de frijol
                            rica sopa de tortilla, elaborada con mucho amor, jitomate
                            y arroz.
                            molido y más cositas. acompañada detiras de tortilla frita,
                            un imprescindible de nuestra carta
                            chile pasilla y lima.
                            tostada de atún endiablado
                            enfrijoladas
                            tortilla de maíz tostada, con frijol refrito, lechuga, atún
                            dos tortillas de maíz rellenas con queso y pollo, bañadas
                            endiablado, lombarda y crema agria.
                            en salsa
                            chili vegano
                            bebidas
                            sor chili inspiró la receta desde el más allá, y nosotros
                            creamos la versión vegana, disfruta con este guiso de
                            agua
                            soja texturizada con frijoles y chili
                            caña de cerveza
                            refresco
                            copa de vino
                            pide tu jarra de cerveza, 1/2 litro +1€
                            postres
                            auténtica cocina mexicana tambien para llevar
                            café de olla
                            ¡abierto todos los días!
                            a elegir
                            crepa con nata y chocolate
                            entre:
                            helado
                            si tienes alguna alergia o intolerancia ,
                            por favor coméntaselo a nuestro personal
                            vegetariano
                            sin gluten
                            x
                            ? puede ser sin gluten
                            pica poco
                            pica medio
                            pica mucho"""
                ]},
                {"role": "model", "parts": [r"""{
                                "products": [
                                    "nachos con pico de gallo",
                                    "cochinita pibil taquería",
                                    "ensalada de aguacate",
                                    "pollo con chipotle",
                                    "sincronizada de verduras",
                                    "lentejas de olla",
                                    "tinga de guajolote",
                                    "huevos rancheros",
                                    "fajitas de verdura",
                                    "chili con carne",
                                    "agua",
                                    "caña de cerveza",
                                    "refresco",
                                    "copa de vino", 
                                    "café de olla", 
                                    "crepa con nata y chocolate", 
                                    "helado", 
                                    "chupito de margarita", 
                                    "ensalada de pollo con manzana", 
                                    "pollo yucateco", 
                                    "tostadas de tinga", 
                                    "sincronizada pibil", 
                                    "sopa azteca",  
                                    "tostada de atún endiablado",  
                                    "chili vegano"
                                ],
                                "price": 21.95,
                                "is_more_than_one_menu": true,
                                "complementary_prices": true,
                            }"""
                ]}
            ])

            response = chat_session.send_message(serializer.validated_data["string"])
            json_string = response.text.replace("```json", "").replace("```", "")
            extracted_data = json.loads(json_string)

            return Response({"extracted_text": extracted_data}, status=status.HTTP_200_OK)

        except json.JSONDecodeError as e:
            return Response({"error": f"Invalid JSON from Gemini: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OcrToJsonView(APIView):
    parser_classes = (MultiPartParser,)

    @extend_schema(
        request={"multipart/form-data": PDFUploadSerializer},
        responses={
            200: OpenApiResponse(response={"type": "object", "properties": {"extracted_json": {"type": "object"}}}, description="OCR and JSON extraction successful"),
            400: OpenApiResponse(response={"type": "object", "properties": {"error": {"type": "string"}}}, description="Validation error"),
            500: OpenApiResponse(response={"type": "object", "properties": {"error": {"type": "string"}}}, description="Server error"),
        },
    )
    def post(self, request):
        pdf_serializer = PDFUploadSerializer(data=request.data)
        if not pdf_serializer.is_valid():
            return Response(pdf_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            pdf_file = pdf_serializer.validated_data["pdf_file"]
            client = FormRecognizerClient(endpoint, AzureKeyCredential(api_key))
            file_stream = io.BytesIO(pdf_file.read())
            poller = client.begin_recognize_content(file_stream)
            result = poller.result()

            extracted_text = "\n".join(line.text for page in result for line in page.lines)

            if not extracted_text.strip():
                return Response({"error": "No text found in the document."}, status=status.HTTP_400_BAD_REQUEST)

            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                generation_config={
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                    "response_mime_type": "text/plain",
                },
            )

            chat_session = model.start_chat(history=[
                {"role": "user", "parts": ["You are an AI model designed to transform plain text from menus into JSON. You will only include the following fields: 'products':list of strings, 'price':double, 'is_more_than_one_menu':boolean and 'complementary_prices':boolean. Note that you will have to analyze the data in order to determine if there is more than one menu, this could be because the user inputed menus for multiple days or multiple menu options for the same day. Complementary prices usually come next to a product with or without parenthesis. Transform the text to lower case. Use my next message as a template for the JSON, you will only respond with the JSON as for now respond with 'OK'."]},
                {"role": "model", "parts": ["OK"]},
                {"role": "user", "parts": [r"""menú del día
                            la mordida
                            menú válido desde apertura a 16:00
                            festivos no incluidos
                            comidas y bebidas de méxico
                            lunes
                            miércoles
                            viernes
                            primeros
                            s
                            segundos
                            nachos con pico de gallo
                            crujientes totopos bañados con frijol refrito molido,
                            cochinita pibil taquería
                            ?
                            cubiertos con nuestra mezcla de quesos y pico de gallo
                            envidioso puerco cocinado despacito durante horas en
                            ensalada de aguacate
                            un aderezo traído desde yucatán, acompañado de frijol
                            y arroz.
                            pocos secretos acompañan a esta ensalada de
                            un imprescindible de nuestra carta
                            lechuga, tomate, elote y aguacate fresco
                            pollo con chipotle
                            ?
                            sincronizada de verduras
                            ?
                            dicen que pico, pero no te creas, no es para tanto. dados
                            dos tortillas. en medio, queso y verduras a la plancha,
                            de pechuga de pollo en salsa de chile chipotle con crema
                            acompañadas de pico de gallo
                            de leche. acompañado de arroz
                            lentejas de olla
                            tinga de guajolote
                            ?
                            lentejas guisadas con cebolla, ajo, batata, chorizo,
                            guiso de pavo con cebolla, tomate, orégano y un toque de
                            especias y un pelín de jalapeño
                            chile chipotle, acompañado de arroz y tortillas
                            huevos rancheros
                            fajitas de verdura
                            ?
                            en tortillas de maíz tostadas, un par de huevos
                            bañados con salsa de jitomate tatemado
                            la misma locura de nuestras fajitas, pero en este caso
                            solo con vegetales. cocinados a la plancha y
                            acompañados de arroz y tortillas
                            bebidas
                            chili con carne
                            ?
                            sor chili inspiró la receta desde el más allá, así que
                            agua
                            no le hagas un feo y regodéate con este guiso de carne
                            picada con frijoles y chili
                            caña de cerveza
                            refresco
                            copa de vino
                            postres
                            pide tu jarra de cerveza, 1/2 litro +1€
                            café de olla
                            crepa con nata y chocolate
                            auténtica cocina mexicana también para llevar
                            a elegir
                            entre:
                            helado
                            ¡abierto todos los días!
                            chupito de margarita (1€ extra)
                            si tienes alguna alergia o intolerancia ,
                            por favor coméntaselo a nuestro personal
                            vegetariano
                            sin gluten
                            x
                            ? puede ser sin gluten
                            pica poco
                            pica medio
                            pica mucho"""
                ]},
                {"role": "model", "parts": [r"""{
                                "products": [
                                    "nachos con pico de gallo",
                                    "cochinita pibil taquería",
                                    "ensalada de aguacate",
                                    "pollo con chipotle",
                                    "sincronizada de verduras",
                                    "lentejas de olla",
                                    "tinga de guajolote",
                                    "huevos rancheros",
                                    "fajitas de verdura",
                                    "chili con carne",
                                    "agua",
                                    "caña de cerveza",
                                    "refresco",
                                    "copa de vino", 
                                    "café de olla", 
                                    "crepa con nata y chocolate", 
                                    "helado", 
                                    "chupito de margarita", 
                                    "ensalada de pollo con manzana", 
                                    "pollo yucateco", 
                                    "tostadas de tinga", 
                                    "sincronizada pibil", 
                                    "sopa azteca",  
                                    "tostada de atún endiablado",  
                                    "chili vegano"
                                ],
                                "price": 21.95,
                                "is_more_than_one_menu": true,
                                "complementary_prices": true,
                            }"""
                ]}
            ])

            response = chat_session.send_message(extracted_text)
            json_string = response.text.replace("```json", "").replace("```", "")
            extracted_json = json.loads(json_string)

            return Response({"extracted_json": extracted_json}, status=status.HTTP_200_OK)

        except json.JSONDecodeError as e:
            return Response({"error": f"Invalid JSON from Gemini: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)