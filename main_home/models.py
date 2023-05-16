from datetime import timezone
from django.db import models
from django.forms import ValidationError
from client.models import Client
from nurse.models import Nurse
from receptionist.models import Receptionist
from django.utils import timezone


# Get the current time in Algeria timezone


# Create your models here.

class Complaint(models.Model):
    TOPIC_CHOICES = [
        ('Billing', 'Billing'),
        ('Customer Service', 'Customer Service'),
        ('Facilities', 'Facilities'),
        ('Quality of Service', 'Quality of Service'),
        ('Other', 'Other'),
    ]

    date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f"Complaint #{self.id}"

    class Meta:
        db_table = 'complaint'
        

class Laboratory(models.Model):
    name = models.CharField(max_length=45, primary_key=True)
    location = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    monthly_revenue = models.FloatField()
    tests_made = models.FloatField()

    class Meta:
        db_table = 'laboratory'
        verbose_name_plural = 'Laboratories'
        
    def __str__(self):
        return self.name
        
class ComponentInformation(models.Model):
    name = models.CharField(max_length=50, unique=True)
    unit = models.CharField(max_length=45, null=True, blank=True)
    low_male_range = models.FloatField(null=True, blank=True)
    high_male_range = models.FloatField(null=True, blank=True)
    low_female_range = models.FloatField(null=True, blank=True)
    high_female_range = models.FloatField(null=True, blank=True)
    
    class Meta:
            db_table = 'component_info'
            verbose_name_plural = 'Component Info'
    
    def __str__(self):
        return self.name
    
class Component(models.Model):
    info = models.ForeignKey(ComponentInformation, on_delete=models.CASCADE)
    value = models.FloatField()

    class Meta:
        db_table = 'component'
        
        
    def __str__(self):
        return f'{self.info.name} value:{self.value}'

class TestOffered(models.Model):
    name = models.CharField(max_length=50,unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'test_offered'
        verbose_name_plural = 'Offered Tests'
        
    def __str__(self):
        return self.name
            
class Test(models.Model):
    test_offered = models.ForeignKey(TestOffered,on_delete=models.CASCADE)
    components = models.ManyToManyField(Component)
    value = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True, blank=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
            db_table = 'test'
            verbose_name_plural = 'Tests Preformed'
            
    def __str__(self):
        return self.test_offered.name
        
class BloodBank(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.username} - {self.blood_type}"
 
 
def validate_date_not_past(date):
    if date < timezone.now:
        # dont allow dates from the past
        raise ValidationError('The date cannot be in the past.')
    elif Appointment.objects.filter(date=date).count() >= 50:
        # Don't allow more than 50 appointments per day
        raise ValidationError("Sorry, no more appointments available on this day. Max is 50 per day.")
    
class MedicalDocument(models.Model):
    
    image = models.ImageField(upload_to='medical_documents/')
 
    class Meta:
        db_table = 'medical_document'
           
class Appointment(models.Model):
    PRE_PAY = 'PP'
    ON_RECEIVE = 'OR'
    PAYMENT_CHOICES = [
        (PRE_PAY, 'Pre-Pay'),
        (ON_RECEIVE, 'On-Receive'),
    ]
    
    UPCOMING = 'Upcoming'
    TOMORROW = 'Tommorow'
    TODAY = 'Today'
    OVERDUE = 'Overdue'
    STATUS_CHOICES = [
        (UPCOMING, 'Upcoming'),
        (TOMORROW, 'Tommorow'),
        (TODAY, 'Today'),
        (OVERDUE, 'Overdue'),
    ]
    
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    tests_requested = models.ManyToManyField(Test) 
    date = models.DateField(validators=[validate_date_not_past],)
    description = models.CharField(max_length=1000)
    documents = models.ManyToManyField(MedicalDocument)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_option = models.CharField(max_length=2, choices=PAYMENT_CHOICES)
    payment_status = models.BooleanField(default=False)
    attended = models.BooleanField(default=False)

    class Meta:
        db_table = 'appointment'
        
    def __str__(self):
        return f"Appointment #{self.id}"
    
    @property
    def status(self):
        today = timezone.now().date()
        
        if self.date > today:
            return self.UPCOMING
        elif self.date == today:
            return self.TODAY
        elif self.date == today + timezone.timedelta(days=1):
            return self.TOMORROW
        else:
            return self.OVERDUE
     
class AnalysisRequest(models.Model):
    PENDING = 'pending'
    WORKING_ON = 'working-on'
    FINISHED = 'finished'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (WORKING_ON, 'Working On'),
        (FINISHED, 'Finished'),
    ]
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    accepted = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    status =  models.CharField(max_length=45, choices=STATUS_CHOICES, default=PENDING)
    
    def duration(self):
        if self.finish_time:
            duration = self.finish_time - self.start_time
        else:
            duration = timezone.now() - self.start_time
        return duration
    
    def save(self, *args, **kwargs):
        if self.accepted and not self.start_time:
            self.start_time = timezone.now()
            self.status = self.WORKING_ON
        if self.finished and not self.finish_time:
            self.finish_time = timezone.now()
            self.status = self.FINISHED
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'analysis_request'
        
    def __str__(self):
        return f"{self.appointment.client.user.username} - Analysis Requested #{self.id}"
    
    
    
class TestResult(models.Model):
    request = models.ForeignKey(AnalysisRequest, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    tests = models.ManyToManyField(Test)
    blood_sample = models.ForeignKey(BloodBank, on_delete=models.CASCADE)
    duration = models.DurationField(null=True, blank=True)
    approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'test_result'
        
    def __str__(self):
        return f"Test Result #{self.id}"
        
class Report(models.Model):
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    
    class Meta:
        db_table = 'report'
        
    def __str__(self):
        return f"Report #{self.id}"

class Invoice(models.Model):
    PRE_PAY = 'PP'
    ON_RECEIVE = 'OR'
    PAYMENT_CHOICES = [
        (PRE_PAY, 'Pre-Pay'),
        (ON_RECEIVE, 'On-Receive'),
    ]
    
    creation_time = models.DateTimeField(auto_now_add=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_option = models.CharField(max_length=2, choices=PAYMENT_CHOICES)
    payment_status = models.BooleanField(default=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'invoice'
        
    def __str__(self):
        return f"Invoice #{self.id}"
