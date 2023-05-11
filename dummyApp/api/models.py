from django.db import models
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from math import pi


class SteelDesign(models.Model):
    objects = None
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class FinPlateDesign(models.Model):
    # Input Parameters
    beam_depth = models.FloatField()
    beam_width = models.FloatField()
    column_depth = models.FloatField()
    column_width = models.FloatField()
    bolt_diameter = models.FloatField()
    bolt_grade = models.CharField(max_length=10)
    weld_thickness = models.FloatField()
    plate_thickness = models.FloatField()
    plate_length = models.FloatField()
    plate_width = models.FloatField()
    axial_force = models.FloatField()
    shear_force = models.FloatField()
    bending_moment = models.FloatField()
    # Output Parameters
    plate_shear_capacity = models.FloatField(blank=True, null=True)
    bolt_shear_capacity = models.FloatField(blank=True, null=True)
    bolt_bearing_capacity = models.FloatField(blank=True, null=True)
    bolt_capacity = models.FloatField(blank=True, null=True)
    plate_bending_capacity = models.FloatField(blank=True, null=True)
    bolt_required = models.IntegerField(blank=True, null=True)
    plate_required = models.IntegerField(blank=True, null=True)
    plate_thickness_provided = models.FloatField(blank=True, null=True)
    plate_length_provided = models.FloatField(blank=True, null=True)
    plate_width_provided = models.FloatField(blank=True, null=True)
    #fin_plate_design_report = models.OneToOneField('FinPlateDesignReport', on_delete=models.CASCADE, null=True)

class FinPlateDesignReport(models.Model):
    #fin_plate_design = models.OneToOneField(FinPlateDesign, on_delete=models.CASCADE, related_name='report')
    bolt_shear_stress = models.FloatField(blank=True, null=True)
    bolt_bearing_stress = models.FloatField(blank=True, null=True)
    bolt_capacity_check = models.CharField(max_length=10, blank=True, null=True)
    plate_shear_stress = models.FloatField(blank=True, null=True)
    plate_bending_stress = models.FloatField(blank=True, null=True)
    plate_capacity_check = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)


def calculate_finplate_report(fin_plate):
    bolt_diameter = fin_plate.bolt_diameter
    bolt_grade = fin_plate.bolt_grade
    column_flange_thickness = fin_plate.column_flange_thickness
    column_depth = fin_plate.column_depth
    beam_depth = fin_plate.beam_depth
    beam_flange_width = fin_plate.beam_flange_width
    beam_web_thickness = fin_plate.beam_web_thickness
    plate_thickness = fin_plate.plate_thickness
    shear_force = fin_plate.shear_force
    bending_moment = fin_plate.bending_moment
    yield_strength = fin_plate.yield_strength
    safety_factor = fin_plate.safety_factor

    bolt_area = pi * bolt_diameter ** 2 / 4
    bolt_capacity = 0.9 * bolt_area * bolt_grade / safety_factor

    column_flange_net_area = column_flange_thickness * column_depth
    column_flange_capacity = 0.9 * column_flange_net_area * yield_strength / safety_factor

    beam_flange_net_area = beam_flange_width * beam_depth
    beam_flange_capacity = 0.9 * beam_flange_net_area * yield_strength / safety_factor

    plate_net_area = (beam_depth - plate_thickness) * beam_web_thickness
    plate_capacity = 0.9 * plate_net_area * yield_strength / safety_factor

    required_capacity = shear_force / safety_factor + bending_moment / safety_factor
    required_bolt_rows = int((required_capacity / bolt_capacity + 1) / 2)
    required_bolt_cols = 2

    report = {
        'bolt_area': bolt_area,
        'bolt_capacity': bolt_capacity,
        'column_flange_capacity': column_flange_capacity,
        'beam_flange_capacity': beam_flange_capacity,
        'plate_capacity': plate_capacity,
        'required_bolt_rows': required_bolt_rows,
        'required_bolt_cols': required_bolt_cols,
    }

    return report


class Drawing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='drawings/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


'''class AnalysisOutput(models.Model):
    input = models.ForeignKey(AnalysisInput, on_delete=models.CASCADE)
    data = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class SteelDesignAnalysis(models.Model):
    design = models.ForeignKey(SteelDesign, on_delete=models.CASCADE)
    analysis_type = models.CharField(max_length=255)
    analysis_result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.analysis_type} for {self.design.name}" '''