document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById('jsonFileInput');

    fileInput.addEventListener('change', handleFileUpload);

    function handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) {
            alert("Please select a JSON file first.");
            return;
        }

        const reader = new FileReader();
        reader.onload = (event) => {
            const data = JSON.parse(event.target.result);
            populateTranscriptData(data);
        };
        reader.readAsText(file);
    }

    function populateTranscriptData(data) {
        populateStudentInfo(data);
        populateTranscriptTable(data);
    }

    function populateStudentInfo(data) {
        const studentInfoFields = [
            { id: "student-name", value: data.student_name },
            { id: "dob", value: data.date_of_birth },
            { id: "admission-date", value: data.date_of_admission },
            { id: "degree", value: data.degree },
            { id: "major", value: data.major },
            { id: "student-id", value: data.student_id },
            { id: "grad-date", value: data.date_of_graduation }
        ];

        studentInfoFields.forEach(field => {
            document.getElementById(field.id).value = field.value;
        });
    }

    function populateTranscriptTable(data) {
        const tbody = document.querySelector("table tbody");
        tbody.innerHTML = ""; // Clear existing table content

        let totalCredits = 0;
        let totalGradePoints = 0;

        const years = Object.keys(data.credit);
        years.forEach((year) => {
            const semesters = Object.keys(data.credit[year]);
            semesters.forEach((semester) => {
                let semesterCredits = 0;
                let semesterGradePoints = 0;

                // Append semester header
                appendSemesterHeader(tbody, semester, year);

                const courses = Array.isArray(data.credit[year][semester])
                    ? data.credit[year][semester]
                    : [data.credit[year][semester]];

                // Append course rows and calculate credits/grade points
                courses.forEach((course) => {
                    appendCourseRow(tbody, course);
                    const gradePoint = getGradePoint(course.grade);
                    const courseCredits = parseFloat(course.credit);
                    semesterCredits += courseCredits;
                    semesterGradePoints += courseCredits * gradePoint;
                    totalCredits += courseCredits;
                    totalGradePoints += courseCredits * gradePoint;
                });

                // Append semester summary row
                appendSummaryRow(tbody, semesterCredits, semesterGradePoints, totalCredits, totalGradePoints);
            });
        });
    }

    function appendSemesterHeader(tbody, semester, year) {
        const semesterHeaderRow = document.createElement("tr");
        const semesterHeaderCell = document.createElement("td");
        semesterHeaderCell.colSpan = 6;
        semesterHeaderCell.textContent = `${semester}, ${year}`;
        semesterHeaderCell.classList.add("semester-header");
        semesterHeaderRow.appendChild(semesterHeaderCell);
        tbody.appendChild(semesterHeaderRow);
    }

    function appendCourseRow(tbody, course) {
        const row = document.createElement("tr");
        const courseTitleCell = createTableCell(`${course.subject_id} - ${course.name}`);
        const creditCell = createTableCell(course.credit);
        const gradeCell = createTableCell(course.grade);

        row.appendChild(courseTitleCell);
        row.appendChild(creditCell);
        row.appendChild(gradeCell);

        tbody.appendChild(row);
    }

    function appendSummaryRow(tbody, semesterCredits, semesterGradePoints, totalCredits, totalGradePoints) {
        const gps = (semesterGradePoints / semesterCredits).toFixed(2);
        const gpa = (totalGradePoints / totalCredits).toFixed(2);

        const summaryRow = document.createElement("tr");
        const summaryCell = createTableCell(`GPS: ${gps}, GPA: ${gpa}`, 6);
        summaryCell.classList.add("summary-row");
        summaryRow.appendChild(summaryCell);
        tbody.appendChild(summaryRow);
    }

    function createTableCell(content, colSpan = 1) {
        const cell = document.createElement("td");
        cell.colSpan = colSpan;
        cell.textContent = content;
        return cell;
    }
    
    function getGradePoint(grade) {
        const gradePoints = {
            "A": 4.0,
            "B+": 3.5,
            "B": 3.0,
            "C+": 2.5,
            "C": 2.0,
            "D+": 1.5,
            "D": 1.0,
            "F": 0.0
        };
        return gradePoints[grade] || 0.0;
    }
});
