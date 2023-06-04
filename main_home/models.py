from datetime import timedelta, timezone
from django.db import models
from django.forms import ValidationError
from auditor.models import Auditor
from client.models import Client
from nurse.models import Nurse
from receptionist.models import Receptionist
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User



# Get the current time in Algeria timezone


# Create your models here.

class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    nurse = models.OneToOneField(Nurse, on_delete=models.CASCADE)
    auditor = models.ForeignKey(Auditor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.sender.username} | To: {self.receiver.username}"
    
    
class Complaint(models.Model):
    TOPIC_CHOICES = [
        ('Billing', 'Billing'),
        ('Customer Service', 'Customer Service'),
        ('Facilities', 'Facilities'),
        ('Quality of Service', 'Quality of Service'),
        ('Other', 'Other'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
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

    class Meta:
        db_table = 'laboratory'
        verbose_name_plural = 'Laboratories'

    @property
    def tests_made(self):
        return Test.objects.filter().count()
    
    def calculate_monthly_revenue(self):
        current_month = timezone.now().month
        current_year = timezone.now().year
        invoices = Invoice.objects.filter(laboratory=self, creation_time__month=current_month, creation_time__year=current_year)
        total_revenue = invoices.aggregate(total=Sum('total_price'))['total']
        monthly_revenue, _ = MonthlyRevenue.objects.get_or_create(laboratory=self, month=current_month, year=current_year)
        monthly_revenue.revenue = total_revenue or 0
        monthly_revenue.save()

    def get_average_monthly_revenue(self):
        total_revenue = MonthlyRevenue.objects.filter(laboratory=self).aggregate(total=Sum('revenue'))['total']
        months_count = MonthlyRevenue.objects.filter(laboratory=self).count()
        return total_revenue / months_count if months_count else 0

    def __str__(self):
        return self.name
    
class MonthlyRevenue(models.Model):
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    revenue = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'monthly_revenue'

    def __str__(self):
        return f"{self.laboratory} - {self.month}/{self.year}"
        
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
    value = models.FloatField(null=True,blank=True)

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
    value = models.CharField(max_length=100,blank=True,null=True)
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
    
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    submission_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.user.username} - {self.blood_type}"
 
 
def validate_date_not_past(date):
    if date < timezone.now().date():
        # dont allow dates from the past
        raise ValidationError('The date cannot be in the past.')
    elif Appointment.objects.filter(date=date).count() >= 50:
        # Don't allow more than 50 appointments per day
        raise ValidationError("Sorry, no more appointments available on this day. Max is 50 per day.")
    
class MedicalDocument(models.Model):
    
    image = models.ImageField(upload_to='medical_documents')
 
    class Meta:
        db_table = 'medical_document'
           
class Appointment(models.Model):
    
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
    tests_requested = models.ManyToManyField(TestOffered) 
    date = models.DateField(validators=[validate_date_not_past])
    description = models.CharField(max_length=1000,blank=True)
    document = models.ImageField(null=True,blank=True,upload_to='medical_documents')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    arrived = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    performed = models.BooleanField(default=False)

    class Meta:
        db_table = 'appointment'
        
    def __str__(self):
        return f"Appointment #{self.id}"
    
    @property
    def cancelable(self):
        time_difference = self.date - timezone.now().date()
        return time_difference.days
        
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
   
   
class Payment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    appointment_fee = models.DecimalField(max_digits=10, decimal_places=2,default=5.00)
    tests_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    nurse_tests_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payed_appointment_fee = models.BooleanField(default=False)
    payed_tests_fee = models.BooleanField(default=False)
    payed_nurse_tests_fee = models.BooleanField(default=False)
    total_amount_payed = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

    def __str__(self):
        return f"Payment for {self.appointment}"
    
    def save(self, *args, **kwargs):
        if self.tests_fee == 0.00:
            self.tests_fee = self.appointment.total_price
        super().save(*args, **kwargs)
   
class Lobby(models.Model):
    nurse = models.OneToOneField(Nurse, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Appointment, blank=True)
    
    class Meta:
        verbose_name_plural = 'Lobbies'
        
    def __str__(self):
        return f"Lobby: {self.nurse}"
       
class AnalysisRequest(models.Model):
    PENDING = 'pending'
    WORKING_ON = 'working-on'
    FINISHED = 'finished'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (WORKING_ON, 'Working On'),
        (FINISHED, 'Finished'),
    ]
    
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    tests = models.ManyToManyField(Test)
    creation_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    accepted = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    status =  models.CharField(max_length=45, choices=STATUS_CHOICES, default=PENDING)
    
    def duration_unformated(self):
        if self.start_time :
            if self.finish_time:
                duration = self.finish_time - self.start_time
            else:
                duration = timezone.now() - self.start_time
            return duration
        
        return 0 
    
    def duration(self):
        if self.start_time:
            if self.finish_time:
                duration = self.finish_time - self.start_time
            else:
                duration = timezone.now() - self.start_time

            # Convert the duration to hours and minutes
            hours = duration // timedelta(hours=1)
            minutes = (duration % timedelta(hours=1)) // timedelta(minutes=1)

            return f"{hours} hours {minutes} minutes"

        return "0 hours 0 minutes"
    
    def all_tests_confirmed(self):
        return self.tests.filter(confirmed=False).count() == 0
    
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
        return f"{self.appointment.client.user.first_name} {self.appointment.client.user.last_name} - Analysis Requested #{self.id}"
    
    
    
class TestResult(models.Model):
    request = models.OneToOneField(AnalysisRequest, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)
    approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'test_result'
        
    def __str__(self):
        return f"Test Result #{self.id}"
        
class Report(models.Model):
    test_result = models.OneToOneField(TestResult, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100000, null=True, blank=True)
    
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
    
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    creation_time = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'invoice'
        
    def __str__(self):
        return f"Invoice #{self.id}"



