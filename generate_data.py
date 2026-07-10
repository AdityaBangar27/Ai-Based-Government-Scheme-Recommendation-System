import os
import random
import csv
import pandas as pd
import numpy as np

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Helper lists for User Generation
first_names_male = [
    "Aarav", "Vihaan", "Vivaan", "Arjun", "Sai", "Aditya", "Krishna", "Aryan", "Shaurya", "Kabir",
    "Ishaan", "Dhruv", "Atharva", "Ansh", "Dev", "Rahul", "Amit", "Rajesh", "Sanjay", "Anil",
    "Sunil", "Ramesh", "Dinesh", "Suresh", "Vijay", "Ajay", "Vikram", "Rohit", "Sandeep", "Deepak",
    "Manoj", "Pranav", "Harish", "Alok", "Pankaj", "Rakesh", "Karan", "Gaurav", "Yash", "Abhishek"
]

first_names_female = [
    "Diya", "Isha", "Ananya", "Aanya", "Aadhya", "Saanvi", "Prisha", "Aaradhya", "Anika", "Kavya",
    "Riya", "Neha", "Priya", "Sunita", "Anita", "Geeta", "Babita", "Rekha", "Pooja", "Jyoti",
    "Deepa", "Meena", "Radha", "Swati", "Shweta", "Aarti", "Preeti", "Divya", "Anjali", "Sneha",
    "Komal", "Priyanka", "Rashmi", "Poonam", "Kiran", "Sapna", "Sheetal", "Kirti", "Nisha", "Mamta"
]

last_names = [
    "Kumar", "Sharma", "Singh", "Verma", "Gupta", "Patel", "Yadav", "Reddy", "Nair", "Joshi",
    "Rao", "Mehta", "Das", "Banerjee", "Chatterjee", "Sen", "Kulkarni", "Deshmukh", "Patil", "Shah",
    "Gandhi", "Mishra", "Tiwari", "Chaudhary", "Prasad", "Gowda", "Bhat", "Iyer", "Pillai", "Gill",
    "Shinde", "More", "Sinha", "Dubey", "Pandey", "Saxena", "Soni", "Jha", "Mukherjee", "Nair"
]

states_districts = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad", "Solapur", "Amravati"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Prayagraj", "Meerut", "Bareilly", "Aligarh"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Trichy", "Salem", "Tirunelveli", "Vellore", "Erode"],
    "Karnataka": ["Bengaluru", "Mysore", "Hubli", "Mangalore", "Belgaum", "Dharwad", "Davangere", "Bellary"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Darbhanga", "Purnia", "Ara", "Begusarai"],
    "West Bengal": ["Kolkata", "Howrah", "Darjeeling", "Asansol", "Siliguri", "Durgapur", "Kharagpur", "Malda"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer", "Bikaner", "Alwar", "Sikar"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Gandhinagar", "Bhavnagar", "Jamnagar", "Junagadh"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Dewas", "Satna"],
    "Kerala": ["Trivandrum", "Kochi", "Kozhikode", "Thrissur", "Kollam", "Alappuzha", "Palakkad", "Kannur"],
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Tirupati", "Kakinada", "Kurnool", "Rajahmundry"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Hoshiarpur", "Pathankot", "Moga"]
}

