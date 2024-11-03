#Q1
import pandas as pd

# Load the CSV files into DataFrames
users_df = pd.read_csv('users.csv')
repos_df = pd.read_csv('repositories.csv')

# Convert 'created_at' to datetime format
users_df['created_at'] = pd.to_datetime(users_df['created_at'])

# Sort by 'created_at'
sorted_users = users_df.sort_values(by='created_at')

# Get the logins of the 5 earliest registered users
earliest_users = sorted_users.head(5)['login'].tolist()

# Print the logins in ascending order of created_at
print("5 earliest registered GitHub users in Austin:", ", ".join(earliest_users))

#Q2
import pandas as pd

# Load the repositories.csv file into a DataFrame
repos_df = pd.read_csv('repositories.csv')

# Filter out missing licenses
repos_df = repos_df[repos_df['license_name'].notna()]

# Count the occurrences of each license
license_counts = repos_df['license_name'].value_counts()

# Get the 3 most popular licenses
top_licenses = license_counts.head(3).index.tolist()

# Print the top 3 licenses, comma-separated
print("3 most popular licenses:", ", ".join(top_licenses))

#Q3
import pandas as pd

# Load the users.csv file into a DataFrame
users_df = pd.read_csv('users.csv')

# Filter out missing company entries
users_df = users_df[users_df['company'].notna()]

# Count the occurrences of each company
company_counts = users_df['company'].value_counts()

# Get the company with the highest count
majority_company = company_counts.idxmax()
majority_count = company_counts.max()

# Print the company with the majority of developers
print(f"The majority of these developers work at: {majority_company} with {majority_count} developers")

#Q4
import pandas as pd

# Load the repositories.csv file into a DataFrame
repos_df = pd.read_csv('repositories.csv')

# Filter out missing language entries
repos_df = repos_df[repos_df['language'].notna()]

# Count the occurrences of each programming language
language_counts = repos_df['language'].value_counts()

# Get the most popular language
most_popular_language = language_counts.idxmax()
most_popular_count = language_counts.max()

# Print the most popular programming language
print(f"The most popular programming language among these users is: {most_popular_language} with {most_popular_count} repositories")

#Q5,Q6
import pandas as pd

# Load the CSV files into DataFrames
repos_df = pd.read_csv('repositories.csv')
users_df = pd.read_csv('users.csv')

# Calculate the highest average number of stars per repository by language
language_avg_stars = repos_df.groupby('language')['stargazers_count'].mean()
most_popular_language = language_avg_stars.idxmax()
highest_avg_stars = language_avg_stars.max()

print(f"The language with the highest average number of stars per repository is: {most_popular_language} with an average of {highest_avg_stars:.2f} stars")

# Define leader_strength as followers / (1 + following)
users_df['leader_strength'] = users_df['followers'] / (1 + users_df['following'])

# Sort users by leader_strength and get the top 5
top_leaders = users_df.sort_values(by='leader_strength', ascending=False).head(5)
top_leader_logins = top_leaders['login'].tolist()

print("Top 5 users by leader_strength:", ", ".join(top_leader_logins))


 #Q7,Q8,Q9
import pandas as pd
import numpy as np
from scipy import stats

def clean_company_names(company):
    """
    Clean up company names according to specified rules:
    1. Trim whitespace
    2. Strip leading @ symbol (only the first one)
    3. Convert to UPPERCASE

    Args:
        company (str): Original company name

    Returns:
        str: Cleaned company name or empty string if None/NaN
    """
    if pd.isna(company):
        return ''


    # Convert to string to handle potential non-string inputs
    company_str = str(company).strip()
    # Remove only the first @ if present
    if company_str.startswith('@'):
        company_str = company_str[1:]

    return company_str.strip().upper()

def process_github_data(users_file, repos_file):
    """
    Process GitHub user and repository data

    Args:
        users_file (str): Path to users CSV file
        repos_file (str): Path to repositories CSV file

    Returns:
        tuple: Processed users and repositories DataFrames
    """
    # Read the input files
    users_df = pd.read_csv(users_file)
    repos_df = pd.read_csv(repos_file)

    # Clean company names
    users_df['company'] = users_df['company'].apply(clean_company_names)

    # Convert created_at to datetime
    users_df['created_at'] = pd.to_datetime(users_df['created_at'])

    # Filter users from Austin with over 100 followers
    austin_users = users_df[
        (users_df['location'].str.contains('Austin', case=False, na=False)) &
        (users_df['followers'] > 100)
    ]

    # Filter repositories for these users
    austin_repos = repos_df[repos_df['login'].isin(austin_users['login'])]

    return austin_users, austin_repos

