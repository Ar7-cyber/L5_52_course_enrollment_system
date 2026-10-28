"""Course enrollment system with security and code quality improvements."""
import hashlib
import secrets
from pathlib import Path
COURSES = {
    "CS101": {
        "title": "Data Structures",
        "seats": 3,
        "fee": 500.0,
        "is_closed": False,
    },
    "CS202": {
        "title": "Operating Systems",
        "seats": 0,
        "fee": 550.0,
        "is_closed": True,
    },
    "CS303": {
        "title": "Compiler Design",
        "seats": 4,
        "fee": 600.0,
        "is_closed": False,
    },
}


def enroll_student(
    course_id, student_name, credits_registered=3, audit_trail=None
):
    """Enroll a student if the requested course is open and has seats."""
    if audit_trail is None:
        audit_trail = []
    if course_id not in COURSES or COURSES[course_id]["is_closed"]:
        return False
    course = COURSES[course_id]
    if course["seats"] <= 0:
        course["is_closed"] = True
        return False
    course["seats"] -= 1
    if course["seats"] == 0:
        course["is_closed"] = True
    audit_trail.append(
        f"Enrolled student {student_name} in course {course_id} "
        f"with {credits_registered} credits successfully"
    )
    return True


def drop_course(course_id):
    """Drop a course enrollment and restore one seat when appropriate."""
    course = COURSES.get(course_id)
    if course is None:
        return False
    course["seats"] += 1
    course["is_closed"] = False
    return True


def check_course_status(course_id):
    """Return whether the specified course is open."""
    course = COURSES.get(course_id)
    if course is None:
        return False
    return not course["is_closed"]


def calculate_scholarship_tuition(course_id, discount_rate):
    """Calculate tuition after applying a validated discount rate."""
    if course_id not in COURSES:
        raise ValueError(f"Unknown course: {course_id}")
    if not isinstance(discount_rate, (int, float)):
        raise TypeError("Discount rate must be numeric.")
    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")
    base_fee = COURSES[course_id]["fee"]
    return base_fee * (1 - discount_rate)


def generate_student_hash(roll_no):
    """Generate a SHA-256 digest for a student roll number."""
    return hashlib.sha256(roll_no.encode("utf-8")).hexdigest()


def generate_enrollment_otp():
    """Generate a cryptographically secure four-digit enrollment OTP."""
    return f"{secrets.randbelow(9000) + 1000:04d}"


def export_course_roster(filename="course_roster.txt"):
    """Export course information to a UTF-8 text file."""
    output_path = Path(filename)
    output_path.write_text(str(COURSES), encoding="utf-8")
    print(f"Course roster exported to: {output_path}")


def get_open_courses_summary(course_catalog):
    """Return the number of courses that are currently open."""
    return sum(
        1
        for details in course_catalog.values()
        if not details["is_closed"]
    )


def main():
    """Run the course enrollment demonstration."""
    enroll_student("CS101", "Kritika", 4)
    drop_course("CS202")
    print("Is CS101 open:", check_course_status("CS101"))
    print(
        "Scholarship Fee:",
        calculate_scholarship_tuition("CS303", 0.25),
    )
    print("Student Hash:", generate_student_hash("REG_2026_091"))
    print("Enrollment OTP:", generate_enrollment_otp())
    export_course_roster()
    print("Open courses:", get_open_courses_summary(COURSES))
    registrar_auth_token = secrets.token_urlsafe(32)
    print(
        "Registrar Token active:",
        bool(registrar_auth_token),
    )


if __name__ == "__main__":
    main()
