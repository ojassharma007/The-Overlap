# Django Football Project

## Overview
The Django Football project is a web application designed to provide football-related information, including leagues, live fixtures, player stats, and standings. It features a responsive design and interactive UI components.

## Features
- Display football leagues and their details.
- Live fixtures and match updates.
- Player statistics and team standings.
- User-friendly navigation and responsive design.

## Technologies Used
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default) or any Django-supported database
- **Styling**: Custom CSS with responsive design

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ojas2708/Football.git
   cd Football
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:8000`.

## Usage
- Navigate through the application to explore leagues, fixtures, and player stats.
- Use the admin panel for managing data (accessible at `/admin`).

## Folder Structure
- **templates/**: Contains HTML templates for the application.
- **static/**: Includes CSS, JavaScript, and image files.
- **apps/**: Custom Django apps for handling specific functionalities.
- **manage.py**: Django's command-line utility for administrative tasks.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## Contact
For any inquiries or support, please contact at [LinkedIn/ojassharma007](http://linkedin.com/in/ojassharma007/). 