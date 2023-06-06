from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
import os

from main_home.models import Appointment, Component, ComponentInformation, Lobby, Test

from django.db.models.signals import pre_save, pre_delete
from client.models import Client
from nurse.models import Nurse
from receptionist.models import Receptionist
from auditor.models import Auditor


#######   Tests 

@receiver(post_save, sender=Test)
def add_components_to_test(sender, instance, created, **kwargs):
    
    if created and instance.test_offered.name == 'Complete Blood Count (CBC)':
        
        component_names = [
            'Red Blood Cell Count (RBC)',
            'White Blood Cell Count (WBC)',
            'Platelet Count (PLT)',
            'Hemoglobin (Hb)',
            'Hematocrit (Hct)',
            'Mean Corpuscular Volume (MCV)',
            'Mean Corpuscular Hemoglobin (MCH)',
            'Mean Corpuscular Hemoglobin Concentration (MCHC)',
        ]
        components = []
        for component_name in component_names:
            component_info = ComponentInformation.objects.get(name=component_name)
            component = Component(info=component_info)
            components.append(component)
        Component.objects.bulk_create(components)
        instance.components.add(*components)
        
    if created and instance.test_offered.name == 'Basic Metabolic Panel (BMP)':
        
        component_names = [
            'Glucose (GLU)', 
            'Sodium (Na)',  
            'Potassium (K)', 
            'Calcium (Ca)', 
            'Chloride (Cl)', 
            'Carbon Dioxide (CO2)',  
            'Blood Urea Nitrogen (BUN)', 
            'Creatinine (Cr)', 
        ]
        components = []
        for component_name in component_names:
            component_info = ComponentInformation.objects.get(name=component_name)
            component = Component(info=component_info)
            components.append(component)
        Component.objects.bulk_create(components)
        instance.components.add(*components)
        
    if created and instance.test_offered.name == 'Comprehensive Metabolic Panel (CMP)':
        
        component_names = [
            'Glucose (GLU)',
            'Sodium (Na)', 
            'Potassium (K)',
            'Calcium (Ca)',
            'Chloride (Cl)',
            'Carbon Dioxide (CO2)',
            'Blood Urea Nitrogen (BUN)',
            'Creatinine (Cr)',
            'Albumin (Alb)',
            'Bilirubin (Bili)',  
            'Total Protein Level (TP)', 
            'Alkaline Phosphatase (ALP)', 
            'Alanine Aminotransferase (ALT)', 
            'Aspartate Aminotransferase (AST)',
        ]
        
        components = []
        for component_name in component_names:
            component_info = ComponentInformation.objects.get(name=component_name)
            component = Component(info=component_info)
            components.append(component)
            
        Component.objects.bulk_create(components)
        instance.components.add(*components)
        
    if created and instance.test_offered.name == 'Lipid Panel':
        
        component_names = [
            'Total Cholesterol (TC)',
            'High-Density Lipoprotein (HDL)',
            'Low-Density Lipoprotein (LDL)',
            'Triglyceride (TG)', 
        ]
        components = []
        for component_name in component_names:
            component_info = ComponentInformation.objects.get(name=component_name)
            component = Component(info=component_info)
            components.append(component)
        Component.objects.bulk_create(components)
        instance.components.add(*components)
    
    
    if created and instance.test_offered.name == 'Thyroid Function Tests':
        
        component_names = [
            'Thyroid-Stimulating Hormone (TSH)',
            'Triiodothyronine (T3)', 
            'Thyroxine (T4)', 
        ]
        components = []
        for component_name in component_names:
            component_info = ComponentInformation.objects.get(name=component_name)
            component = Component(info=component_info)
            components.append(component)
        Component.objects.bulk_create(components)
        instance.components.add(*components)
        
        
    if created and instance.test_offered.name == 'Hemoglobin A1C (HbA1c)':
        
        component_names = [
            'HbA1c', 
        ]
        components = []
        for component_name in component_names:
            component_info = ComponentInformation.objects.get(name=component_name)
            component = Component(info=component_info)
            components.append(component)
        Component.objects.bulk_create(components)
        instance.components.add(*components)
        
        
    if created and instance.test_offered.name == 'Coagulation Panel':
        
        component_names = [
            'Prothrombin Time (PT)', 
            'Partial Thromboplastin Time (PTT)', 
            'International Normalized Ratio (INR)',
        ]
        components = []
        for component_name in component_names:
            component_info = ComponentInformation.objects.get(name=component_name)
            component = Component(info=component_info)
            components.append(component)
        Component.objects.bulk_create(components)
        instance.components.add(*components)
        
        
    if created and instance.test_offered.name == 'Vitamin D Levels':
        
        component_names = [
            'Vitamin D', 
        ]
        components = []
        for component_name in component_names:
            component_info = ComponentInformation.objects.get(name=component_name)
            component = Component(info=component_info)
            components.append(component)
        Component.objects.bulk_create(components)
        instance.components.add(*components)
        
        
