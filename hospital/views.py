from django.shortcuts import render, redirect
from django.http import  HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from . import models
from .helpers import auth_helpers
from .helpers import machine
from .helpers import analysis
from .helpers import sentiment
from .helpers import collocations as col
from django.utils import timezone
import nltk
import math
import os
import numpy as np
from nltk.stem import WordNetLemmatizer
from sklearn.linear_model import LogisticRegression
from bs4 import BeautifulSoup
from sklearn.externals import joblib
import nltk
from nltk.collocations import *
from nltk.corpus import stopwords
from nltk.corpus import webtext
from nltk.corpus import PlaintextCorpusReader
import numpy as np
from nltk import FreqDist
from hospital.models import Hospital
from django.db.models import Q
import operator

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url="/hospital")
def home_view(request):
    form = auth_helpers.update_profile_entity(request)
    if auth_helpers.is_hospital(request.user): 
        hosp = models.HospitalDetails.objects.get(hospital=models.Hospital.objects.get(user=request.user))
        review = models.Reviews.objects.filter(hospital=models.Hospital.objects.get(user=request.user))
        dis=models.special.objects.filter(hospital=models.Hospital.objects.get(user=request.user))
        hospname=str(hosp.hospital)
        live=[]
        file = open("/home/helios/Desktop/easclepius/easclepius/"+hospname,'a')
        for i in review: #for storing reviews of this hospital in a list named live 
            live.append(i.review)
            file.write(str(i.review)+"\n")#writing reviews in a file for collocations
        file.close()
        #print(live)
        good=col.give(hospname)
        #print (good)
        good2=[]
        for y in good:                                #good2 is an array of strings
            good2.append(" ".join(str(x) for x in y))
        print("here you go")
        print (good2)
        sent2=analysis.live_review(live)

        hospi=models.Hospital.objects.get(user=request.user)
        models.polarity.objects.filter(hospital=models.Hospital.objects.get(user=request.user)).delete()
        if live: #live stores reviews of a hospital, there may be a case when it contains no value
         models.polarity.objects.create(hospital=hospi,pol = sent2[0])
        if(sent2!=0):
            if sent2[0]>0:
                p="Positive"
            else:
                p="Negative"
            sent3=int(math.floor(sent2[0]*10))
            sent5=sent2[1]*100
            sent6=sent2[2]*100
            sent7 = sent2[3] * 100
            li=[]
            li2=[]
            sent22=sent2[0]
            
        if(sent2==0):
            p="no data available"
            sent3="no data available"
            sent5="no data available"
            sent6="no data available"
            sent7="no data available"
            sent22=sent2

        history=models.MedicalHistory.objects.filter(hospital=models.Hospital.objects.get(user=request.user))
        return render(request, "hospital_profile.html",{'form':form,'hosp':hosp,"review":review,"sent":sent3,"sent2":sent22,
                                                      "sent5":sent5,"sent6":sent6,"sent7":sent7,"polarity":p,"good2":good2,"history":history})
    history = models.MedicalHistory.objects.filter(patient=models.Patient.objects.get(user=request.user))
    ur=models.PatientDetails.objects.get(patient=models.Patient.objects.get(user=request.user))
    return render(request, "patient_profile.html",{'form':form,"ur":ur,"history":history})


def authentication_manager(request):
    if not request.user.is_anonymous:
        return redirect("/hospital/home")
    if request.method == "GET":
        return render(request, "index.html")
    if request.method == "POST":
        req =  request.POST
        username = req["uname"]
        password = req["psw"]
        if req["meta"] == "login":
            #login logic here

            if auth_helpers.login_user(username, password, request):
                return redirect("/hospital/home")
            else:
                return redirect("/hospital")
        elif req["meta"] == "signup":

            #check if similar user exists
            if auth_helpers.signup_patient(request.POST):
                if auth_helpers.login_user(username, password, request):
                    return redirect("/hospital/home")
            return redirect("/hospital")
        else:
            #standard error page
            pass
    return redirect("/hospital")




def logout_view(request):
    if not request.user.is_anonymous:
        logout(request)
    return redirect("/hospital")


