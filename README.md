# GitHub Users in Austin with 100+ Followers

## Data Collection
This dataset contains information about GitHub users located in Austin, Texas, who have more than 100 followers.

### Data Files
1. `users.csv`: Detailed information about each user
2. `repositories.csv`: Public repositories for these users

### Data Collection Process
- Used GitHub Search API to find users in Austin
- Filtered users with over 100 followers
- Collected user details and their repositories

### Statistics
- Total Users: 100
- Total Repositories: 7263
- Collection Date: 2024-10-31

### Columns
#### users.csv
- `login`: GitHub username
- `name`: Full name
- `company`: Cleaned company name
- `location`: City (Austin)
- `email`: User's email
- `hireable`: Availability for hiring
- `bio`: User's bio
- `public_repos`: Number of public repositories
- `followers`: Follower count
- `following`: Following count
- `created_at`: GitHub account creation date

#### repositories.csv
- `login`: Repository owner's username
- `full_name`: Repository full name
- `created_at`: Repository creation date
- `stargazers_count`: Number of stars
- `watchers_count`: Number of watchers
- `language`: Primary programming language
- `has_projects`: Projects enabled
- `has_wiki`: Wiki enabled
- `license_name`: Repository license
