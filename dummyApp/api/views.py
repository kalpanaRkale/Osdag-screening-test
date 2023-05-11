from rest_framework import generics,viewsets
from .models import SteelDesign,  Drawing
from .serializers import  SteelDesignSerializer, DrawingSerializer
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import HttpResponse, FileResponse
import io
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework.views import APIView
from ezdxf import readfile


class SteelDesignList(generics.ListCreateAPIView):
    queryset = SteelDesign.objects.all()
    serializer_class = SteelDesignSerializer


class SteelDesignDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SteelDesign.objects.all()
    serializer_class = SteelDesignSerializer


class UserLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


def generate_report(request, pk):
    design = get_object_or_404(SteelDesign, pk=pk, owner=request.user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{design.name}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Report for {design.name}")
    p.drawString(100, 700, f"Description: {design.description}")
    # Add more content to the report as needed
    p.save()
    return response

'''
class AnalysisInputCreate(generics.CreateAPIView):
    queryset = AnalysisInput.objects.all()
    serializer_class = AnalysisInputSerializer


class AnalysisInputDetail(generics.RetrieveAPIView):
    queryset = AnalysisInput.objects.all()
    serializer_class = AnalysisInputSerializer


class AnalysisOutputDetail(generics.RetrieveAPIView):
    queryset = AnalysisOutput.objects.all()
    serializer_class = AnalysisOutputSerializer


class AnalysisStart(generics.GenericAPIView):
    queryset = SteelDesign.objects.all()

    def post(self, request, pk):
        design = get_object_or_404(SteelDesign, pk=pk, owner=request.user)
        analysis_type = request.data.get('analysis_type')
        data = request.data.get('data')
        if analysis_type == 'load':
            result = load_analysis(design, data)
        elif analysis_type == 'structural':
            result = structural_analysis(design, data)
        elif analysis_type == 'stability':
            result = stability_analysis(design, data)
        else:
            return Response({'error': 'Invalid analysis type'}, status=status.HTTP_400_BAD_REQUEST)
        input = AnalysisInput.objects.create(design=design, analysis_type=analysis_type, data=data)
        output = AnalysisOutput.objects.create(input=input, data=result)
        output_serializer = AnalysisOutputSerializer(output)
        return Response(output_serializer.data)


class SteelDesignAnalysisView(generics.GenericAPIView):
    queryset = SteelDesign.objects.all()
    serializer_class = SteelDesignAnalysisSerializer

    def post(self, request, pk):
        design = get_object_or_404(SteelDesign, pk=pk, owner=request.user)
        analysis_type = request.data.get('analysis_type', None)
        if not analysis_type:
            return Response({'error': 'Please specify the analysis type.'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform the analysis based on the analysis_type
        if analysis_type == 'load':
            # Perform load analysis and save the results
            analysis_result = perform_load_analysis(design)
        elif analysis_type == 'structural':
            # Perform structural analysis and save the results
            analysis_result = perform_structural_analysis(design)
        elif analysis_type == 'stability':
            # Perform stability analysis and save the results
            analysis_result = perform_stability_analysis(design)
        else:
            return Response({'error': 'Invalid analysis type.'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the analysis result to the database
        analysis = SteelDesignAnalysis.objects.create(design=design, analysis_type=analysis_type, analysis_result=analysis_result)
        serializer = self.get_serializer(analysis)
        return Response(serializer.data)

    def perform_load_analysis(design):
        # Perform the load analysis and return the results
        # ...
        pass

    def perform_structural_analysis(design):
        # Perform the structural analysis and return the results
        # ...
        pass

    def perform_stability_analysis(design):
        # Perform the stability analysis and return the results
        # ...
        pass
'''

def view_report(request):
    #create Bytestream Buffer
    buf = io.BytesIO()
    #create a canvas
    c= canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",16)

    lines =[ "this is pdf "]

    for line in lines:
        textob.textLine(line)

    #Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='report.pdf')


def view_dwg(request):
    doc = ezdxf.readfile('E:\projects\screening\solids.dwg')
    data = doc.modelspace().export_dxf()
    return HttpResponse(data, content_type='application/dxf')
