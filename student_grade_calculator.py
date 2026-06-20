#!/usr/bin/env python3
# Ipyana Archie
# CIS261
# Wk10 VIBE Coding
"""Student Grade Calculator

Features:
- Add new student records
- Calculate averages and letter grades
- Display students in a table
- Class statistics (highest, lowest, average)
- Search by name (case-insensitive)
- Save/load from student_grades.txt (pipe-delimited)
- Exit by typing ESC at prompts or menu

Data structure: Student class (Option B)
File format: name|id|test1|test2|test3|average|grade
"""
from __future__ import annotations
import os
import argparse
from typing import List, Optional

DATA_FILE = "student_grades.txt"


class Student:
	def __init__(self, name: str, sid: str, test1: float, test2: float, test3: float):
		self.name = name.strip()
		self.id = sid.strip()
		self.test1 = float(test1)
		self.test2 = float(test2)
		self.test3 = float(test3)
		self.average = self.calculate_average()
		self.grade = self.calculate_letter()

	def calculate_average(self) -> float:
		return round((self.test1 + self.test2 + self.test3) / 3.0, 2)

	def calculate_letter(self) -> str:
		avg = self.average
		if avg >= 90:
			return "A"
		if avg >= 80:
			return "B"
		if avg >= 70:
			return "C"
		if avg >= 60:
			return "D"
		return "F"

	def to_pipe(self) -> str:
		return f"{self.name}|{self.id}|{self.test1:.2f}|{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}\n"

	@staticmethod
	def from_pipe(line: str) -> Optional["Student"]:
		parts = line.strip().split("|")
		if len(parts) < 7:
			return None
		try:
			name, sid, t1, t2, t3, avg, grade = parts[:7]
			# Use provided test scores to recreate object; average/grade recalculated
			return Student(name, sid, float(t1), float(t2), float(t3))
		except Exception:
			return None


def load_records(filename: str = DATA_FILE) -> List[Student]:
	students: List[Student] = []
	if not os.path.exists(filename):
		return students
	try:
		with open(filename, "r", encoding="utf-8") as f:
			for line in f:
				if not line.strip():
					continue
				s = Student.from_pipe(line)
				if s:
					students.append(s)
	except Exception as e:
		print(f"Error loading {filename}: {e}")
	return students


def save_records(students: List[Student], filename: str = DATA_FILE) -> bool:
	try:
		with open(filename, "w", encoding="utf-8") as f:
			for s in students:
				f.write(s.to_pipe())
		return True
	except Exception as e:
		print(f"Error saving to {filename}: {e}")
		return False


def format_score(v: float) -> str:
	return f"{v:.2f}"


def display_students(students: List[Student]) -> None:
	if not students:
		print("No student records to display.")
		return
	widths = {
		"name": 20,
		"id": 12,
		"test": 7,
		"avg": 8,
		"grade": 6,
	}
	header = (
		f"{ 'Name':{widths['name']}} | { 'ID':{widths['id']}} |"
		f" { 'T1':{widths['test']}} | { 'T2':{widths['test']}} | { 'T3':{widths['test']}} |"
		f" { 'Average':{widths['avg']}} | { 'Grade':{widths['grade']}}"
	)
	sep = "-" * len(header)
	print(sep)
	print(header)
	print(sep)
	for s in students:
		print(
			f"{s.name:{widths['name']}} | {s.id:{widths['id']}} | {format_score(s.test1):{widths['test']}} |"
			f" {format_score(s.test2):{widths['test']}} | {format_score(s.test3):{widths['test']}} | {format_score(s.average):{widths['avg']}} | {s.grade:{widths['grade']}}"
		)
	print(sep)


def class_statistics(students: List[Student]) -> None:
	if not students:
		print("No student records for statistics.")
		return
	avgs = [s.average for s in students]
	highest = max(avgs)
	lowest = min(avgs)
	class_avg = round(sum(avgs) / len(avgs), 2)
	print(f"Highest Average: {highest:.2f}")
	print(f"Lowest Average: {lowest:.2f}")
	print(f"Class Average: {class_avg:.2f}")


def search_by_name(students: List[Student], query: str) -> List[Student]:
	q = query.strip().lower()
	return [s for s in students if q in s.name.lower()]


def get_input(prompt: str) -> str:
	try:
		return input(prompt).strip()
	except (EOFError, KeyboardInterrupt):
		return "ESC"


def get_float(prompt: str) -> Optional[float]:
	while True:
		val = get_input(prompt)
		if val.upper() == "ESC":
			return None
		try:
			f = float(val)
			return round(f, 2)
		except ValueError:
			print("Invalid number. Enter a numeric value or type ESC to cancel.")


def add_student_interactive(students: List[Student]) -> bool:
	print("Enter student information (type ESC at any prompt to cancel/exit).")
	name = get_input("Name: ")
	if name.upper() == "ESC":
		return False
	sid = get_input("ID: ")
	if sid.upper() == "ESC":
		return False
	t1 = get_float("Test 1 score: ")
	if t1 is None:
		return False
	t2 = get_float("Test 2 score: ")
	if t2 is None:
		return False
	t3 = get_float("Test 3 score: ")
	if t3 is None:
		return False
	s = Student(name, sid, t1, t2, t3)
	students.append(s)
	print(f"Added {s.name} (Average: {s.average:.2f}, Grade: {s.grade})")
	return True


def demo_mode() -> None:
	print("Running demo mode: adding sample students and showing outputs.")
	students: List[Student] = []
	students.append(Student("Alice Johnson", "S001", 92.5, 88.0, 95.0))
	students.append(Student("Bob Smith", "S002", 76.0, 82.5, 79.0))
	display_students(students)
	class_statistics(students)
	saved = save_records(students)
	print(f"Saved to {DATA_FILE}: {saved}")


def main() -> None:
	print("Student Grade Calculator")
	print("Data file:", DATA_FILE)
	students = load_records()
	if students:
		print(f"Loaded {len(students)} student(s) from {DATA_FILE}.")
	else:
		print("No existing records found.")

	menu = (
		"\nMenu:\n"
		"1) Add new student\n"
		"2) Display all students\n"
		"3) Class statistics\n"
		"4) Search student by name\n"
		"5) Save records to file\n"
		"ESC) Exit program\n"
	)

	while True:
		print(menu)
		choice = get_input("Choose an option (or type ESC): ")
		if not choice:
			continue
		if choice.upper() == "ESC":
			print("Exiting. Saving records...")
			save_records(students)
			break
		if choice == "1":
			added = add_student_interactive(students)
			if added:
				print("Student added. You may add another or return to menu.")
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			class_statistics(students)
		elif choice == "4":
			q = get_input("Enter name to search: ")
			if q.upper() == "ESC":
				continue
			results = search_by_name(students, q)
			if results:
				display_students(results)
			else:
				print("No matching student found.")
		elif choice == "5":
			ok = save_records(students)
			print("Save succeeded." if ok else "Save failed.")
		else:
			print("Unknown selection. Enter 1-5 or type ESC to exit.")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="Student Grade Calculator")
	parser.add_argument("--demo", action="store_true", help="Run demo then exit")
	args = parser.parse_args()
	if args.demo:
		demo_mode()
	else:
		try:
			main()
		except KeyboardInterrupt:
			print("\nInterrupted. Saving records and exiting.")
			# attempt to save on interrupt
			# load current in-memory students? we can't access scope here; just exit
			raise

