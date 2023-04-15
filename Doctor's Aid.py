open('doctors_aid_outputs.txt', 'w').close() #clears the doctors_aid_outputs.txt
data_list = [] #main data list
lines = [] #list with all inputs
patient = [] #for find specified patient's information in create section
data = [] #temporary data list
number = 0 #command counter
def read():
    global lines
    with open('doctors_aid_inputs.txt', 'r') as f:
        lines = f.readlines()
def output(text):
    with open('doctors_aid_outputs.txt', mode='a', encoding="utf-8") as x:
        x.write(str(text) + "\n")
def create():
    global patient
    global data_list
    patient.pop(0)
    if data_list.__contains__(patient[0][:-1]):
        output("Patient " + patient[0][:-1] + " cannot be recorded due to duplication.")
    else:
        patient[2:4] = [" ".join(patient[2:4])] #merges the indexes with 2 words
        if len(patient) == 7:
            patient[4:6] = [" ".join(patient[4:6])] #merges the indexes with 2 words
        for i in range(len(patient)):
            patient[i] = patient[i].replace(",","")
        data_list += patient
        output("Patient " + patient[0] + " is recorded.")
    patient.clear()
def remove():
    if not (data_list.__contains__(name[number][:-1])):
        output("Patient " + name[number][:-1] + " cannot be removed due to absence.")
    else:
        patients_index = data_list.index(patient_name[:-1])
        del data_list[patients_index:patients_index + 6]
        output("Patient " + name[number][:-1] + " is removed.")
def probability():
    global patient_name
    if(patient_name.__contains__("\n")):
            patient_name = patient_name[:-1]
    if not (data_list.__contains__(patient_name)):
        output("Probability for " + patient_name + " cannot be calculated due to absence.")
    else:
        patients_index = data_list.index(patient_name)
        wrong_diag = 1-float(data_list[patients_index+1])
        inc = (data_list[patients_index+3]).split("/")
        per_inc = int(inc[0]) / int(inc[1])
        act_diag = per_inc / (wrong_diag + per_inc)
        act_diag *= 100
        act_diag = "{0:.2f}".format(act_diag)
        act_diag = ('%f' % float(act_diag)).rstrip('0').rstrip('.')  + "%"
        output("Patient " + patient_name + " has a probability of " + act_diag + " of having " + str.lower(data_list[((patients_index + 2))]) + ".")
def recommendation():
    global patient_name
    if(patient_name.__contains__("\n")):
        patient_name = patient_name[:-1]
    if not (data_list.__contains__(patient_name)):
        output("Recommendation for " + patient_name + " cannot be calculated due to absence.")
    else:
        patients_index = data_list.index(patient_name)
        wrong_diag = 1-float(data_list[patients_index+1])
        inc = (data_list[patients_index+3]).split("/")
        per_inc = int(inc[0]) / int(inc[1])
        act_diag = per_inc / (wrong_diag + per_inc)
        if act_diag < float(data_list[patients_index + 5]):
            output("System suggests " + patient_name + " NOT to have the treatment.") 
        else:
            output("System suggests " + patient_name + " to have the treatment.")
def _list():
    output("Patient".ljust(8) + "Diagnosis".ljust(12) + "Disease".ljust(16) + "Disease".ljust(12) + "Treatment".ljust(16) + "Treatment")
    output("Name".ljust(8) + "Accuracy".ljust(12) + "Name".ljust(16) + "Incidence".ljust(12) + "Name".ljust(16) + "Risk")
    output("-------------------------------------------------------------------------")
    for i in range(0,len(data_list),6):
        acc = "{0:.2f}%".format(float(data_list[i+1])*100)
        risk = "{0:.0f}%".format(float(data_list[i+5])*100)
        output(data_list[i].ljust(8) + acc.ljust(12) + data_list[i+2].ljust(16) + data_list[i+3].ljust(12) + data_list[i+4].ljust(16) + risk)
def zero_index(lst): #finds the first indexes(commands)
    items = []
    for item in lst:
        items.append(item.split(" ")[0])
    return items
def one_index(lst): #finds the second indexes (names)
    items = []
    for item in lst:
        if item == "list\n":
            items.append("a")
        else:
            items.append(item.split(" ")[1])
    return items
read()
for item in lines:
    data.append(item.split(" "))
command = zero_index(lines)
name = one_index(lines)
for i in range(len(command)):
    number = i
    if command[i] == "create":
        patient.append(data[i])
        patient = patient[0]
        create()
    elif command[i] == "remove":
        patient_name = name[i]
        remove()
    elif command[i] == "probability":
        patient_name = name[i]
        probability()
    elif command[i] == "recommendation":
        patient_name = name[i]
        recommendation()
    elif command[i] == "list\n":
        _list()
    number += 1
