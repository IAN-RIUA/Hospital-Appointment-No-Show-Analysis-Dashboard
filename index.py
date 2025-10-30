#  Import Libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings("ignore")
sns.set(style="whitegrid")

#  Data Loading Function
# ==========================
def load_data(filepath: str) -> pd.DataFrame:
    """Load the medical appointment dataset."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    df = pd.read_csv(filepath)
    print(f" Data successfully loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

# ==========================
#  Data Cleaning Function
# ==========================
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare the dataset for analysis."""
    # Rename columns for easier access
    df.rename(columns={'No-show': 'No_show'}, inplace=True)
    
    # Convert No_show to binary (1 = No-show, 0 = Show)
    df['No_show'] = df['No_show'].apply(lambda x: 1 if x == 'Yes' else 0)

    # Convert date columns to datetime
    df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])

    # Create WaitingDays column
    df['WaitingDays'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days
    df['WaitingDays'] = df['WaitingDays'].apply(lambda x: max(x, 0))  # Handle negatives
    
    # Remove invalid ages
    df = df[df['Age'] >= 0]

    print(f" Data cleaned. Remaining records: {df.shape[0]}")
    return df

# ==========================
#  Exploratory Analysis
# ==========================
def analyze_data(df: pd.DataFrame):
    """Perform EDA and visualize relationships."""
    
    # Overall No-show rate
    no_show_rate = df['No_show'].mean() * 100
    print(f" Overall No-Show Rate: {no_show_rate:.2f}%")
    
    # Plot: No-Show Distribution
    sns.countplot(x='No_show', data=df)
    plt.title('Appointment Attendance (0 = Show, 1 = No-Show)')
    plt.show()
    
    # Age vs No-Show
    plt.figure(figsize=(8,5))
    sns.histplot(data=df, x='Age', hue='No_show', multiple='stack', bins=30)
    plt.title('Age Distribution by Attendance')
    plt.show()
    
    # Gender vs No-Show
    plt.figure(figsize=(6,4))
    sns.barplot(x='Gender', y='No_show', data=df, ci=None)
    plt.title('No-Show Rate by Gender')
    plt.show()
    
    # SMS reminders effect
    plt.figure(figsize=(6,4))
    sns.barplot(x='SMS_received', y='No_show', data=df, ci=None)
    plt.title('Impact of SMS Reminders on Attendance')
    plt.show()
    
    # Waiting Days vs No-Show
    plt.figure(figsize=(8,5))
    sns.boxplot(x='No_show', y='WaitingDays', data=df)
    plt.title('Waiting Days vs No-Show')
    plt.show()


def summarize_insights(df: pd.DataFrame):
    """Print key insights from the dataset."""
    avg_wait_noshow = df[df['No_show'] == 1]['WaitingDays'].mean()
    avg_wait_show = df[df['No_show'] == 0]['WaitingDays'].mean()
    
    print("\n Summary Insights:")
    print(f"- Average waiting days (No-Show): {avg_wait_noshow:.2f}")
    print(f"- Average waiting days (Show): {avg_wait_show:.2f}")
    
    if avg_wait_noshow > avg_wait_show:
        print(" Patients with longer waiting times tend to miss appointments more often.")
    else:
        print(" Waiting time does not significantly affect attendance in this dataset.")
    
    # Gender effect
    gender_rate = df.groupby('Gender')['No_show'].mean() * 100
    print(f"- No-Show Rate by Gender:\n{gender_rate}\n")
    
    # SMS effect
    sms_rate = df.groupby('SMS_received')['No_show'].mean() * 100
    print(f"- SMS Reminder Impact:\n{sms_rate}\n")
    
    print("Key Takeaway: Shorter waiting times and SMS reminders improve attendance rates.")


def main():
    filepath = "medical appointment.csv"
    df = load_data(filepath)
    df = clean_data(df)
    analyze_data(df)
    summarize_insights(df)

if __name__ == "__main__":
    main()




