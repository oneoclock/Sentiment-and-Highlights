from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from . import helperforms
from .. import models
def check_unique_field(field_name, field_value):
    if field_name == "username":
        return not bool(len(User.objects.filter(username=field_value)))
    return not bool(len(User.objects.filter(email=field_value)))

def passwords_match(password, repassword):
    return password == repassword

def login_user(username, password, request):
    user = authenticate(username=username,password=password)
    if user is not None:
        login(request, user)
        return True
    return False

def signup_patient(request):
    first_name = request["first_name"]
    last_name = request["last_name"]
    username = request["uname"]
    password = request["psw"]
    confirm_password = request["psw-repeat"]
    email = request["email"]
    phno = request["phno"]
    try:
        if check_unique_field("username", username) and \
        passwords_match(password, confirm_password) and \
        check_unique_field("email", email):
            user = User.objects.create(username=username,
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email)
            user.set_password(password)
            user.save()
            patient = models.Patient.objects.create(user = user, phno = phno)
            return True
    except:
        return False

def signup_hospital(request):
    username = request["uname"]
    password = request["psw"]
    confirm_password = request["psw-repeat"]
    email = request["email"]
    phno = request["phno"]
    license = request["license"]
    location = request["location"]
    #speciality = request["speciality"]
    description = request["description"]
    try:
        if check_unique_field("username", username) and \
        passwords_match(password, confirm_password) and \
        check_unique_field("email", email):
            user = User.objects.create(username=username,
                                        email=email)
            user.set_password(password)
            user.save()
            hospital = models.Hospital.objects.create(user = user,license=license,location=location, description=description, phno = phno)
            #print("RESOLVE THIS SH")
            #print(hospital.user)
            #speciality = models.special.objects.create(diseasetype = speciality, hospital=models.Hospital.objects.get(user))
            return True
    except:
        return False

def is_hospital(user):
    return len(models.Hospital.objects.filter(user = user))!=0

def update_profile_entity(request):
    userobj = User.objects.get(username=request.user)
    if is_hospital(request.user):
        entity = "hospital"
    else:
        entity = "patient"

    if entity == "patient":
        patient = models.Patient.objects.get(user = userobj)
        try:
            patient_details = models.PatientDetails.objects.get(patient=patient)
        except models.PatientDetails.DoesNotExist:
            patient_details = models.PatientDetails.objects.create(patient=patient)
        if request.method == "POST":
            form = helperforms.PatientDetailsForm(request.POST,instance=patient_details)
            if form.is_valid():
                patientdetails = form.save(commit=False)
                patientdetails.patient = patient
                patientdetails.save()
        else:
            form = helperforms.PatientDetailsForm(instance=patient_details)
    else:
        hospital = models.Hospital.objects.get(user = userobj)
        try:
            hospital_details = models.HospitalDetails.objects.get(hospital = hospital)
        except models.HospitalDetails.DoesNotExist:
            hospital_details = models.HospitalDetails.objects.create(hospital = hospital)
        if request.method == "POST":
            form = helperforms.HospitalDetailForm(request.POST,instance=hospital_details)
            if form.is_valid():
                hospitaldetails = form.save(commit=False)
                hospitaldetails.hospital = hospital
                hospitaldetails.save()
        else:
            form = helperforms.HospitalDetailForm(instance = hospital_details)
    return form