def generate_users_csv(filename="users.csv", count=1500):
    """Generates a realistic, correlated user dataset of 1,500 records."""
    users = []
    
    for i in range(1, count + 1):
        user_id = f"USR{i:04d}"
        
        # Gender Selection
        gender = "Male" if i % 2 == 0 else "Female"
        
        # Name Selection based on Gender
        first_name = random.choice(first_names_male) if gender == "Male" else random.choice(first_names_female)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        
        # Age Selection (18 to 80)
        # Using a distribution where working age is more common
        age = int(np.clip(np.random.normal(40, 15), 18, 80))
        
        # State and District Selection
        state = list(states_districts.keys())[i % len(states_districts)]
        district = random.choice(states_districts[state])
        
        # Occupation & Student/Farmer/Employment Status
        occupation = "Unemployed"
        employment_status = "Unemployed"
        student_status = "No"
        farmer_status = "No"
        
        if age <= 24:
            # High probability of being a student
            if random.random() < 0.75:
                occupation = "Student"
                employment_status = "Student"
                student_status = "Yes"
            else:
                occupation = random.choice(["Laborer", "Private Employee", "Unemployed"])
                employment_status = "Unemployed" if occupation == "Unemployed" else "Employed"
        elif age >= 60:
            # High probability of being retired
            if random.random() < 0.80:
                occupation = "Retired"
                employment_status = "Retired"
            else:
                occupation = random.choice(["Farmer", "Business Owner", "Unemployed"])
                employment_status = "Self-Employed" if occupation in ["Farmer", "Business Owner"] else "Unemployed"
                if occupation == "Farmer":
                    farmer_status = "Yes"
        else:
            # Working age group
            rand_val = random.random()
            if rand_val < 0.25:
                occupation = "Farmer"
                employment_status = "Self-Employed"
                farmer_status = "Yes"
            elif rand_val < 0.45:
                occupation = "Private Employee"
                employment_status = "Employed"
            elif rand_val < 0.60:
                occupation = "Business Owner"
                employment_status = "Self-Employed"
            elif rand_val < 0.75:
                occupation = "Laborer"
                employment_status = "Employed" if random.random() < 0.8 else "Self-Employed"
            elif rand_val < 0.85:
                occupation = "Government Employee"
                employment_status = "Employed"
            else:
                occupation = "Unemployed"
                employment_status = "Unemployed"
        
        # Education Levels
        education_opts = ["Illiterate", "Primary", "10th", "12th", "Graduate", "Post Graduate"]
        if occupation == "Student":
            if age < 19:
                education = "10th"
            elif age < 22:
                education = "12th"
            else:
                education = "Graduate"
        elif occupation == "Government Employee":
            education = random.choice(["Graduate", "Post Graduate"])
        elif occupation == "Private Employee":
            education = random.choice(["12th", "Graduate", "Post Graduate"])
        elif occupation == "Farmer" or occupation == "Laborer":
            education = random.choice(["Illiterate", "Primary", "10th", "12th"])
        else:
            education = random.choice(education_opts)
            
        # Income & Annual Family Income (correlated with occupation)
        income = 0
        annual_family_income = 0
        
        if occupation == "Student":
            income = 0
            # Family income support
            annual_family_income = random.randint(90000, 800000)
        elif occupation == "Unemployed":
            income = 0
            # Family income support
            annual_family_income = random.randint(50000, 200000)
        elif occupation == "Farmer":
            income = random.randint(4000, 15000) # Monthly individual income
            annual_family_income = 12 * income + random.randint(10000, 50000)
        elif occupation == "Laborer":
            income = random.randint(6000, 12000)
            annual_family_income = 12 * income + random.randint(5000, 20000)
        elif occupation == "Business Owner":
            income = random.randint(15000, 90000)
            annual_family_income = 12 * income + random.randint(50000, 300000)
        elif occupation == "Government Employee":
            income = random.randint(35000, 120000)
            annual_family_income = 12 * income + random.randint(30000, 150000)
        elif occupation == "Private Employee":
            income = random.randint(15000, 110000)
            annual_family_income = 12 * income + random.randint(20000, 200000)
        elif occupation == "Retired":
            income = random.randint(5000, 25000) # Pension
            annual_family_income = 12 * income + random.randint(10000, 40000)
            
        # Category (General/OBC/SC/ST/EWS)
        # EWS is General category but with family income < 8,000,000 (usually < 8 Lakhs)
        category_opts = ["General", "OBC", "SC", "ST"]
        category = random.choices(category_opts, weights=[0.30, 0.40, 0.18, 0.12])[0]
        if category == "General" and annual_family_income < 800000:
            # Let's say a portion of eligible General category are EWS
            if random.random() < 0.4:
                category = "EWS"
                
        # Disability Status (Yes/No)
        disability_status = "Yes" if random.random() < 0.08 else "No"
        
        # Rural / Urban
        if occupation == "Farmer":
            rural_urban = "Rural" if random.random() < 0.95 else "Urban"
        else:
            rural_urban = "Rural" if random.random() < 0.55 else "Urban"
            
        # BPL Status (Below Poverty Line)
        # Threshold: if annual family income is low
        if rural_urban == "Rural" and annual_family_income < 100000:
            bpl_status = "Yes" if random.random() < 0.90 else "No"
        elif rural_urban == "Urban" and annual_family_income < 120000:
            bpl_status = "Yes" if random.random() < 0.90 else "No"
        else:
            bpl_status = "No"
            
        # Minority Status (Yes/No)
        minority_status = "Yes" if random.random() < 0.18 else "No"
        
        # Marital Status
        if age <= 23:
            marital_status = "Single" if random.random() < 0.92 else "Married"
        elif age >= 65:
            marital_status = "Widowed" if random.random() < 0.35 else "Married"
        else:
            marital_status = "Married" if random.random() < 0.85 else random.choice(["Single", "Divorced"])
            
        users.append({
            "User_ID": user_id,
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Income": income,
            "Annual_Family_Income": annual_family_income,
            "State": state,
            "District": district,
            "Education": education,
            "Occupation": occupation,
            "Category": category,
            "Disability_Status": disability_status,
            "Rural_Urban": rural_urban,
            "Employment_Status": employment_status,
            "Marital_Status": marital_status,
            "Farmer_Status": farmer_status,
            "Student_Status": student_status,
            "BPL_Status": bpl_status,
            "Minority_Status": minority_status
        })
        
    df = pd.DataFrame(users)
    df.to_csv(filename, index=False)
    print(f"Generated {count} user records in {filename}")

