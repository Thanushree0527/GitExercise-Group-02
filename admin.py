class PartTimeJob:
    def _init_(self, title, faculty):
        self.title = title
        self.faculty = faculty

class PartTimeJobPortal:
    def _init_(self):
        self.jobs = []

    def add_job(self, title, faculty):
        job = PartTimeJob(title, faculty)
        self.jobs.append(job)

    def filter_by_faculty(self, faculty):
        filtered_jobs = [job for job in self.jobs if job.faculty.lower() == faculty.lower()]
        return filtered_jobs

# Sample usage
job_portal = PartTimeJobPortal()

# Add some sample jobs
job_portal.add_job("Software Developer", "Computing and Informatics")
job_portal.add_job("Data Scientist", "Computing and Informatics")
job_portal.add_job("Information Security Analyst", "Computing and Informatics")
job_portal.add_job("Mechanical Engineer", "Engineering")
job_portal.add_job("Electrical Engineer", "Engineering")
job_portal.add_job("Chemical Engineer", "Engineering")
job_portal.add_job("Marketing Assistant", "Management")
job_portal.add_job("Sales Manager", "Management")
job_portal.add_job("Human Resources Manager", "Management")
job_portal.add_job("Graphic Designer", "Creative Multimedia")
job_portal.add_job("Film Editor", "Creative Multimedia")
job_portal.add_job("Web Developer", "Creative Multimedia")
job_portal.add_job("Library Assistant", "Others")
job_portal.add_job("Secondary School Teacher ", "Others")
job_portal.add_job("Pharmacist", "Others")

# Get user input for faculty
faculty = input("Enter faculty to filter jobs: ")

# Check if the input matches predefined faculties
if faculty.lower() in ["computing and informatics", "engineering", "management", "creative multimedia"]:
    filtered_jobs = job_portal.filter_by_faculty(faculty)
    if filtered_jobs:
        print(f"Part-time jobs in {faculty}:")
        for job in filtered_jobs:
            print(job.title)
    else:
        print(f"No part-time jobs available for the {faculty} faculty.")
# If the input doesn't match, offer to display all jobs under 'Others' or ask for a new faculty
else:
    print(f"Filtering jobs for {faculty} is not available.")
    choice = input("Do you want to see all jobs under 'Others' faculty? (yes/no): ")
    if choice.lower() == "yes":
        filtered_jobs = job_portal.filter_by_faculty("Others")
        if filtered_jobs:
            print("Part-time jobs under 'Others' faculty:")
            for job in filtered_jobs:
                print(job.title)
        else:
            print("No part-time jobs available under 'Others' faculty.")
    else:
        new_faculty = input("Enter a new faculty to filter jobs: ")
        filtered_jobs = job_portal.filter_by_faculty(new_faculty)
        if filtered_jobs:
            print(f"Part-time jobs in {new_faculty}:")
            for job in filtered_jobs:
                print(job.title)
        else:
            print(f"No part-time jobs available for the {new_faculty} faculty.") class PartTimeJob:
    def _init_(self, title, faculty):
        self.title = title
        self.faculty = faculty

class PartTimeJobPortal:
    def _init_(self):
        self.jobs = []

    def add_job(self, title, faculty):
        job = PartTimeJob(title, faculty)
        self.jobs.append(job)

    def filter_by_faculty(self, faculty):
        filtered_jobs = [job for job in self.jobs if job.faculty.lower() == faculty.lower()]
        return filtered_jobs

# Sample usage
job_portal = PartTimeJobPortal()

# Add some sample jobs
job_portal.add_job("Software Developer", "Computing and Informatics")
job_portal.add_job("Data Scientist", "Computing and Informatics")
job_portal.add_job("Information Security Analyst", "Computing and Informatics")
job_portal.add_job("Mechanical Engineer", "Engineering")
job_portal.add_job("Electrical Engineer", "Engineering")
job_portal.add_job("Chemical Engineer", "Engineering")
job_portal.add_job("Marketing Assistant", "Management")
job_portal.add_job("Sales Manager", "Management")
job_portal.add_job("Human Resources Manager", "Management")
job_portal.add_job("Graphic Designer", "Creative Multimedia")
job_portal.add_job("Film Editor", "Creative Multimedia")
job_portal.add_job("Web Developer", "Creative Multimedia")
job_portal.add_job("Library Assistant", "Others")
job_portal.add_job("Secondary School Teacher ", "Others")
job_portal.add_job("Pharmacist", "Others")

# Get user input for faculty
faculty = input("Enter faculty to filter jobs: ")

# Check if the input matches predefined faculties
if faculty.lower() in ["computing and informatics", "engineering", "management", "creative multimedia"]:
    filtered_jobs = job_portal.filter_by_faculty(faculty)
    if filtered_jobs:
        print(f"Part-time jobs in {faculty}:")
        for job in filtered_jobs:
            print(job.title)
    else:
        print(f"No part-time jobs available for the {faculty} faculty.")
# If the input doesn't match, offer to display all jobs under 'Others' or ask for a new faculty
else:
    print(f"Filtering jobs for {faculty} is not available.")
    choice = input("Do you want to see all jobs under 'Others' faculty? (yes/no): ")
    if choice.lower() == "yes":
        filtered_jobs = job_portal.filter_by_faculty("Others")
        if filtered_jobs:
            print("Part-time jobs under 'Others' faculty:")
            for job in filtered_jobs:
                print(job.title)
        else:
            print("No part-time jobs available under 'Others' faculty.")
    else:
        new_faculty = input("Enter a new faculty to filter jobs: ")
        filtered_jobs = job_portal.filter_by_faculty(new_faculty)
        if filtered_jobs:
            print(f"Part-time jobs in {new_faculty}:")
            for job in filtered_jobs:
                print(job.title)
        else:
            print(f"No part-time jobs available for the {new_faculty} faculty.")