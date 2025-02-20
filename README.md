# TrainPass-SNCF
 TrainPass SNCF is a Flask-based web application that allows users to book train tickets for high-speed and regional trains in France. The system integrates an interactive train selection, seat reservation, and QR code generation for ticket validation, providing a smooth and efficient booking experience.
 
Key Features
✅ Train Selection – Users can choose a train from the real-time schedule stored in a CSV file and database. The departure and arrival times are automatically fetched and displayed.
✅ Seat Reservation – An interactive wagon layout allows users to select seats, with occupied ones marked dynamically.
✅ QR Code Generation – Each ticket generates a unique QR code containing passenger details, train information, and travel class for easy validation.
✅ Dashboard & Data Visualization – The app includes a dashboard with interactive charts built using Pandas and Plotly, displaying:

Number of reservations per destination 📊
Ticket types distribution 🎫
Payment method statistics 💳
✅ Admin Panel – Admins can add, edit, or remove trains from the system and update real-time schedules.
Technologies Used
Backend: Flask, SQLAlchemy (SQLite database)
Frontend: HTML, CSS (Responsive UI), JavaScript
Data Handling: Pandas for processing train schedules
Visualization: Plotly (interactive charts in the dashboard)
Storage: SQLite, CSV file for train schedules
QR Code: qrcode library for digital ticketing
Objective
This project aims to create a modern, efficient, and user-friendly train ticketing system that integrates real-time scheduling, seat management, and interactive dashboards. By leveraging Flask, SQLAlchemy, Pandas, and Plotly, the application provides data-driven insights for train ticket sales while enhancing customer experience with an easy-to-use online booking system.

