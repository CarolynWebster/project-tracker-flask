"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    grades = hackbright.get_grades_by_github(github)

    return render_template('student_info.html', first=first, 
                                                last=last, github=github,
                                                grades=grades)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template('student_search.html')


@app.route("/student-input")
def show_input_form():
    """Show form for adding student to database"""

    return render_template('student-input.html')


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    fname = request.form.get('first_name')
    lname = request.form.get('last_name')
    ghub = request.form.get('github')

    hackbright.make_new_student(fname, lname, ghub)

    return render_template('student-added.html', github=ghub)


@app.route("/projects")
def list_projects():
    """Returns a list of projects with title, desc, and max grade"""

    proj_name = request.args.get('title')

    #get project name, description, and max grade
    title, description, max_grade = hackbright.get_proj_info(proj_name)

    #a list of all the grades for that project
    all_grades = hackbright.get_grades_by_title(proj_name)

    #holds tuples (github, grade, student)
    grades = []

    # grades are (github, grade) tuples
    for grade in all_grades:
        ghub = grade[0]
        #(first_name, last_name, github)
        student_info = hackbright.get_student_by_github(ghub)
        student = "{} {}".format(student_info[0], student_info[1])
        grade_info = (ghub, grade[1], student)
        grades.append(grade_info)

    # return render_template("project-info.html", title=proj_name,
    #                                             description=result[1],
    #                                             max_grade=result[2])
    return render_template("project-info.html", title=title,
                                                description=description,
                                                max_grade=max_grade, 
                                                grades=grades)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
