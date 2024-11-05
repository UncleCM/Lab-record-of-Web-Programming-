const daysOfMonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        const monthNames = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"];
        let currentMonth = 0;  // Jan
        let currentYear = 2024;
    function showMonthOf2024(month) {
        const totalDays = daysOfMonth[month];
        const firstDay = new Date(currentYear, month, 1).getDay();
        const startDay = (firstDay === 0) ? 6 : firstDay - 1;
        const calendarBody = document.getElementById("calendar-body");
        const monthYearDisplay = document.getElementById("month-year");
        calendarBody.innerHTML = "";
        monthYearDisplay.textContent = `${monthNames[month]} / ${currentYear}`;
        let date = 1;
        for (let i = 0; i < 6; i++) {
            const row = document.createElement("tr");
            for (let j = 0; j < 7; j++) {
                const cell = document.createElement("td");
                if (i === 0 && j < startDay) {
                    cell.innerHTML = "";
                } else if (date > totalDays) {
                    cell.innerHTML = "";
                } else {
                    cell.innerHTML = date;
                    date++;
                }
                if (j == 6) {
                    cell.style.color = "red";
                }
                row.appendChild(cell);
            }
            calendarBody.appendChild(row);
        }
        document.getElementById("prev").addEventListener("click", () => {
            if (currentMonth === 0) {
                currentMonth = 0; 
            } else {
                currentMonth--;
            }
            showMonthOf2024(currentMonth);
        });

        document.getElementById("next").addEventListener("click", () => {
            if (currentMonth === 11) {
                currentMonth = 11; 
            } else {
                currentMonth++;
            }
            showMonthOf2024(currentMonth);
        });

    }