class ExtraFeaturesPartTimeJob:
    def _init_(self, title, description, hours, pay_rate):
        self.title = title
        self.description = description
        self.hours = hours
        self.pay_rate = pay_rate
        self.completed = False
    
    def mark_completed(self):
        self.completed = True

class JobManagementSystem:
    def _init_(self):
        self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)

    def display_jobs(self, filter_keyword=None):
        if not self.jobs:
            print("No jobs available.")
        else:
            for i, job in enumerate(self.jobs, 1):
                if not filter_keyword or filter_keyword.lower() in job.title.lower() or filter_keyword.lower() in job.description.lower():
                    print(f"Job {i}: {job.title}")
                    print(f"Description: {job.description}")
                    print(f"Hours: {job.hours}")
                    print(f"Pay Rate: RM{job.pay_rate}/hour")
                    print("Status: Completed" if job.completed else "Status: Pending")
                    print()

    def search_jobs(self, keyword):
        self.display_jobs(filter_keyword=keyword)

    def filter_jobs(self, min_hours=None, max_pay_rate=None):
        filtered_jobs = []
        for job in self.jobs:
            if (min_hours is None or job.hours >= min_hours) and (max_pay_rate is None or job.pay_rate <= max_pay_rate):
                filtered_jobs.append(job)
        return filtered_jobs

    def update_job_feed(self):
        
        print("Job feed updated.")

# Example usage:
if _name_ == "_main_":
    job_system = JobManagementSystem()

    job1 = PartTimeJob("J&T Delivery", "Deliver packages to customers", 10, 15)
    job2 = PartTimeJob("Tutor", "Tutor students in Math or Addmath", 5, 20)
    job3 = PartTimeJob("KK Mart Cyberjaya (Cashier)", "Handle cash transactions at the register", 20, 12)

    job_system.add_job(job1)
    job_system.add_job(job2)
    job_system.add_job(job3)

    print("All jobs:")
    job_system.display_jobs()

    print("\nSearch results for 'Delivery':")
    job_system.search_jobs("Delivery")

    print("\nFiltered jobs (min hours: 10, max pay rate: $15):")
    filtered_jobs = job_system.filter_jobs(min_hours=10, max_pay_rate=15)
    for i, job in enumerate(filtered_jobs, 1):
        print(f"Job {i}: {job.title}")

    job_system.update_job_feed()