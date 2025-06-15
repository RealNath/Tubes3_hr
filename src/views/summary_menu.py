from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import Qt
from src.generated.summary_menu import Ui_SummaryWindow
from src.generated.job_template import Ui_Job_Form
from src.generated.education_desc import Ui_Edu_Form

class SummaryPage(QMainWindow):
    def __init__(self, applicant_id):
        super().__init__()
        self.ui = Ui_SummaryWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Summary")

        self.id = applicant_id

        #!Placeholder
        name = "John Doe"
        contact = "Call me yeah?"
        #!Holder
        self.ui.nameLabel.setText(name)
        self.ui.contactLabel.setText(contact)

        job_dict = {"job_title": "CTO", "job_year": "2020-2022", "job_desc": "Lorem ipsum"}
        job = Job_Form(job_dict)
        job2 = Job_Form(job_dict)
        job3 = Job_Form(job_dict)
        self.ui.verticalLayout_3.addWidget(job, Qt.AlignTop | Qt.AlignLeft)
        self.ui.verticalLayout_3.addWidget(job2, Qt.AlignTop | Qt.AlignLeft)
        self.ui.verticalLayout_3.addWidget(job3, Qt.AlignTop | Qt.AlignLeft)
        self.ui.verticalLayout_3.addStretch(1)

        edu_dict = {"edu_major" : "Mathematics", "edu_place": "MIT", "edu_year":"2022-2024"}
        edu = Edu_Form(edu_dict)
        edu2 = Edu_Form(edu_dict)
        edu3 = Edu_Form(edu_dict)
        self.ui.verticalLayout_4.addWidget(edu, Qt.AlignTop | Qt.AlignLeft)
        self.ui.verticalLayout_4.addWidget(edu2, Qt.AlignTop | Qt.AlignLeft)
        self.ui.verticalLayout_4.addWidget(edu3, Qt.AlignTop | Qt.AlignLeft)
        self.ui.verticalLayout_4.addStretch(1)


class Job_Form(QWidget):
    def __init__(self, job_dict):
        super().__init__()
        self.ui = Ui_Job_Form()
        self.ui.setupUi(self)
        self.setMinimumSize(430, 80)
        
        title = job_dict.get("job_title")
        self.ui.jobTitle.setText(title)
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




