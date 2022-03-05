roles = [
    {
        "name": "Superadmin",
        "shorthand": "SDM",
        "is_specific": False,
    },
    {
        "name": "Admin",
        "shorthand": "ADM",
        "is_specific": False,
    },
    {
        "name": "User",
        "shorthand": "USR",
        "is_specific": False,
    },
    {
        "name": "Main Teacher",
        "shorthand": "mtr",
        "is_specific": True,
    },
    {
        "name": "Assistant Teacher",
        "shorthand": "atr",
        "is_specific": True,
    },
    {
        "name": "Coordinator",
        "shorthand": "cor",
        "is_specific": True,
    },
    {
        "name": "Academic Director",
        "shorthand": "adr",
        "is_specific": True,
    },
    {
        "name": "Class Leader",
        "shorthand": "clr",
        "is_specific": True
    }
]

tags = [
    {
        "name": "contracted",
        "description": "This staff has signed the contract.",
        "deletable": False
    },
    {
        "name": "high-achiever",
        "description": "This staff is considered a 'high achiever' by the center.",
        "deletable": False
    }
]

departments = [
    {
        "name": "Board of Directors",
        "shorthand": "BOD",
        "description": "Being the pinnacle of the center, the BOD makes various decisions regarding the expansion of the center."

    },
    {
        "name": "Secretariat",
        "shorthand": "SEC",
        "description": "The Secretariat consists of department heads and is also a subset of the BOD. The Secretariat and the BOD make up the Upper Management.",
    },
    {
        "name": "IT Department",
        "shorthand": "ITD",
        "description": "IT Department's members design, develop and maintain the center's tech infrastructure. "
        "They are also responsible to come up with new ideas that will automate various processes of the center "
        "(since the center is mostly online). And, we also made this website :)",
    },
    {
        "name": "HR Department",
        "shorthand": "HRD",
        "description": "The Human Resource Department plans, coordinates, and directs the administrative functions "
        "of the center. Its oversees the recruiting, interviewing, and hiring of new staff; "
        "consults with top executives on strategic planning; and serves as a link between the center's management and its employees.",
    },
    {
        "name":"Finance Department",
        "shorthand":"FIN",
        "description":"The Finance Department manages payrolls, oversees the center's spendings and consults with top executives "\
            "on determining fees for new classes, courses and services as well as salaries for newly appointed positions. "\
            "The department is also responsible to keep track of students' monthly fee transactions.",
    },
    {
        "name":"Marketing and Student Service Department",
        "shorthand":"MKS",
        "description":"The marketing aspect of the department manages the center's communication channels such as "\
            "its Facebook page, official website, and YouTube channel. It is also responsible in the announcement of "\
            "new classes and changes center-wide. The student service aspect deals with student registration, payment "\
            "and complain report and resolution.",
    },
    {
        "name":"Academic Department",
        "shorthand":"ACD",
        "description":"The Academic Department is by far the largest in the center. The department "\
        "consists of Main Teachers, Assistant Teachers and Coordinators. They are the frontliners of the "\
        "center such that they are the ones conducting lessons to the students every day.",
    }
]

categories = [
    {"name":"Starters"},
    {"name":"Movers"},
    {"name":"Flyers"},
    {"name":"KET"},
    {"name":"PET"},
    {"name":"FCE"},
    {"name":"CAE"},
    {"name":"CPE"},
    {"name":"IELTS"},
    {"name":"General English"},
    {"name":"Club"},
    {
        "name":"Grammar",
        "description":"All classes containing 'grammar' must go under this category (e.g. Grammar for IELTS)."
    },
    {"name":"Duolingo"}
]


jobs = [

    {
        "title":"Secretary",
        "salary":400000
    },
    {
        "title":"Academic Director",
        "salary":350000
    },
    {
        "title":"Coordinator",
        "salary":300000
    },
    {
        "title":"Content Writer",
        "salary":300000
    },
    {
        "title":"Graphic Designer",
        "salary":300000
    },
    {
        "title":"Customer Service",
        "salary":300000
    },
    {
        "title":"Student Service",
        "salary":300000
    },
    {
        "title":"Developer",
        "salary":350000
    },
    {
        "title":"UI/UX Designer",
        "salary":350000
    },
    {
        "title":"Accountant",
        "salary":300000
    }
]