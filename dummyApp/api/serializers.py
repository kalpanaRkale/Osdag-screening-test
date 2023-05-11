from rest_framework import serializers
from .models import SteelDesign, Drawing


class SteelDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteelDesign
        fields = '__all__'


'''class AnalysisInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisInput
        fields = ['id', 'design', 'analysis_type', 'data', 'created_at']


class AnalysisOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisOutput
        fields = ['id', 'input', 'data', 'created_at']

class SteelDesignAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteelDesignAnalysis
        fields = '__all__'  '''


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = '__all__'

