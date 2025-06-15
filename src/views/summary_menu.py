from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import Qt
from src.generated.summary_menu import Ui_SummaryWindow
from src.generated.job_template import Ui_Job_Form
from src.generated.skill_template import Ui_Skill_Form
from src.generated.education_desc import Ui_Edu_Form

from src.utils.regex.education_extractor import extract_education
from src.utils.regex.experience_extractor import extract_experience
from src.utils.regex.skill_extractor import extract_skills


class SummaryPage(QMainWindow):
    def __init__(self, detail_id, text, full_name, date_of_birth, address, phone_number):
        super().__init__()
        self.ui = Ui_SummaryWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Summary")

        self.detail_id = detail_id
        self.text = text

        self.ui.nameLabel.setText(full_name)

        contact_info = str(date_of_birth) + "\n" + str(address) + "\n" + str(phone_number)
        self.ui.contactLabel.setText(contact_info if contact_info else "Unknown")

        skill = Skill_Form(extract_skills(self.text))
        self.ui.horizontalLayout.addWidget(skill, Qt.AlignTop | Qt.AlignLeft)
        self.ui.horizontalLayout.addStretch(1)

        job = Job_Form(extract_experience(self.text)[0])
        self.ui.verticalLayout_3.addWidget(job, Qt.AlignTop | Qt.AlignLeft)
        self.ui.verticalLayout_3.addStretch(1)

        edu = Edu_Form(extract_education(self.text))
        self.ui.verticalLayout_4.addWidget(edu, Qt.AlignTop | Qt.AlignLeft)
        self.ui.verticalLayout_4.addStretch(1)


class Job_Form(QWidget):
    def __init__(self, job_dict):
        super().__init__()
        self.ui = Ui_Job_Form()
        self.ui.setupUi(self)
        self.setMinimumSize(430, 100)
        
        title = job_dict.get("company")
        self.ui.jobTitle.setText(title)
        company = job_dict.get("title")
        self.ui.jobCompany.setText(company)
        year = job_dict.get("start") + " - " + job_dict.get("end", "Present")
        self.ui.jobYear.setText(year)
        desc = job_dict.get("description", "")
        self.ui.jobDescription.setText(desc)


class Edu_Form(QWidget):
    def __init__(self, edu_dict):
        super().__init__()
        self.ui = Ui_Edu_Form()
        self.ui.setupUi(self)
        self.setMinimumSize(450, 75)
        major = edu_dict.get("major")
        self.ui.eduMajor.setText(major)
        place = edu_dict.get("school")
        self.ui.eduPlace.setText(place)
        year = edu_dict.get("year")
        self.ui.eduYear.setText(str(year))


class Skill_Form(QWidget):
    def __init__(self, skill):
        super().__init__()
        self.ui = Ui_Skill_Form()
        self.ui.setupUi(self)
        self.setMinimumSize(100, 40)
    
        skill_text = "\n".join(skill) if skill else ""

        self.ui.skillName.setText(skill_text)
        self.ui.skillName.adjustSize()
        self.ui.skillFrame.adjustSize()

