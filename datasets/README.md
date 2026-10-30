# 📂 Datasets & Data Storage Process

## Overview
This directory serves as the **operational datastore** for the Government Scheme Recommendation System. The application uses structured CSV flat-files with strict schemas for transaction persistence, eliminating the need for heavyweight database servers while maintaining ACID-like write safety through Node.js file streams.

---

## 📁 Dataset Catalog

| File Name | Purpose | Primary Consumer | Record Format |
|---|---|---|---|
| `schemes.csv` | Master database of government schemes | Recommendation engine, Scheme routes | Core Scheme Criteria |
| `users.csv` | Registered user profiles & credentials | Auth controller, User controller | User Accounts |
| `admins.csv` | Administrative role credentials | Admin controller | Admin Accounts |
| `applications.csv` | Citizen scheme application submissions | User dashboard, Admin tracking | Applications |
| `documents.csv` | Uploaded document verification records | User verification | Document Metadata |
| `favorites.csv` | Citizen bookmarked schemes | User dashboard | Bookmarks |
| `notifications.csv` | System and deadline alerts | Notification bar | Alerts |
| `chat_history.csv` | Citizen chatbot interactions | Chatbot analytics | Chat Logs |
| `feedback.csv` | Citizen scheme feedback and ratings | Admin analytics | Feedback |
| `login.csv` | Authentication audit trail | Security audit | Login History |
| `email_logs.csv` | Outgoing notification email logs | Mail service | Email Logs |

---

## 📋 Schema Specifications

### 1. `schemes.csv` (Government Schemes)
```csv
scheme_id,scheme_name,description,department,min_age,max_age,income_limit,eligibility_criteria,benefits,required_documents,required_certificates,last_application_date,official_website,category,state,created_at
```
- **`scheme_id`**: Numeric unique identifier (1–10).
- **`scheme_name`**: Official title (e.g., *PM Kisan Samman Nidhi*, *Ayushman Bharat*).
- **`department`**: Central/State Ministry (e.g., *Ministry of Agriculture*, *Ministry of Health*).
- **`min_age` / `max_age`**: Numeric age window (0 to 100).
- **`income_limit`**: Annual income ceiling in ₹ (or `"unlimited"`).
- **`eligibility_criteria`**: Comma-separated target tags (e.g., `"Farmer,Land ownership"`).
- **`benefits`**: Financial or physical grant description (e.g., `"₹6,000 annually"`, `"₹5 lakh coverage"`).
- **`required_documents`**: Proof of identity/residence (Aadhaar, Ration Card, etc.).
- **`official_website`**: Verified `.gov.in` portal URL for final submission.

### 2. `users.csv` (Registered Users)
```csv
user_id,full_name,email,password,mobile_number,aadhaar_number,pan_number,date_of_birth,age,gender,state,district,taluka,village,address,occupation,education,annual_income,category,religion,disability_status,farmer_status,student_status,employment_status,marital_status,bank_name,bank_account_number,ifsc_code,profile_image,profile_completion_percentage,created_at,recommended_scheme
```
- **`password`**: Securely hashed with bcrypt (salt rounds = 10).
- **`profile_completion_percentage`**: Integer (0 to 100%) tracking demographic profile completeness.

---

## 🔄 Read & Write Process

Backend controllers utilize streaming readers and atomic writers:
- **Reading**: `fs.createReadStream().pipe(csv())` prevents high memory usage.
- **Writing**: `csv-writer` (`createObjectCsvWriter`) formats structured JS objects to CSV lines, ensuring header alignment.

> **Important**: Do not delete the header row from any CSV file in this directory. Empty CSVs must preserve line 1 headers to allow the `csv-parser` stream to initialize properly.