def hospital_auth(request):
    if not request.user.is_anonymous:
        return redirect("/hospital/hospital")
    if request.method == "GET":
        return render(request, "hospital_index.html")
    if request.method == "POST":
        req =  request.POST
        username = req["uname"]
        password = req["psw"]
        if req["meta"] == "login":
            #login logic here

            if auth_helpers.login_user(username, password, request):
                return redirect("/hospital/home")
            else:
                return redirect("/hospital/hospital")
        elif req["meta"] == "signup":

            #check if similar user exists
            if auth_helpers.signup_hospital(request.POST):
                if auth_helpers.login_user(username, password, request):
                    return redirect("/hospital/home")
            return redirect("/hospital/hospital")
        else:
            #standard error page
            pass
    return redirect("/hospital/hospital")

@login_required(login_url="/hospital")
def profile_view(request,username):
    comment = "Hi"
    try:
        user=User.objects.get(username=username)
        patient = models.Patient.objects.get(user = user)
        history = models.MedicalHistory.objects.filter(patient=patient).order_by('-date_time')
        if request.method == "POST":
            hospital = models.Hospital.objects.get(user = request.user)
            diseasetype = request.POST["diseasetype"]
            comment = request.POST["comment"]
            disease = models.Disease.objects.get(diseaseType = diseasetype)
            medical_history = models.MedicalHistory.objects.create(hospital = hospital, patient = patient, disease = disease, comment = comment )
        return render(request,"profile_view.html",{"user":user,"history":history, "diseases": models.Disease.objects.all()})
    except:
        return redirect("/hospital")


def filter_hospital(request):
    if request.method == "GET":
        pass
    else:
        pass
    return render(request, 'filter.html')
        # pin_filter = None
        # cost_filter = None
        # name_filter = None
        # speciality_filter = None
        # star_filter = None
        # staff_strength_filter = None

def search_hosp(request):
    #try:
        flag=0
        if request.method=='POST':
            srch=request.POST['srh']
            
            if srch:
                print("true")
                ur=[]
                match=Hospital.objects.filter(Q(user__username__icontains=srch)) 
                print(match)
                if match:
                    print ("pass")
                    m=[]
                    m.append(match)                                              #match 2d array(list inside a list)
                    ur=m
                    print(match)
                    return render(request,"allhospital.html",{"ur":ur,"flag":flag})
                match=models.special.objects.filter(Q(diseasetype__icontains=srch))
                #print(match[1].hospital_id)
                if match:
                    flag=1
                    print("passSpeciality")
                    m=[]
                    for k in match:
                        m.append(Hospital.objects.filter(Q(id__icontains=k.hospital_id)))
                    arr=[]
                    review=[]
                    print(m)
                   
                    for v in m:
                        review.append( models.Reviews.objects.filter(hospital_id=v[0].id)) #review 2d array
                        print(v[0].id)
                    overall={}
                    count=0
                    for re in review:#each hospital in re
                        
                        count+=1
                        print("count="+str(count))
                        summ=0
                        l=0
                        
                        for r in re: #each review
                            summ=summ+r.intensity
                            idk=r
                            
                            print(r.intensity)
                            l=l+1
                        print("lll="+str(l))
                        if l!=0:
                         summ=summ/l
                         print("----------------------")
                         print("sum2="+str(summ))
                         print("----------------------")
                        print("sum2="+str(summ))
                        overall[Hospital.objects.get(id=idk.hospital_id)]=summ
                    asc = sorted(overall.items(), key=operator.itemgetter(1),reverse=True)
                    print(overall)
                    print(asc)
                    ur=m
                    todisp=[]
                    for ii in asc:				#stores only the key (ie Hospital object in array todisp)
                        todisp.append(ii[0])
                    return render(request,"allhospital.html",{"todisp":todisp,"flag":flag})
        

        return render(request,"allhospital.html",{"ur":ur})

    #except:
    #   return redirect("/hospital")
