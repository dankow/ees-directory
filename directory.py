#!/usr/bin/env python3

"""Produce a PDF directory from a CSV of student data

"""

import csv
import os
import sys
import argparse
import phonenumbers
from fpdf import FPDF

class PDF(FPDF):
    col = 0
    y0 = 10
    
    def set_col(self, col):
        """ Set position at a given column """
        self.col = col
        x= 10 + col * 129
        self.set_left_margin(x)
        self.set_x(x)

    def accept_page_break(self):
        """ Method accepting or not automatic page break """
        if self.col < 2 or self.y >= 175:
#         if self.col < 2:
            # Go to next column
            self.set_col(self.col + 1)
            # Set ordinate to top
            self.set_y(self.y0)
            # Keep on page
            return False
        else:
            # Go back to first column
            self.set_col(0)
            # Page break
            return True

class Directory:
    students = []
    classes = set()
    columns = [
                "timestamp",
                "child_name",
                "grade",
                "teacher_name",
                "guardian1_name",
                "guardian1_email",
                "guardian1_phone",
                "guardian2_name",
                "guardian2_email",
                "guardian2_phone",
                "pk_class"
            ]              
    
    def __init__(self, filename):
        with open(filename, 'r') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)
            for row in readCSV:
                if row[0] != '':
                    self.students.append(Student(row, self.columns))
                    try:
                        if row[self.columns.index("pk_class")] == "":
                            self.classes.add(row[self.columns.index("teacher_name")])
                        else:
                            self.classes.add("{} ({})".format(row[self.columns.index("teacher_name")],row[self.columns.index("pk_class")]))
                    except IndexError:
                        self.classes.add(row[self.columns.index("teacher_name")])
    def __str__(self):
        return'\n'.join(map(str, self.students))
        
    def make_pdf(self, outfile):
        pdf = PDF('L', 'mm', 'letter')
        pdf.set_auto_page_break(auto=False, margin = 20)
        for c in sorted(self.classes, key=sort_classes):
            pdf.add_page()
            pdf.set_col(0)
            pdf.set_font('Arial', 'B', 18)
            pdf.cell(98, 15, "{}".format(c))
            pdf.ln()
            previous_student_name = ''
            for s in [s for s in self.students if s.classname == c]:
                if pdf.y > 174:
                    pdf.accept_page_break()
                if s.student_name != previous_student_name:
                    pdf.set_font('Arial', 'B', 10)
                    pdf.cell(40, 6, "{}".format(s.student_name))
                    pdf.ln() 
                for p in s.guardians:
                    pdf.set_font('Arial', '', 10)
                    out = "{}".format(p['name'])
                    try:
                        out += ": {}".format(p['email'])
                        out += ", {}".format(p['phone'])
                    except KeyError:
                        pass
                    out += "\n"
                    pdf.set_x(pdf.x + 6)
                    pdf.multi_cell(120, 5, txt=out, border=0, align='L')
#                     pdf.ln()
                previous_student_name = s.student_name
            pdf.ln()
        pdf.output(outfile, 'F')

class Student:
    def __init__(self,row,columns):
        self.student_name = row[1]
        self.columns = columns
        try:
            if row[self.columns.index("pk_class")] == "":
                self.classname = row[self.columns.index("teacher_name")]
            else:
                self.classname = "{} ({})".format(row[self.columns.index("teacher_name")],row[self.columns.index("pk_class")])
        except IndexError:
            self.classname = row[self.columns.index("teacher_name")]
        self.guardians = []
        if str(row[self.columns.index("guardian1_name")]):
            # guardian 1
            guardian1 = {"name": row[self.columns.index("guardian1_name")]}
            if str(row[self.columns.index("guardian1_email")]):
                guardian1['email'] = row[self.columns.index("guardian1_email")]
            phone = ''
            if str(row[self.columns.index("guardian1_phone")]):
                phone = formatPhone(row[self.columns.index("guardian1_phone")])
                if len(phone) > 0:
                    guardian1['phone'] = phone
            self.guardians.append(guardian1)
        if str(row[self.columns.index("guardian2_name")]):
            # guardian 2
            guardian2 = {"name": row[self.columns.index("guardian2_name")]}
            if str(row[self.columns.index("guardian2_email")]):
                guardian2['email'] = row[self.columns.index("guardian2_email")]
            phone = ''
            if str(row[self.columns.index("guardian2_phone")]):
                phone = formatPhone(row[self.columns.index("guardian2_phone")])
                if len(phone) > 0:
                    guardian2['phone'] = phone
            self.guardians.append(guardian2)

    def __str__(self):
        return "Student name: {} – {}\n\t{}".format(self.student_name, self.classname, str(self.guardians))

def sort_classes(classname):
    if classname.startswith("PreK"):
        return "0 {}".format(classname)
    if classname.startswith("K:"):
        return "1 {}".format(classname)
    else:
        return classname

def formatPhone(phone):
    try:
        raw = phonenumbers.parse(phone, "US")
    except phonenumbers.NumberParseException:
        return ""
    if phonenumbers.is_valid_number(raw):
        formattedPhone = phonenumbers.format_number(raw, phonenumbers.PhoneNumberFormat.NATIONAL)
    else:
        formattedPhone = ""
    return formattedPhone

def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--infile', help="Input file")
    parser.add_argument('-o', '--outfile', help="Output file")

    args = parser.parse_args(arguments)
    
    directory = Directory(str(args.infile))
#     print(directory.classes)
#     print(directory)
    directory.make_pdf(args.outfile)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