def analyze_github_data(users, repositories):
    """
    Perform detailed analysis on GitHub data

    Args:
        users (pd.DataFrame): Processed users DataFrame
        repositories (pd.DataFrame): Processed repositories DataFrame

    Returns:
        dict: Analysis results
    """
    # 1. Second most popular language for users who joined after 2020
    users_after_2020 = users[users['created_at'].dt.year > 2020]
    repos_after_2020 = repositories[repositories['login'].isin(users_after_2020['login'])]

    language_counts = repos_after_2020['language'].value_counts()
    second_most_popular_language = language_counts.index[1] if len(language_counts) > 1 else "Not enough data"

    # 2. Correlation between followers and public repositories
    correlation, p_value = stats.pearsonr(users['followers'], users['public_repos'])

    # 3. Regression of followers on public repositories
    slope, intercept, r_value, p_value, std_err = stats.linregress(users['public_repos'], users['followers'])

    return {
        'second_most_popular_language': second_most_popular_language,
        'followers_repos_correlation': round(correlation, 3),
        'followers_repos_regression_slope': round(slope, 3)
    }

def main():
    # Process the data
    users, repositories = process_github_data('users.csv', 'repositories.csv')

    # Perform analysis
    analysis_results = analyze_github_data(users, repositories)

    # Print results
    print("Analysis Results:")
    print(f"1. Second Most Popular Language (for users who joined after 2020): {analysis_results['second_most_popular_language']}")
    print(f"2. Correlation between Followers and Public Repositories: {analysis_results['followers_repos_correlation']}")
    print(f"3. Regression Slope of Followers on Public Repositories: {analysis_results['followers_repos_regression_slope']}")

if __name__ == '__main__':
    main()

#Q10,Q11,Q12
import pandas as pd
import numpy as np
from scipy import stats

def clean_company_names(company):
    """
    Clean up company names according to specified rules:
    1. Trim whitespace
    2. Strip leading @ symbol (only the first one)
    3. Convert to UPPERCASE

    Args:
        company (str): Original company name

    Returns:
        str: Cleaned company name or empty string if None/NaN
    """
    if pd.isna(company):
        return ''

    # Convert to string to handle potential non-string inputs
    company_str = str(company).strip()

    # Remove only the first @ if present
    if company_str.startswith('@'):
        company_str = company_str[1:]

    return company_str.strip().upper()

def process_github_data(users_file, repos_file):
    """
    Process GitHub user and repository data

    Args:
        users_file (str): Path to users CSV file
        repos_file (str): Path to repositories CSV file

    Returns:
        tuple: Processed users and repositories DataFrames
    """
    # Read the input files
    users_df = pd.read_csv(users_file)
    repos_df = pd.read_csv(repos_file)

    # Clean company names
    users_df['company'] = users_df['company'].apply(clean_company_names)

    # Filter users from Austin with over 100 followers
    austin_users = users_df[
        (users_df['location'].str.contains('Austin', case=False, na=False)) &
        (users_df['followers'] > 100)
    ]

    # Filter repositories for these users
    austin_repos = repos_df[repos_df['login'].isin(austin_users['login'])]

    return austin_users, austin_repos

def analyze_github_advanced_data(users, repositories):
    """
    Perform advanced analysis on GitHub data

    Args:
        users (pd.DataFrame): Processed users DataFrame
        repositories (pd.DataFrame): Processed repositories DataFrame

    Returns:
        dict: Analysis results
    """
    # 1. Correlation between projects and wiki enabled
    # Create binary columns for easier correlation
    repositories['projects_enabled'] = repositories['has_projects'].astype(int)
    repositories['wiki_enabled'] = repositories['has_wiki'].astype(int)

    # Calculate correlation between projects and wiki
    projects_wiki_corr, _ = stats.pearsonr(
        repositories['projects_enabled'],
        repositories['wiki_enabled']
    )

    # 2. Difference in following for hireable vs non-hireable users
    hireable_following_avg = users[users['hireable'] == True]['following'].mean()
    non_hireable_following_avg = users[users['hireable'] == False]['following'].mean()
    following_difference = hireable_following_avg - non_hireable_following_avg

    # 3. Bio length impact on followers
    # Count words in bio (splitting by whitespace, counting Unicode words)
    users['bio_word_count'] = users['bio'].fillna('').str.split().str.len()

    # Filter out users without bios
    bio_users = users[users['bio_word_count'] > 0]

    # Regression of followers on bio word count
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        bio_users['bio_word_count'],
        bio_users['followers']
    )

    return {
        'projects_wiki_correlation': round(projects_wiki_corr, 3),
        'following_difference': round(following_difference, 3),
        'followers_bio_length_slope': round(slope, 3)
    }

