from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import Qt
from src.generated.summary_menu import Ui_SummaryWindow
from src.generated.job_template import Ui_Job_Form
from src.generated.skill_template import Ui_Skill_Form
from src.generated.education_desc import Ui_Edu_Form

class SummaryPage(QMainWindow):
    def __init__(self, detail_id, text):
        super().__init__()
        self.ui = Ui_SummaryWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Summary")

        self.detail_id = detail_id
        self.text = text

        #!Placeholder
        name = "Salman Halim"
        contact = "Address : 6th Street \n Phone : 0888-888-888"
        #!Holder
        self.ui.nameLabel.setText(name)
        self.ui.contactLabel.setText(contact)


        skill = Skill_Form("Asian Cuisine")
        self.ui.horizontalLayout.addWidget(skill, Qt.AlignTop | Qt.AlignLeft)
        self.ui.horizontalLayout.addStretch(1)

        job_dict = {"job_title": "Head Chef", "job_company": "Chez Gusteau", "job_year": "2020-2022", "job_desc": ""}
        job = Job_Form(job_dict)
        self.ui.verticalLayout_3.addWidget(job, Qt.AlignTop | Qt.AlignLeft)
        self.ui.verticalLayout_3.addStretch(1)

        edu_dict = {"edu_major" : "Mathematics", "edu_place": "MIT", "edu_year":"2022-2024"}
        edu = Edu_Form(edu_dict)
        self.ui.verticalLayout_4.addWidget(edu, Qt.AlignTop | Qt.AlignLeft)
        self.ui.verticalLayout_4.addStretch(1)


class Job_Form(QWidget):
    def __init__(self, job_dict):
        super().__init__()
        self.ui = Ui_Job_Form()
        self.ui.setupUi(self)
        self.setMinimumSize(430, 100)
        
        title = job_dict.get("job_title")
        self.ui.jobTitle.setText(title)
        company = job_dict.get("job_company")
        self.ui.jobCompany.setText(company)
        year = job_dict.get("job_year")
        self.ui.jobYear.setText(year)
        desc = job_dict.get("job_desc")
        self.ui.jobDescription.setText(desc)


class Edu_Form(QWidget):
    def __init__(self, edu_dict):
        super().__init__()
        self.ui = Ui_Edu_Form()
        self.ui.setupUi(self)
        self.setMinimumSize(450, 75)
        major = edu_dict.get("edu_major")
        self.ui.eduMajor.setText(major)
        place = edu_dict.get("edu_place")
        self.ui.eduPlace.setText(place)
        year = edu_dict.get("edu_year")
        self.ui.eduYear.setText(year)


class Skill_Form(QWidget):
    def __init__(self, skill):
        super().__init__()
        self.ui = Ui_Skill_Form()
        self.ui.setupUi(self)
        self.setMinimumSize(100, 40)
    
        self.ui.skillName.setText(skill)
        self.ui.skillName.adjustSize()
        self.ui.skillFrame.adjustSize()

