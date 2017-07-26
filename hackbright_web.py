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


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
