from django.db import models
from django.contrib.auth.models import User
from itertools import product
# Create your models here.

class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phno = models.CharField(max_length=10)
    def __str__(self):
        return str(self.user)


class Hospital(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license = models.CharField(unique = True, max_length=10)
    phno = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    intensity = models.FloatField(default=0)
    def __str__(self):
        return str(self.user)

class PatientDetails(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    SEX_CHOICES = (
        ('M','MALE'),
        ('F','FEMALE'),
        ('O','OTHER')
    )
    sex=models.CharField(max_length=7,choices = SEX_CHOICES,null=True, blank=True)
    date_of_birth = models.DateField(blank=True,null=True)

    BLOOD_GROUP_CHOICES = (
        ("A+","A+"),("B+","B+"),("AB+","AB+"), ("O+","O+"),
        ("A-","A-"),("B-","B-"),("AB-","AB-"),("O-","O-")
    )
    blood_group = models.CharField(max_length=10, choices = BLOOD_GROUP_CHOICES, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    pin_code = models.IntegerField(blank=True, null=True)
    district= models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    taluka = models.CharField(max_length=100, null=True, blank=True)


    def get_score(self):
        score = 0
        variables = [self.sex, self.date_of_birth, self.blood_group, self.address, self.pin_code,
        self.district, self.state, self.taluka]
        for var in variables:
            if var != None:
                score+=1

        #calculates Returns the completion score
        return str(score)+"/"+str(len(variables))

    def __str__(self):
        return str(self.patient)

class HospitalDetails(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    RATING_CHOICE = (
    ('1',"POOR"),
    ('2','BELOW AVERAGE'),
    ('3','AVERAGE'),
    ('4','ABOVE AVERAGE'),
    ('5','AMAZING')
    )
    ratings = models.CharField(max_length=20, choices = RATING_CHOICE, default = '1')
    total_ratings = models.PositiveIntegerField(default = 0)
    speech_ratings = models.CharField(max_length=20, choices = RATING_CHOICE, default = '1')
    address = models.CharField(max_length=500, null=True, blank=True)
    pin_code = models.IntegerField(blank=True, null=True)
    district= models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    taluka = models.CharField(max_length=100, null=True, blank=True)
    staff_strength = models.PositiveIntegerField(default=0)
    COST_CLASS = (
    ('1','CHEAP <200'),
    ('2','MODERATE <1000'),
    ('3','EXPENSIVE <10000'),
    ('4','FULL STAR > 10000')
    )
    cost_range = models.CharField(max_length=100, choices = COST_CLASS, default='4')
    operation_facilty = models.BooleanField(default=False)
    emergency_facility = models.BooleanField(default=False)
    beds_count = models.PositiveIntegerField(default = 10)
    beds_occupied = models.PositiveIntegerField(default = 10)

    def get_score(self):
        score = 0
        variables = [
            self.ratings,
            self.total_ratings,
            self.speech_ratings,
            self.address,
            self.pin_code,
            self.district,
            self.state,
            self.taluka,
            self.staff_strength,
            self.cost_range,
            self.operation_facilty,
            self.emergency_facility,
            self.beds_count,
            self.beds_occupied
        ]
        for var in variables:
            if var != None:
                score+=1

            #calculates Returns the completion score
        return str(score)+"/"+str(len(variables))
    def __str__(self):
        return str(self.hospital)


class Reviews(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    spam = models.BooleanField(default=False)
    review = models.TextField(max_length=5000, null=True, blank=True)
    date_time = models.DateTimeField(auto_now=True)
    polarity = models.BooleanField(default=False)
    intensity = models.FloatField(default=0)
    def __str__(self):
        return str(self.hospital)+" <- "+str(self.patient)

class Disease(models.Model):
    diseaseType = models.CharField(default='',max_length=5000, unique = True)
    diseaseName = models.CharField( default='',max_length=5000)
    severity = models.IntegerField(default = 5)
    def __str__(self):
        return str(self.diseaseName) + " - "+str(self.severity)

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital=models.ForeignKey(Hospital,on_delete=models.PROTECT)
    disease=models.ForeignKey(Disease,on_delete=models.CASCADE)
    comment = models.TextField(max_length=5000, null=True, blank=True)
    date_time=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.hospital)+" <- "+str(self.patient)


class special(models.Model):
    hospital=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    diseasetype=models.CharField(max_length=5000, default='nothing')
    def gethosp(self):
        return self.hospital
    def __str__(self):
        return str(self.diseasetype)

class polarity(models.Model):
    hospital=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    pol = models.FloatField(blank=True, null=True)
