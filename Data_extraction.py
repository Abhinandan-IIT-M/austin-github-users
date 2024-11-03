#The Main code is to fetch the data while fetching the datathere was a error, i.e "pagination",  in which only 100 elements were only getting extracted.
#We resolved that issue by delimiting the 100 elements limit.
#Also here in this code i have given option to validate the "token" as it is very sensitive data and i was doing it on google Collab. 


!pip install requests
import os
import requests
import csv
import time
import getpass

def get_github_token():
    """
    Retrieve GitHub token securely
    """
    # Check environment variable first
    token = os.environ.get('GITHUB_TOKEN')

    # If no environment variable, prompt user
    if not token:
        print("GitHub token not found in environment variables.")
        token = getpass.getpass("Enter your GitHub Personal Access Token: ")

        # Option to save for current session
        save_choice = input("Save token for this session? (yes/no): ").lower()
        if save_choice == 'yes':
            os.environ['GITHUB_TOKEN'] = token

    # Validate token by making a simple GitHub API request
    try:
        response = requests.get('https://api.github.com/user',
                                headers={'Authorization': f'token {token}'})
        if response.status_code == 200:
            print("Token successfully validated!")
            return token
        else:
            raise ValueError("Invalid GitHub token")
    except Exception as e:
        print(f"Token validation failed: {e}")
        raise ValueError("Could not validate GitHub token")

def clean_company_name(company):
    """
    Clean up company names according to specified requirements
    """
    if not company:
        return ''

    # Strip leading @ symbol (only first one)
    if company.startswith('@'):
        company = company.lstrip('@')

    # Trim whitespace and convert to uppercase
    return company.strip().upper()

def fetch_all_users(token):
    """
    Comprehensively fetch GitHub users in Austin with over 100 followers
    Uses pagination to get beyond the initial 100 results
    """
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    base_url = "https://api.github.com/search/users"
    all_users = []
    page = 1
    per_page = 100

    while True:
        params = {
            'q': 'location:Austin followers:>100',
            'sort': 'followers',
            'order': 'desc',
            'per_page': per_page,
            'page': page
        }

        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            users = data.get('items', [])

            # Add users to the complete list
            all_users.extend(users)

            # Print progress
            print(f"Page {page}: Fetched {len(users)} users. Total so far: {len(all_users)}")

            # Break if no more users or reached GitHub's search limit
            if len(users) < per_page:
                break

            # Increment page
            page += 1

            # Respect GitHub's rate limits
            time.sleep(2)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching users on page {page}: {e}")
            break

    return all_users

def fetch_user_details(token, login):
    """
    Fetch detailed information for a specific user
    """
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    url = f"https://api.github.com/users/{login}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details for {login}: {e}")
        return None

def fetch_repositories(token, login):
    """
    Fetch repositories for a specific user
    """
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    url = f"https://api.github.com/users/{login}/repos"
    params = {
        'per_page': 500,
        'sort': 'pushed',
        'direction': 'desc'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories for {login}: {e}")
        return []

def main():
    # Get GitHub token
    try:
        TOKEN = get_github_token()
    except ValueError:
        print("Failed to obtain a valid GitHub token. Exiting.")
        return

    # Fetch all users (with comprehensive pagination)
    users = fetch_all_users(TOKEN)
    print(f"Total unique users found: {len(users)}")

    # Prepare data collections
    user_details = []
    repo_data = []

    # Fetch details for each user
    for user in users:
        # Fetch user details
        details = fetch_user_details(TOKEN, user['login'])
        if details:
            user_details.append(details)

        # Fetch repositories
        repos = fetch_repositories(TOKEN, user['login'])
        for repo in repos:
            repo_entry = {
                'login': user['login'],
                'full_name': repo['full_name'],
                'created_at': repo['created_at'],
                'stargazers_count': repo['stargazers_count'],
                'watchers_count': repo['watchers_count'],
                'language': repo.get('language', ''),
                'has_projects': str(repo.get('has_projects', False)).lower(),
                'has_wiki': str(repo.get('has_wiki', False)).lower(),
                'license_name': repo.get('license', {}).get('key', '') if repo.get('license') else ''
            }
            repo_data.append(repo_entry)

        # Add a small delay to respect GitHub API rate limits
        time.sleep(0.5)

    # Write users to CSV
    with open('users.csv', 'w', newline='', encoding='utf-8') as user_file:
        user_writer = csv.writer(user_file)
        user_writer.writerow([
            'login', 'name', 'company', 'location', 'email',
            'hireable', 'bio', 'public_repos', 'followers',
            'following', 'created_at'
        ])

        for user in user_details:
            user_writer.writerow([
                user.get('login', ''),
                user.get('name', ''),
                clean_company_name(user.get('company', '')),
                user.get('location', ''),
                user.get('email', ''),
                str(user.get('hireable', '')).lower(),
                user.get('bio', ''),
                user.get('public_repos', 0),
                user.get('followers', 0),
                user.get('following', 0),
                user.get('created_at', '')
            ])

    # Write repositories to CSV
    with open('repositories.csv', 'w', newline='', encoding='utf-8') as repo_file:
        repo_writer = csv.writer(repo_file)
        repo_writer.writerow([
            'login', 'full_name', 'created_at', 'stargazers_count',
            'watchers_count', 'language', 'has_projects',
            'has_wiki', 'license_name'
        ])

        for repo in repo_data:
            repo_writer.writerow([
                repo['login'],
                repo['full_name'],
                repo['created_at'],
                repo['stargazers_count'],
                repo['watchers_count'],
                repo['language'],
                repo['has_projects'],
                repo['has_wiki'],
                repo['license_name']
            ])

    # Create README.md
    with open('README.md', 'w', encoding='utf-8') as readme_file:
        readme_content = f"""# GitHub Users in Austin with 100+ Followers

## Data Collection
This dataset contains comprehensive information about GitHub users located in Austin, Texas, who have more than 100 followers.

### Data Files
1. `users.csv`: Detailed information about each user
2. `repositories.csv`: Public repositories for these users

### Data Collection Process
- Used GitHub Search API to find users in Austin
- Implemented comprehensive pagination to capture all users
- Filtered users with over 100 followers
- Collected detailed user information and their repositories

### Statistics
- Total Unique Users: {len(user_details)}
- Total Repositories: {len(repo_data)}
- Collection Date: {time.strftime('%Y-%m-%d')}

### Methodology
- Utilized GitHub Search API with advanced querying
- Paginated through all available results
- Respected GitHub API rate limits
- Cleaned and standardized data

### Columns Details
[Same column details as in previous README]
"""
        readme_file.write(readme_content)

    print(f"Users saved: {len(user_details)}")
    print(f"Repositories saved: {len(repo_data)}")

    # Provide a summary for verification
    print("\nVerification Summary:")
    print(f"Total Users Found: {len(user_details)}")

if __name__ == "__main__":
    main()