def hosp_profile(request,license):
    #one hospital cannot review another hospital
    print("IS RUNNING")
    try:
        hospital = models.Hospital.objects.get(license=license)
        hospitaldetails=models.HospitalDetails.objects.get(hospital=hospital)
        other_reviews=models.Reviews.objects.filter(hospital=hospital)
    except (models.Hospital.DoesNotExist, models.HospitalDetails.DoesNotExist) :
        return  redirect("/hospital")
    if request.user.is_anonymous:
        review = None
########This code will return values only when new hospital created has open its profile atleast once###############
        good=col.give(str(hospital.user))
        good2=[]
        for y in good:
            good2.append(" ".join(str(x) for x in y))
########Review calculation of polarity##############################################################################
        live=[]
        for i in other_reviews:
            live.append(i.review)
        print (live)
        sent2=analysis.live_review(live)
########Conditions when there is a review###########################################################################
        if(sent2!=0):
            if sent2[0]>0:
                p="Positive"
            else:
                p="Negative"
            sent3=int(math.floor(sent2[0]*10))
            sent5=sent2[1]*100
            sent6=sent2[2]*100
            sent7 = sent2[3] * 100
            li=[]
            li2=[]
            sent22=sent2[0]
            
        if(sent2==0):
            p="no data available"
            sent22=sent2
            sent5=0
            sent6=0
            sent7=0
        print(sent5)
        print(sent6)
        print(sent7)
####################################################################################################################
    else:
        try:
            patient = models.Patient.objects.get(user = request.user)
            hospital = models.Hospital.objects.get(license=license)
            hospitaldetails=models.HospitalDetails.objects.get(hospital=hospital)
            other_reviews=models.Reviews.objects.filter(hospital=hospital)
            review = models.Reviews.objects.filter(hospital=hospital,patient=patient)

        except (models.Patient.DoesNotExist, models.Hospital.DoesNotExist, models.HospitalDetails.DoesNotExist) :
            #review = None
            return  redirect("/hospital")

        #Also get the review if exists
        
########This code will return values only when new hospital created has open its profile atleast once###############
        good=col.give(str(hospital.user))
        good2=[]
        for y in good:
            good2.append(" ".join(str(x) for x in y))
########Review calculation of polarity##############################################################################
        live=[]
        for i in other_reviews:
            live.append(i.review)
        sent2=analysis.live_review(live)
        
########Conditions when there is a review###########################################################################
        if(sent2!=0):
            if sent2[0]>0:
                p="Positive"
            else:
                p="Negative"
            sent3=int(math.floor(sent2[0]*10))
            sent5=sent2[1]*100
            sent6=sent2[2]*100
            sent7 = sent2[3] * 100
            li=[]
            li2=[]
            sent22=sent2[0]
            
        if(sent2==0):
            p="no data available"
            sent22=sent2
            sent5=0
            sent6=0
            sent7=0
####################################################################################################################
        if request.method == "POST":
            review = models.Reviews.objects.get_or_create(hospital=hospital,patient=patient)[0]
            reviewText = request.POST["review_text"]
            print(reviewText)
            review.review = reviewText
            review.date_time = timezone.now()
            #print(type(machine.analyze(reviewText)))
            review.polarity=machine.analyze(reviewText)
            review.intensity=analysis.single(reviewText)
            print(review.intensity)
            review.save();


    return render(request, "viewhospital.html", {"hosp": hospitaldetails,"review":review, "other_reviews":other_reviews, "good2":good2,"sent2":sent22,"polarity":p,"sent5":sent5,"sent6":sent6,"sent7":sent7, "location": str(hospital.user)+","+hospital.location})

def search(request):
    return render(request,'find.html')

def loadspec(request):
    return     render(request, "special.html")

def specialfunc(request):
    #render(request, "special.html")
    print(request.user)
    hospital=models.Hospital.objects.get(user=request.user)
    spec=request.POST.get('spec')
    print(spec)
    speciality = models.special.objects.create(diseasetype = spec, hospital=hospital)
    return redirect("/hospital")

#to check compound positive or neutral analysis function to be used
#to change to our code put changes in hosp_profile()


#EACH HOSPITAL HAS MULTI SPECIALITIES SO ONLY ONE BEING LISTED.
