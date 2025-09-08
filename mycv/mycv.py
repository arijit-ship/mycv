import os
from src.loader import CVLoader

class MyCV:
    """
    Main CV object.
    Loads data using CVLoader and provides access to all sections.
    """

    def __init__(self, data_file="mycv.yaml"):
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"{data_file} not found.")
        self.loader = CVLoader(data_file)

    # Expose loader methods
    @property
    def personal_info(self):
        return self.loader.get_personal_info()

    @property
    def about(self):
        return self.loader.get_about()

    @property
    def education(self):
        return self.loader.get_education()

    @property
    def experience(self):
        return self.loader.get_experience()

    @property
    def skills(self):
        return self.loader.get_skills()

    @property
    def projects(self):
        return self.loader.get_projects()

    @property
    def certificates(self):
        return self.loader.get_certificates()

    @property
    def presentations(self):
        return self.loader.get_presentations()

    def get_section(self, key):
        return self.loader.get_section(key)


# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    cv = MyCV("mycv.yaml")
    print("Name:", cv.personal_info.get("name"))
    print("Education:", cv.education)
    print("Projects:", cv.projects)