def generate_schemes_csv(filename="schemes.csv"):
    """Generates exactly 100 government scheme records covering diverse criteria."""
    
    # We will hand-craft/generate a list of 100 realistic schemes
    schemes_data = [
        # Farmer Schemes (1-12)
        {
            "Scheme_Name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
            "Beneficiary": "Farmers",
            "Description": "Central government scheme providing income support of Rs. 6,000 per year in three equal installments to all landholding farmer families.",
            "Min_Age": 18, "Max_Age": 80, "Income_Limit": 999999999, "State": "All", "Gender": "All",
            "Education": "All", "Occupation": "Farmer", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "Rural", "Employment_Status": "Self-Employed", "Marital_Status": "All",
            "Farmer_Status": "Yes", "Student_Status": "No", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Financial benefit of Rs. 6000 per annum paid directly to bank accounts.",
            "Required_Documents": "Aadhaar Card, Land Ownership Papers, Bank Account Details",
            "Official_Website": "https://pmkisan.gov.in"
        },
        {
            "Scheme_Name": "PM Krishi Sinchayee Yojana (PMKSY)",
            "Beneficiary": "Farmers",
            "Description": "Focuses on creating sources of assured irrigation and promoting water conservation practices under More Crop Per Drop.",
            "Min_Age": 18, "Max_Age": 80, "Income_Limit": 999999999, "State": "All", "Gender": "All",
            "Education": "All", "Occupation": "Farmer", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "Rural", "Employment_Status": "Self-Employed", "Marital_Status": "All",
            "Farmer_Status": "Yes", "Student_Status": "No", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Subsidies for micro-irrigation systems (drip and sprinkler) up to 55%.",
            "Required_Documents": "Aadhaar Card, Land Cultivation Proof, Bank Passbook, Address Proof",
            "Official_Website": "https://pmksy.gov.in"
        },
        {
            "Scheme_Name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
            "Beneficiary": "Farmers",
            "Description": "Crop insurance scheme offering financial support to farmers suffering crop loss/damage due to natural calamities, pests & diseases.",
            "Min_Age": 18, "Max_Age": 80, "Income_Limit": 999999999, "State": "All", "Gender": "All",
            "Education": "All", "Occupation": "Farmer", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "Self-Employed", "Marital_Status": "All",
            "Farmer_Status": "Yes", "Student_Status": "No", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Low premium rate insurance coverage for all food, oilseeds and horticultural crops.",
            "Required_Documents": "Aadhaar, Land Records, Sowing Certificate, Bank Account Details",
            "Official_Website": "https://pmfby.gov.in"
        },
        {
            "Scheme_Name": "Kisan Credit Card (KCC) Scheme",
            "Beneficiary": "Farmers",
            "Description": "Provides farmers with timely access to credit for their cultivation and other needs including agriculture machinery.",
            "Min_Age": 18, "Max_Age": 75, "Income_Limit": 999999999, "State": "All", "Gender": "All",
            "Education": "All", "Occupation": "Farmer", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "Self-Employed", "Marital_Status": "All",
            "Farmer_Status": "Yes", "Student_Status": "No", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Short term credit limit up to Rs. 3 Lakh at low interest rates (4%).",
            "Required_Documents": "Land Possession Document, Aadhaar Card, PAN Card, Passport Photograph",
            "Official_Website": "https://www.sbi.co.in/web/personal-banking/loans/agriculture-loans/kisan-credit-card"
        },
        {
            "Scheme_Name": "PM Kisan Maan-Dhan Yojana (PM-KMY)",
            "Beneficiary": "Farmers",
            "Description": "Old age pension scheme for small and marginal landholding farmers to ensure post-retirement social security.",
            "Min_Age": 18, "Max_Age": 40, "Income_Limit": 999999999, "State": "All", "Gender": "All",
            "Education": "All", "Occupation": "Farmer", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "Rural", "Employment_Status": "Self-Employed", "Marital_Status": "All",
            "Farmer_Status": "Yes", "Student_Status": "No", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Assured monthly pension of Rs. 3000 upon reaching the age of 60.",
            "Required_Documents": "Aadhaar Card, Bank Account details, Land cultivation certificate",
            "Official_Website": "https://pmkmy.gov.in"
        },
        # Student & Education Schemes (13-25)
        {
            "Scheme_Name": "Post Matric Scholarship Scheme for SC Students",
            "Beneficiary": "SC Students",
            "Description": "Provides financial assistance to students belonging to Scheduled Castes for pursuing post-matriculation or post-secondary courses.",
            "Min_Age": 18, "Max_Age": 30, "Income_Limit": 250000, "State": "All", "Gender": "All",
            "Education": "10th", "Occupation": "Student", "Category": "SC", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "Student", "Marital_Status": "All",
            "Farmer_Status": "No", "Student_Status": "Yes", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "100% tuition fee waiver and monthly maintenance allowance.",
            "Required_Documents": "Caste Certificate, Income Certificate, Fee Receipt, Academic Marksheets",
            "Official_Website": "https://scholarships.gov.in"
        },
        {
            "Scheme_Name": "Post Matric Scholarship Scheme for OBC Students",
            "Beneficiary": "OBC Students",
            "Description": "Financial support program enabling students of Other Backward Classes to pursue secondary and higher education.",
            "Min_Age": 18, "Max_Age": 30, "Income_Limit": 150000, "State": "All", "Gender": "All",
            "Education": "10th", "Occupation": "Student", "Category": "OBC", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "Student", "Marital_Status": "All",
            "Farmer_Status": "No", "Student_Status": "Yes", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Partial reimbursement of tuition fees and monthly academic maintenance allowance.",
            "Required_Documents": "OBC Caste Certificate, Income Certificate, Previous Academic Marksheet, Aadhaar",
            "Official_Website": "https://scholarships.gov.in"
        },
        {
            "Scheme_Name": "Central Sector Scheme of Scholarship for College and University Students",
            "Beneficiary": "Meritorious Students",
            "Description": "Provides financial aid to meritorious students from non-wealthy families to meet a part of their day-to-day expenses while pursuing higher studies.",
            "Min_Age": 18, "Max_Age": 25, "Income_Limit": 450000, "State": "All", "Gender": "All",
            "Education": "12th", "Occupation": "Student", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "Student", "Marital_Status": "All",
            "Farmer_Status": "No", "Student_Status": "Yes", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Scholarship of Rs. 12000 per annum for graduation and Rs. 20000 for post graduation.",
            "Required_Documents": "Class 12 Marksheet, Aadhaar Card, Income Certificate, College Admission Proof",
            "Official_Website": "https://scholarships.gov.in"
        },
        {
            "Scheme_Name": "Pragati Scholarship Scheme for Girls",
            "Beneficiary": "Female Technical Students",
            "Description": "AICTE scheme providing financial assistance to female students to encourage and support technical education.",
            "Min_Age": 18, "Max_Age": 25, "Income_Limit": 800000, "State": "All", "Gender": "Female",
            "Education": "12th", "Occupation": "Student", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "Student", "Marital_Status": "All",
            "Farmer_Status": "No", "Student_Status": "Yes", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Rs. 50,000 per annum as tuition fee reimbursement and incidentals.",
            "Required_Documents": "College Fee Receipt, Aadhaar, Income Certificate, Caste Certificate (if applicable)",
            "Official_Website": "https://www.aicte-india.org"
        },
        # Women Empowerment Schemes (26-38)
        {
            "Scheme_Name": "Pradhan Mantri Matru Vandana Yojana (PMMVY)",
            "Beneficiary": "Pregnant & Lactating Women",
            "Description": "Maternity benefit program providing cash incentives for pregnant and lactating mothers for improved health and nutrition.",
            "Min_Age": 19, "Max_Age": 45, "Income_Limit": 999999999, "State": "All", "Gender": "Female",
            "Education": "All", "Occupation": "All", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "All", "Marital_Status": "Married",
            "Farmer_Status": "All", "Student_Status": "All", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Direct cash transfer of Rs. 5000 in three installments upon complying with vaccine milestones.",
            "Required_Documents": "Mother and Child Protection (MCP) card, Aadhaar, Bank Account details",
            "Official_Website": "https://wcd.nic.in"
        },
        {
            "Scheme_Name": "Mahila Co-operative Loan Scheme",
            "Beneficiary": "Women Entrepreneurs",
            "Description": "Financial assistance program providing concessional loans to women looking to start cooperative businesses.",
            "Min_Age": 18, "Max_Age": 65, "Income_Limit": 500000, "State": "All", "Gender": "Female",
            "Education": "Primary", "Occupation": "Business Owner", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "Self-Employed", "Marital_Status": "All",
            "Farmer_Status": "All", "Student_Status": "No", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Loans up to Rs. 2 Lakhs at extremely low interest rates (3-5%).",
            "Required_Documents": "Aadhaar Card, Co-operative registration, Income Certificate, Project Proposal",
            "Official_Website": "https://www.nabard.org"
        },
        {
            "Scheme_Name": "PMMVY-Urban (Maternity Benefit Scheme for Urban Poor)",
            "Beneficiary": "Urban Poor Pregnant Women",
            "Description": "Maternity support specifically targeted towards women in urban slum or low-income settings.",
            "Min_Age": 19, "Max_Age": 45, "Income_Limit": 150000, "State": "All", "Gender": "Female",
            "Education": "All", "Occupation": "All", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "Urban", "Employment_Status": "All", "Marital_Status": "Married",
            "Farmer_Status": "All", "Student_Status": "All", "BPL_Status": "Yes", "Minority_Status": "All",
            "Benefits": "Maternity cash incentive of Rs. 5000 and nutritional supplements.",
            "Required_Documents": "BPL Card, Aadhaar Card, MCP Card, Bank details",
            "Official_Website": "https://wcd.nic.in"
        },
        # Senior Citizen Schemes (39-50)
        {
            "Scheme_Name": "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)",
            "Beneficiary": "BPL Senior Citizens",
            "Description": "Provides monthly pension to senior citizens belonging to households below the poverty line.",
            "Min_Age": 60, "Max_Age": 80, "Income_Limit": 100000, "State": "All", "Gender": "All",
            "Education": "All", "Occupation": "Retired", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "Retired", "Marital_Status": "All",
            "Farmer_Status": "No", "Student_Status": "No", "BPL_Status": "Yes", "Minority_Status": "All",
            "Benefits": "Monthly pension of Rs. 200 (age 60-79) and Rs. 500 (age 80+). States often top this up.",
            "Required_Documents": "Aadhaar Card, BPL Card, Age Proof (Birth Certificate/Voter ID), Bank Passbook",
            "Official_Website": "https://nsap.nic.in"
        },
        {
            "Scheme_Name": "Pradhan Mantri Vaya Vandana Yojana (PMVVY)",
            "Beneficiary": "Senior Citizens",
            "Description": "Pension scheme for senior citizens offering guaranteed rate of return on purchase price, managed by LIC.",
            "Min_Age": 60, "Max_Age": 80, "Income_Limit": 999999999, "State": "All", "Gender": "All",
            "Education": "All", "Occupation": "Retired", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "Retired", "Marital_Status": "All",
            "Farmer_Status": "No", "Student_Status": "No", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Guaranteed return of 7.4% per annum paid monthly as pension for 10 years.",
            "Required_Documents": "Aadhaar, Address Proof, PAN Card, Age Proof, Bank Account Copy",
            "Official_Website": "https://licindia.in"
        },
        # Disability Schemes (51-60)
        {
            "Scheme_Name": "Indira Gandhi National Disability Pension Scheme (IGNDPS)",
            "Beneficiary": "Disabled Persons",
            "Description": "Pensions for persons with severe or multiple disabilities who are living below the poverty line.",
            "Min_Age": 18, "Max_Age": 79, "Income_Limit": 120000, "State": "All", "Gender": "All",
            "Education": "All", "Occupation": "All", "Category": "All", "Disability_Status": "Yes",
            "Rural_Urban": "All", "Employment_Status": "All", "Marital_Status": "All",
            "Farmer_Status": "All", "Student_Status": "All", "BPL_Status": "Yes", "Minority_Status": "All",
            "Benefits": "Monthly financial pension of Rs. 300 per month.",
            "Required_Documents": "Disability Certificate (min 80%), BPL Card, Aadhaar Card, Bank details",
            "Official_Website": "https://nsap.nic.in"
        },
        {
            "Scheme_Name": "Deendayal Disabled Rehabilitation Scheme (DDRS)",
            "Beneficiary": "Persons with Disabilities",
            "Description": "Financial assistance for rehabilitation services, special schools, and vocational training centers for disabled individuals.",
            "Min_Age": 18, "Max_Age": 60, "Income_Limit": 999999999, "State": "All", "Gender": "All",
            "Education": "All", "Occupation": "All", "Category": "All", "Disability_Status": "Yes",
            "Rural_Urban": "All", "Employment_Status": "All", "Marital_Status": "All",
            "Farmer_Status": "All", "Student_Status": "All", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Free education, rehabilitation therapy, vocational training, and helper support.",
            "Required_Documents": "Disability Certificate, Aadhaar Card, Resident Proof, Family Income Proof",
            "Official_Website": "https://disabilityaffairs.gov.in"
        },
        # Entrepreneurship & Business Schemes (61-70)
        {
            "Scheme_Name": "Pradhan Mantri Mudra Yojana (PMMY) - Shishu",
            "Beneficiary": "Micro Entrepreneurs",
            "Description": "Provides loans to non-corporate, non-farm small/micro enterprises to encourage self-employment.",
            "Min_Age": 18, "Max_Age": 65, "Income_Limit": 999999999, "State": "All", "Gender": "All",
            "Education": "All", "Occupation": "Business Owner", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "Self-Employed", "Marital_Status": "All",
            "Farmer_Status": "No", "Student_Status": "No", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Collateral-free business loans up to Rs. 50,000.",
            "Required_Documents": "Business Registration Proof, Aadhaar Card, Address Proof, Photos",
            "Official_Website": "https://www.mudra.org.in"
        },
        {
            "Scheme_Name": "Stand-Up India Scheme",
            "Beneficiary": "SC, ST or Women Entrepreneurs",
            "Description": "Promotes entrepreneurship among women and SC/ST communities by helping them start greenfield enterprises.",
            "Min_Age": 18, "Max_Age": 70, "Income_Limit": 999999999, "State": "All", "Gender": "All",  # Handled by logic check
            "Education": "10th", "Occupation": "Business Owner", "Category": "All", "Disability_Status": "All", # SC/ST or Female
            "Rural_Urban": "All", "Employment_Status": "Self-Employed", "Marital_Status": "All",
            "Farmer_Status": "No", "Student_Status": "No", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Bank loans between Rs. 10 Lakh and Rs. 1 Crore for greenfield projects.",
            "Required_Documents": "Caste Certificate (for SC/ST), Business Plan, Rent Agreement, ID Proof",
            "Official_Website": "https://www.standupmitra.in"
        },
        # EWS & Low Income Schemes (71-80)
        {
            "Scheme_Name": "PM Garib Kalyan Anna Yojana (PMGKAY)",
            "Beneficiary": "BPL and Poor Families",
            "Description": "Food security welfare scheme providing free foodgrains to eligible beneficiaries under National Food Security Act.",
            "Min_Age": 18, "Max_Age": 80, "Income_Limit": 150000, "State": "All", "Gender": "All",
            "Education": "All", "Occupation": "All", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "All", "Marital_Status": "All",
            "Farmer_Status": "All", "Student_Status": "All", "BPL_Status": "Yes", "Minority_Status": "All",
            "Benefits": "5kg of foodgrains (wheat or rice) per person per month, free of cost.",
            "Required_Documents": "Ration Card (NFSA), Aadhaar Card, Income Certificate",
            "Official_Website": "https://dfpd.gov.in"
        },
        {
            "Scheme_Name": "Pradhan Mantri Awas Yojana - Gramin (PMAY-G)",
            "Beneficiary": "Rural Poor",
            "Description": "Assists rural BPL families and homeless citizens in constructing permanent, safe houses.",
            "Min_Age": 18, "Max_Age": 80, "Income_Limit": 200000, "State": "All", "Gender": "All",
            "Education": "All", "Occupation": "All", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "Rural", "Employment_Status": "All", "Marital_Status": "All",
            "Farmer_Status": "All", "Student_Status": "All", "BPL_Status": "Yes", "Minority_Status": "All",
            "Benefits": "Financial assistance of Rs. 1.2 Lakh (plains) / Rs. 1.3 Lakh (hilly areas) for home building.",
            "Required_Documents": "Aadhaar Card, BPL Card, Bank Account, Land NOC, Income Certificate",
            "Official_Website": "https://pmayg.nic.in"
        },
        # Minority & Welfare Schemes (81-90)
        {
            "Scheme_Name": "Naya Savera - Free Coaching Scheme for Minorities",
            "Beneficiary": "Minority Students",
            "Description": "Assists students belonging to minority communities to prepare for competitive examinations.",
            "Min_Age": 18, "Max_Age": 28, "Income_Limit": 600000, "State": "All", "Gender": "All",
            "Education": "12th", "Occupation": "Student", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "Student", "Marital_Status": "All",
            "Farmer_Status": "No", "Student_Status": "Yes", "BPL_Status": "All", "Minority_Status": "Yes",
            "Benefits": "Free coaching program fees for competitive exams like UPSC, NEET, JEE.",
            "Required_Documents": "Minority Community Certificate, Income Proof, Admission Card, Class 10/12 marksheets",
            "Official_Website": "https://www.minorityaffairs.gov.in"
        },
        {
            "Scheme_Name": "Maulana Azad National Fellowship for Minorities",
            "Beneficiary": "Minority Scholars",
            "Description": "Fellowship scheme providing financial support to minority students pursuing higher education (M.Phil / Ph.D).",
            "Min_Age": 21, "Max_Age": 35, "Income_Limit": 600000, "State": "All", "Gender": "All",
            "Education": "Graduate", "Occupation": "Student", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "Student", "Marital_Status": "All",
            "Farmer_Status": "No", "Student_Status": "Yes", "BPL_Status": "All", "Minority_Status": "Yes",
            "Benefits": "Monthly fellowship stipend of Rs. 31000 - 35000.",
            "Required_Documents": "Post-Graduation Marks Certificate, Minority Certificate, Family Income Proof, University Enrollment Proof",
            "Official_Website": "https://www.ugc.ac.in"
        },
        # State Specific Schemes (91-100)
        {
            "Scheme_Name": "Sanjay Gandhi Niradhar Anudan Yojana (Maharashtra)",
            "Beneficiary": "Destitute & Widowed Women in Maharashtra",
            "Description": "Maharashtra state scheme providing monthly financial aid to destitute, blind, disabled, and widowed women.",
            "Min_Age": 18, "Max_Age": 65, "Income_Limit": 21000, "State": "Maharashtra", "Gender": "Female",
            "Education": "All", "Occupation": "All", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "Unemployed", "Marital_Status": "Widowed",
            "Farmer_Status": "All", "Student_Status": "No", "BPL_Status": "Yes", "Minority_Status": "All",
            "Benefits": "Financial pension of Rs. 1000 per month.",
            "Required_Documents": "Age Proof, Income Proof, Maharashtra Residence Certificate, Widowed Certificate",
            "Official_Website": "https://sanjaygandhiniradhar.maharashtra.gov.in"
        },
        {
            "Scheme_Name": "Kanya Sumangala Yojana (Uttar Pradesh)",
            "Beneficiary": "Girl Children in UP",
            "Description": "Uttar Pradesh scheme aiming to improve the health and educational status of girls through cash benefits.",
            "Min_Age": 18, "Max_Age": 25, "Income_Limit": 300000, "State": "Uttar Pradesh", "Gender": "Female",
            "Education": "10th", "Occupation": "Student", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "All", "Employment_Status": "Student", "Marital_Status": "Single",
            "Farmer_Status": "No", "Student_Status": "Yes", "BPL_Status": "All", "Minority_Status": "All",
            "Benefits": "Monetary support of Rs. 15,000 paid in phases for education.",
            "Required_Documents": "UP Domicile Proof, Family Income Certificate, Aadhaar Card, Passport Photo",
            "Official_Website": "https://mksy.up.gov.in"
        },
        {
            "Scheme_Name": "Mo Ghara Yojana (Odisha Housing Scheme)",
            "Beneficiary": "Rural Poor in Odisha",
            "Description": "Odisha state government scheme designed to support lower-income and lower-middle-income rural households in rebuilding houses.",
            "Min_Age": 18, "Max_Age": 80, "Income_Limit": 300000, "State": "All", "Gender": "All", # Set State to All but in description Odisha
            "Education": "All", "Occupation": "All", "Category": "All", "Disability_Status": "All",
            "Rural_Urban": "Rural", "Employment_Status": "All", "Marital_Status": "All",
            "Farmer_Status": "All", "Student_Status": "All", "BPL_Status": "Yes", "Minority_Status": "All",
            "Benefits": "Home construction bank loan capital subsidy up to Rs. 60,000.",
            "Required_Documents": "Income Proof, Aadhaar Card, Land Record Copy, Bank Passbook",
            "Official_Website": "https://rhodisha.gov.in/mo-ghara"
        }
    ]
    
    # We will generate up to 100 schemes by modifying elements of our templates
    # and ensuring all categories from the prompt are represented:
    # Central Government, State Government, Women, Farmer, Student, Senior citizen,
    # Disability, Entrepreneurship, Education, Employment, Housing, Healthcare schemes.
    
    # Base lists to construct remaining schemes dynamically to get to exactly 100
    sectors = ["Agriculture", "Education", "Healthcare", "Women Empowerment", "Senior Citizens", "Welfare", "Housing", "Skills Development"]
    states_list = list(states_districts.keys())
    
    current_schemes = list(schemes_data)
    
    # Generate remaining schemes up to 100
    id_counter = len(current_schemes) + 1
    
    while len(current_schemes) < 100:
        sector = random.choice(sectors)
        st = random.choice(states_list) if random.random() < 0.3 else "All"
        gen = "Female" if sector == "Women Empowerment" else ("Male" if random.random() < 0.05 else "All")
        
        # Standard settings
        min_age = 18
        max_age = 80
        inc_lim = 999999999
        occ = "All"
        edu = "All"
        cat = "All"
        dis = "All"
        r_u = "All"
        emp = "All"
        marital = "All"
        farmer = "All"
        student = "All"
        bpl = "All"
        minority = "All"
        
        if sector == "Agriculture":
            name = f"National Farmer Scheme - Phase {id_counter}"
            desc = f"Government initiative to support agricultural development by giving modern irrigation kits and equipment to farmers."
            occ = "Farmer"
            farmer = "Yes"
            r_u = "Rural"
            emp = "Self-Employed"
            benefits = "Free drip irrigation kit and Rs. 5000 subsidy on fertilizers."
            docs = "Aadhaar Card, Land Records, Farmer ID Proof"
            web = f"https://agricoop.nic.in/scheme{id_counter}"
        elif sector == "Education":
            name = f"Merit-cum-Means Post Matric Support - Program {id_counter}"
            desc = f"Financial backing for brilliant students to guarantee access to professional training colleges and technical degrees."
            occ = "Student"
            student = "Yes"
            emp = "Student"
            max_age = 28
            inc_lim = random.choice([200000, 300000, 500000])
            edu = random.choice(["10th", "12th"])
            benefits = "Full academic tuition coverage and a monthly stipend of Rs. 1500."
            docs = "Academic transcript, Income certificate, Fee Structure, Aadhaar"
            web = f"https://scholarships.gov.in/scheme{id_counter}"
        elif sector == "Women Empowerment":
            name = f"Mahila Self-Reliance Scheme - Model {id_counter}"
            desc = f"Encouraging small enterprise setup for women by organizing self-help groups and funding micro-manufacturing setups."
            gen = "Female"
            occ = "Business Owner"
            emp = "Self-Employed"
            inc_lim = 300000
            benefits = "Subsidized startup loan of up to Rs. 1,00,000 without collateral."
            docs = "Aadhaar Card, Residence proof, Self-Help Group certificate"
            web = f"https://wcd.nic.in/scheme{id_counter}"
        elif sector == "Senior Citizens":
            name = f"Senior Citizen Financial Security - Pension {id_counter}"
            desc = f"An annuity and healthcare insurance combination plan for senior citizens designed for a comfortable retired life."
            min_age = 60
            emp = "Retired"
            occ = "Retired"
            benefits = "Guaranteed Rs. 2000 monthly pension and secondary medical coverage up to Rs. 1 Lakh."
            docs = "Age Certificate, Aadhaar, Bank Details, Income proof"
            web = f"https://nsap.nic.in/pension{id_counter}"
        elif sector == "Healthcare":
            name = f"Ayushman Swasthya Suraksha - Yojana {id_counter}"
            desc = f"National health insurance coverage for economically vulnerable populations enabling free hospitalization at registered clinics."
            bpl = "Yes"
            inc_lim = 120000
            benefits = "Cashless medical insurance coverage of up to Rs. 5,000,000 per family per year."
            docs = "BPL Card, Aadhaar Card, Ration Card"
            web = f"https://pmjay.gov.in/swasthya{id_counter}"
        elif sector == "Housing":
            name = f"Awas Sahayata Gramin - Allocation {id_counter}"
            desc = f"Providing masonry training and raw building materials to rural households below the poverty line to build permanent homes."
            bpl = "Yes"
            r_u = "Rural"
            benefits = "Financial assistance of Rs. 1,20,000 along with subsidised building supplies."
            docs = "BPL Certificate, Land ownership map, Aadhaar Card"
            web = f"https://pmayg.nic.in/housing{id_counter}"
        elif sector == "Skills Development":
            name = f"Skill Upgradation and Vocational Loan - Plan {id_counter}"
            desc = f"Short-term industry courses and certification for unemployed youth to improve immediate placement prospects."
            emp = "Unemployed"
            occ = "Unemployed"
            max_age = 35
            benefits = "Free skill training course and job placement assistance with stipend."
            docs = "Aadhaar Card, School leaving certificate, Unemployed registration card"
            web = f"https://msde.gov.in/skill{id_counter}"
        else:
            # General Welfare
            name = f"Social Welfare Security Scheme - Support {id_counter}"
            desc = f"General state-funded social relief for economically weak sections including widows and distressed families."
            inc_lim = 150000
            bpl = "Yes"
            benefits = "Direct cash allowance of Rs. 1500 per month."
            docs = "Aadhaar Card, Income certificate, Bank passbook"
            web = f"https://socialjustice.gov.in/welfare{id_counter}"
            
        current_schemes.append({
            "Scheme_Name": name,
            "Beneficiary": f"Eligible {sector} Beneficiaries",
            "Description": desc,
            "Min_Age": min_age,
            "Max_Age": max_age,
            "Income_Limit": inc_lim,
            "State": st,
            "Gender": gen,
            "Education": edu,
            "Occupation": occ,
            "Category": cat,
            "Disability_Status": dis,
            "Rural_Urban": r_u,
            "Employment_Status": emp,
            "Marital_Status": marital,
            "Farmer_Status": farmer,
            "Student_Status": student,
            "BPL_Status": bpl,
            "Minority_Status": minority,
            "Benefits": benefits,
            "Required_Documents": docs,
            "Official_Website": web
        })
        id_counter += 1
        
    # Standardize columns and add Scheme_ID
    schemes_list = []
    for idx, sch in enumerate(current_schemes):
        sch_id = f"SCH{idx+1:03d}"
        entry = {"Scheme_ID": sch_id}
        entry.update(sch)
        schemes_list.append(entry)
        
    df = pd.DataFrame(schemes_list)
    df.to_csv(filename, index=False)
    print(f"Generated {len(schemes_list)} scheme records in {filename}")

if __name__ == "__main__":
    # Create models and graphs directories if they don't exist
    os.makedirs("models", exist_ok=True)
    os.makedirs("graphs", exist_ok=True)
    
    generate_users_csv("users.csv", count=1500)
    generate_schemes_csv("schemes.csv")
