from email.policy import default
from account.models import User
from django.db import models
from django.utils import timezone
from e_pharmacy import settings
from django.urls import reverse


gender = (
    ('male','Male'),
    ('female','Female'),
)

frequency = (
("1", "1"),
("2", "2"),
("3", "3"),
("4", "4"),
("5", "5"),
("6", "6"),
)

exemption_type = (
    ("None", "None"),
    ("Relative", "Relative "),
    ("Absolute", "Absolute "),
    ("Temporary", "Temporary ")
)

SI = (
    ("mg", "mg"),
    ("g", "g "),
)

class Dosage(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dosage-list')


class Province(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('province-list')

class City(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="1",null=True,blank=True)
    name = models.CharField(max_length=200)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('city-list')

class Suburb(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="11")
    name = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
        # models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('suburb-list')


class MedPractice(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    suburb = models.ForeignKey(Suburb, on_delete=models.PROTECT)
    postal_code = models.CharField(max_length=5)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    reference = models.CharField(max_length=20, unique=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('medprac-list')


class Doctor(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="admin_doctor")
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor", default="")
    surname = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    qualification = models.CharField(max_length=200)
    practice_number = models.ForeignKey(MedPractice, to_field='reference', on_delete=models.CASCADE)
    hc_reg_number = models.CharField(max_length=20)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('doctor-list')


class Pharmacy(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pharmacyAdmin", default="")
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    suburb = models.ForeignKey(Suburb, on_delete=models.PROTECT)
    postal_code = models.CharField(max_length=5)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    license_number = models.CharField(max_length=20)
    pharmacist_name = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('pharmacy-list')


class Pharmacist(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pharm_admin", default="")
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pharm", default="")
    surname = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    reg_number = models.CharField(max_length=200)
    pharmacy_id = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('pharmacist-list')



class ICD10(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    ICD10_code = models.CharField(max_length=20)
    diagnosis = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f'{self.ICD10_code}-{self.diagnosis}'

    def get_absolute_url(self):
        return reverse('ICD10-list')


class ActiveIngredients(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('act-ing-list')



class Medication(models.Model):
    name = models.CharField(max_length=100)
    active_ingridients = models.ForeignKey(ActiveIngredients, on_delete=models.CASCADE)
    dosage_form = models.ForeignKey(Dosage, on_delete=models.CASCADE, default="Tablet")
        # models.ForeignKey(Dosage, on_delete=models.DO_NOTHING)
    strength = models.IntegerField(default="0")
    units = models.CharField(max_length=5, choices=SI, default='1')
    schedule = models.CharField(max_length=5, choices=frequency, default='1')
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('medication-list')

class Patient(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="admin", default="")
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    id_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    suburb = models.ForeignKey(Suburb, on_delete=models.PROTECT)
    postal_code = models.CharField(max_length=5)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    dob = models.DateField()
    date = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=6,choices=gender,default="Male")

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('patient-list')



class MedicalRecord(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="MRadmin", default="1")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="MRdoctor", default="1",)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disease_id = models.ForeignKey(ICD10, on_delete=models.CASCADE)
    medication_name = models.ForeignKey(Medication,null=True,blank=True,on_delete=models.PROTECT, default="")
    active_ingridients = models.ForeignKey(ActiveIngredients, on_delete=models.CASCADE, default='1')
    dosage_form = models.ForeignKey(Dosage, on_delete=models.CASCADE, default='tablet')
    strength = models.IntegerField(default="0")
    units = models.CharField(max_length=5, choices=SI, default='1')
    schedule = models.CharField(max_length=5, choices=frequency, default='1')
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.patient_id.name) + "'s medical record"
    
    def get_absolute_url(self):
        return reverse('med-rec-list')



class ContraIndication(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="adminMedInt", default="")
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(ActiveIngredients, on_delete=models.CASCADE)
    exemption = models.CharField(max_length=20, choices=exemption_type,
                                 default='None')
    start_date = models.DateField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.patient_id.name) + "-" + str(self.medicine_id)+ "-" + str(self.exemption)

    def get_absolute_url(self):
        return reverse('cont-ind-list')



class MedicalInteractions(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medicine_id1 = models.ForeignKey(ActiveIngredients, on_delete=models.CASCADE, related_name='medicine1')
    medicine_id2 = models.ForeignKey(ActiveIngredients, on_delete=models.CASCADE)
    reasons = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.patient_id
    
    def get_absolute_url(self):
        return reverse('med-int-list')



class MedicalHistory(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    drug_allergies = models.CharField(max_length=200)
    chronic_med_hist = models.ForeignKey(ICD10, on_delete=models.CASCADE)
    current_chronic_med = models.ForeignKey(ActiveIngredients, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return str(self.patient) + " " +str(self.patient.surname) + "'s history"
    
    def get_absolute_url(self):
        return reverse('medhist-list')



class Dispense(models.Model):
    pharmacist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    contra_indication = models.ForeignKey(ContraIndication, on_delete=models.CASCADE, default="")
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.medical_record.patient_id)
    
    def get_absolute_url(self):
        return reverse('dispense-list')
    
    
class Reject(models.Model):
    pharmacist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    contra_indication = models.ForeignKey(ContraIndication, on_delete=models.CASCADE, default="")
    reason = models.CharField(max_length=250)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.medical_record.patient_id)
    
    
    def get_absolute_url(self):
        return reverse('reject-detail', kwargs={'pk': self.pk})

status = [
    ('dispensed','Dispensed'),
    ('prescribed','Prescribed')
]

class Prescription(models.Model):
    date = models.DateField(default=timezone.now)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="1")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    repeat = models.IntegerField(default="0")
    repeat_left = models.CharField(max_length=2, default=0)
    quantity = models.IntegerField(default="1")
    dosage_form = models.ForeignKey(Dosage, on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    dispensed_date = models.DateField(auto_now=True)
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE, null=True,blank=True)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, null=True,blank=True)
    status = models.CharField(max_length=10, choices=status, default="prescribed")
        # models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('prescription-list')