#######   Documents



def get_all_document_paths():
    # Retrieve all document paths from the Appointment table
    all_documents = Appointment.objects.exclude(document='').values_list('document', flat=True)
    return set(all_documents)


def delete_unused_images():
    # Get all document paths from the database
    all_documents = get_all_document_paths()

    # Get the path of the directory where the images are stored
    image_directory = 'medical_documents/'

    # Get a list of all files in the image directory
    all_files = default_storage.listdir(image_directory)[1]

    # Loop through each file in the directory
    for file_name in all_files:
        file_path = os.path.join(image_directory, file_name)

        # Check if the file path does not exist in the database documents
        if file_path not in all_documents:
            # Delete the file
            default_storage.delete(file_path)


@receiver(post_save, sender=Appointment)
@receiver(post_delete, sender=Appointment)
def handle_appointment_change(sender, instance, **kwargs):
    delete_unused_images()
    
    
######## Profile pictures

def get_all_profile_pic_paths():
    # Retrieve all profile picture paths from the user models
    all_profile_pics = (
        list(Client.objects.exclude(profile_pic='').values_list('profile_pic', flat=True)) +
        list(Nurse.objects.exclude(profile_pic='').values_list('profile_pic', flat=True)) +
        list(Receptionist.objects.exclude(profile_pic='').values_list('profile_pic', flat=True)) +
        list(Auditor.objects.exclude(profile_pic='').values_list('profile_pic', flat=True))
    )
    return set(all_profile_pics)


def delete_unused_profile_pics():
    # Get all profile picture paths from the database
    all_profile_pics = get_all_profile_pic_paths()

    # Get the path of the directory where the profile pictures are stored
    profile_pic_directory = 'profile_pics/'

    # Get a list of all files in the profile picture directory
    all_files = default_storage.listdir(profile_pic_directory)[1]

    # Loop through each file in the directory
    for file_name in all_files:
        file_path = os.path.join(profile_pic_directory, file_name)

        # Check if the file path does not exist in the database profile pictures
        if file_path not in all_profile_pics:
            # Delete the file
            default_storage.delete(file_path)


@receiver(pre_save, sender=Client)
@receiver(pre_save, sender=Nurse)
@receiver(pre_save, sender=Receptionist)
@receiver(pre_save, sender=Auditor)
def handle_user_profile_pic_change(sender, instance, **kwargs):
    if sender.objects.filter(pk=instance.pk).exists() :
        # Retrieve the existing profile picture path
        old_profile_pic_path = sender.objects.get(pk=instance.pk).profile_pic.path
        old_profile_pic = sender.objects.get(pk=instance.pk).profile_pic

        # Check if the existing profile picture is different from the new profile picture
        if old_profile_pic_path != instance.profile_pic.path and old_profile_pic != "default.png" :
            # Delete the old profile picture
            default_storage.delete(old_profile_pic_path)


@receiver(pre_delete, sender=Client)
@receiver(pre_delete, sender=Nurse)
@receiver(pre_delete, sender=Receptionist)
@receiver(pre_delete, sender=Auditor)
def handle_user_profile_pic_deletion(sender, instance, **kwargs):
    # Delete the profile picture when a user is deleted
    profile_pic_path = instance.profile_pic.path
    profile_pic = instance.profile_pic
    if profile_pic != "default.png" :
        default_storage.delete(profile_pic_path)

    # Delete unused profile pictures
    delete_unused_profile_pics()


# Nurse Lobby
@receiver(post_save, sender=Nurse)
def create_nurse_lobby(sender, instance, created, **kwargs):
    if created:
        lobby = Lobby.objects.create(nurse=instance)
        print(lobby.clients)
        
@receiver(pre_delete, sender=Nurse)
def delete_nurse_lobby(sender, instance, **kwargs):
    if instance.lobby:
        instance.lobby.delete()
