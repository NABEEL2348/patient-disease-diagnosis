from django.shortcuts import render
from .models import RegisterDataset
from django.contrib import messages
import pandas as pd
import pickle,random
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, chi2

data = pd.read_csv(r"C:\Users\moham\Downloads\Training.csv")
X = data.drop('prognosis', axis=1)  # Features
y = data['prognosis']  # Target variable
"""rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X, y)"""
rf_classifier = pickle.load(open(r"C:\Users\moham\Videos\nabeel_project\Djangoproject\Healtity_project\nabeelModel_saved",'rb'))
selector = SelectKBest(chi2,k=20)
X_new = selector.fit_transform(X, y)
selected_cols = X.columns[selector.get_support()]
print(selected_cols)
selected_cols_index = [X.columns.get_loc(col) for col in selected_cols]

print(selected_cols_index)
def home(request):
    return render(request, 'frontend.html')


def login(request):
    messages.success(request, '')
    if request.method == 'POST':
        datas = RegisterDataset.objects.all()
        name = request.POST['username']
        password = request.POST['password']
        for data in datas:
          if(data.Name == name):
              if(data.Password == password):
                  print("Success")
                  messages.success(request, 'Logged in successfully!')
                  return render(request,'prediction.html')
              else:
                  messages.error(request,"Wrong Credentials!!!")

    return render(request, 'login.html')


def register(request):
    messages.success(request, '')
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        conf_password = request.POST['confirm-password']
        if(password == conf_password):
            obj = RegisterDataset()
            obj.Name = name
            obj.Email = email
            obj.Password = password
            obj.save()
            messages.success(request, 'Registered successfully!')
    return render(request, 'register.html')

def predict_disease(symptoms):
    symptoms = pd.DataFrame(symptoms, columns=X.columns)
    prediction = rf_classifier.predict(symptoms)
    return prediction[0]

def predict(request):
    if request.method == "POST" :
        symptoms =[]
        symp =[]
        li =[50,80,100]
        dt=request.POST.getlist('options')
        print(dt)
        for i in range (0,132) :
            """if i in dt :
                symptoms.append(str(1))
            else :
                  symptoms.append(str(0))"""
            if i<=random.choice(li) and i not in dt:
                symptoms.append(str(0))
            else:
                symptoms.append(str(1))
        symp.append(symptoms)
        result = predict_disease(symp)
        print(result)
        return render(request,'prediction.html',{'result':result})



