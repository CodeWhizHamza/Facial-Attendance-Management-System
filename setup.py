from distutils.core import setup
import py2exe

setup(windows=['main.py'], py_modules=['add_student.py', 'attendance.py', 'config.py', 'student_report.py',
      'delete_student.py', 'edit_student_details.py', 'getTotalAttendanceReport.py', 'helper.py', 'student_list.py'], zip=None, options={
    "py2exe": {
        "compressed": True,
        "bundle-files": 1
    }
})