def main():
    # Process the data
    users, repositories = process_github_data('users.csv', 'repositories.csv')

    # Perform advanced analysis
    analysis_results = analyze_github_advanced_data(users, repositories)

    # Print results
    print("Advanced Analysis Results:")
    print(f"1. Correlation between Projects and Wiki Enabled: {analysis_results['projects_wiki_correlation']}")
    print(f"2. Difference in Following (Hireable - Non-Hireable): {analysis_results['following_difference']}")
    print(f"3. Regression Slope of Followers on Bio Length: {analysis_results['followers_bio_length_slope']}")

if __name__ == '__main__':
    main()

#Q13,Q14,Q15
import pandas as pd
import numpy as np

def clean_company_names(company):
    """
    Clean up company names according to specified rules:
    1. Trim whitespace
    2. Strip leading @ symbol (only the first one)
    3. Convert to UPPERCASE

    Args:
        company (str): Original company name

    Returns:
        str: Cleaned company name or empty string if None/NaN
    """
    if pd.isna(company):
        return ''

    # Convert to string to handle potential non-string inputs
    company_str = str(company).strip()

    # Remove only the first @ if present
    if company_str.startswith('@'):
        company_str = company_str[1:]

    return company_str.strip().upper()

def process_github_data(users_file, repos_file):
    """
    Process GitHub user and repository data

    Args:
        users_file (str): Path to users CSV file
        repos_file (str): Path to repositories CSV file

    Returns:
        tuple: Processed users and repositories DataFrames
    """
    # Read the input files
    users_df = pd.read_csv(users_file)
    repos_df = pd.read_csv(repos_file)

    # Clean company names
    users_df['company'] = users_df['company'].apply(clean_company_names)

    # Convert created_at to datetime in UTC
    repos_df['created_at'] = pd.to_datetime(repos_df['created_at'], utc=True)

    return users_df, repos_df

def analyze_github_advanced_data(users, repositories):
    """
    Perform advanced analysis on GitHub data

    Args:
        users (pd.DataFrame): Processed users DataFrame
        repositories (pd.DataFrame): Processed repositories DataFrame

    Returns:
        dict: Analysis results
    """
    # 1. Repositories created on weekends (UTC)
    # Add day of week column (0 = Monday, 6 = Sunday)
    repositories['day_of_week'] = repositories['created_at'].dt.day_name()

    # Count weekend repositories per user
    weekend_repos = repositories[repositories['day_of_week'].isin(['Saturday', 'Sunday'])]
    weekend_repos_count = weekend_repos.groupby('login').size().sort_values(ascending=False)

    # Top 5 users creating repositories on weekends
    top_weekend_users = weekend_repos_count.head(5).index.tolist()

    # 2. Email sharing by hireable status
    # Calculate fraction of users with email for hireable and non-hireable groups
    hireable_email_fraction = users[users['hireable'] == True]['email'].notna().mean()
    non_hireable_email_fraction = users[users['hireable'] == False]['email'].notna().mean()
    email_fraction_difference = hireable_email_fraction - non_hireable_email_fraction

    # 3. Most common surname
    # Extract last name, handling missing or improperly formatted names
    def extract_last_name(name):
        if pd.isna(name):
            return np.nan
        # Trim and split by whitespace, take the last element
        parts = str(name).strip().split()
        return parts[-1] if parts else np.nan

    users['last_name'] = users['name'].apply(extract_last_name)

    # Count last names, excluding NaN
    last_name_counts = users['last_name'].value_counts()
    max_count = last_name_counts.max()
    most_common_surnames = last_name_counts[last_name_counts == max_count].index.sort_values().tolist()

    return {
        'top_weekend_repos_users': top_weekend_users,
        'email_fraction_difference': round(email_fraction_difference, 3),
        'most_common_surnames': most_common_surnames
    }

def main():
    # Process the data
    users, repositories = process_github_data('users.csv', 'repositories.csv')

    # Perform advanced analysis
    analysis_results = analyze_github_advanced_data(users, repositories)

    # Print results
    print("Advanced Analysis Results:")
    print(f"1. Top 5 Users Creating Repositories on Weekends: {', '.join(analysis_results['top_weekend_repos_users'])}")
    print(f"2. Difference in Email Sharing (Hireable - Non-Hireable): {analysis_results['email_fraction_difference']}")
    print(f"3. Most Common Surname(s): {', '.join(analysis_results['most_common_surnames'])}")

if __name__ == '__main__':
    main()

