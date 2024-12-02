#!/usr/bin/python3

from shared import data

print(len([report for report in data() if report.safe]))

