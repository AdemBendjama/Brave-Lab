from main_home.models import ComponentInformation, TestOffered

component_data = [
    (1, 'Red Blood Cell Count (RBC)', 'M/μL', 4.5, 5.5, 4, 5),
    (2, 'White Blood Cell Count (WBC)', 'cells/μL', 4300, 10800, 4300, 10800),
    (3, 'Platelet Count (PLT)', 'K/μL', 150000, 450000, 150000, 450000),
    (4, 'Hemoglobin (Hb)', 'g/dL', 13.5, 17.5, 12, 15.5),
    (5, 'Hematocrit (Hct)', '%', 38.8, 50, 34.9, 44.5),
    (6, 'Mean Corpuscular Volume (MCV)', 'fL', 80, 96, 80, 96),
    (7, 'Mean Corpuscular Hemoglobin (MCH)', 'pg', 27, 31, 27, 31),
    (8, 'Mean Corpuscular Hemoglobin Concentration (MCHC)', 'g/dL', 32, 36, 32, 36),
    (9, 'Glucose (GLU)', 'mg/dL', 70, 99, 70, 99),
    (10, 'Sodium (Na)', 'mEq/L', 135, 145, 135, 145),
    (11, 'Potassium (K)', 'mEq/L', 3.5, 5, 3.5, 5),
    (12, 'Calcium (Ca)', 'mg/dL', 8.5, 10.5, 8.5, 10.5),
    (13, 'Chloride (Cl)', 'mEq/L', 96, 106, 96, 106),
    (14, 'Carbon Dioxide (CO2)', 'mEq/L', 23, 29, 23, 29),
    (15, 'Blood Urea Nitrogen (BUN)', 'mg/dL', 7, 20, 7, 20),
    (16, 'Creatinine (Cr)', 'mg/dL', 0.6, 1.3, 0.5, 1.1),
    (17, 'Total Cholesterol (TC)', 'mg/dL', 200, 0, 200, 0),
    (18, 'High-Density Lipoprotein (HDL)', 'mg/dL', 0, 0, 0, 0),
    (19, 'Low-Density Lipoprotein (LDL)', 'mg/dL', 0, 0, 0, 0),
    (20, 'Triglyceride (TG)', 'mg/dL', 150, 0, 150, 0),
    (21, 'HbA1c', '%', 4, 6.5, 4, 6.5),
    (22, 'Vitamin D', 'ng/mL', 12, 50, 12, 50),
]

test_data = [
    (1, 'Complete Blood Count (CBC)',600),
    (2, 'Basic Metabolic Panel (BMP)',500),
    (3, 'Lipid Panel',900),
    (4, 'Hemoglobin A1C (HbA1c)',750),
    (5, 'Vitamin D Levels',700),
]

print("Inserting component Data...")

for data in component_data:
    component = ComponentInformation()
    component.id = data[0]
    component.name = data[1]
    component.unit = data[2]
    component.low_male_range = data[3]
    component.high_male_range = data[4]
    component.low_female_range = data[5]
    component.high_female_range = data[6]
    component.save()
    
print("Components Saved!")
    
print("Inserting Test names Data...")
    
for data in test_data:
    test_offered = TestOffered()
    test_offered.id = data[0]
    test_offered.name = data[1]
    test_offered.price = data[2]
    test_offered.save()

print("Test names Saved!")