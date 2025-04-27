# Flask Boilerplate

This repository contains a simple Flask boilerplate for building web applications (mostly SaaS) with user authentication, key-based subscriptions, and an admin panel for managing activation keys.

## Features

- **User Authentication:**  
  - Registration and login via `/auth`.
  - User dashboard with key redemption.
  
- **Admin Panel:**  
  - Access via `/admin` using a configured admin password.
  - Generate and delete activation keys.
  
- **Key Redemption:**  
  - Keys stored in a JSON file.
  - Redeem activation keys to update user subscription tiers.

- **File-based Storage:**  
  - Uses JSON files (`users.json` and `keys.json`) for data storage during development.

- **Front-end:**
  - Simple-to-understand HTML
  - Responsive design with custom CSS.
  - Simple JavaScript for form handling and flash messages.

## Repository Structure

```
├── app.py                  # Main Flask application
├── users.json              # User data storage
├── keys.json               # Activation keys storage
├── templates               # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Homepage
│   ├── auth.html           # Login/Register page
│   ├── dashboard.html      # User dashboard
│   └── admin.html          # Admin panel
└── static
    ├── css
    │   ├── styles.css      # Global styles
    │   └── auth.css        # Styles for authentication pages
    └── js
        ├── main.js         # Main JavaScript file (flash messages)
        ├── auth.js         # JS for login/register tab switching
        └── dashboard.js    # JS for key redemption
```

## Setup & Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/hiatus01/flask-boilerplate.git
    cd your-flask-boilerplate
    ```

2. **Set Up a Virtual Environment (Optional but Recommended):**

    ```bash
    python -m venv venv
    venv\Scripts\activate   # Windows
    # or for Unix-based systems
    source venv/bin/activate
    ```

3. **Install the Required Packages:**

    ```bash
    pip install flask werkzeug
    ```

4. **Initialize the Database:**

   The application will automatically create `users.json` and `keys.json` if they do not exist when you run the server.

5. **Run the Application:**

    ```bash
    python app.py
    ```

   The app should now be running at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Configuration

- **Secret Key:**  
  Update the `app.secret_key` in `app.py` for production.

- **Admin Password:**  
  The default admin password is set to `admin123` in `app.py`. For production, update this value or handle it using environment variables.

## Usage

- **User Registration / Login:**  
  Users can register or log in via the `/auth` endpoint.

- **Dashboard & Key Redemption:**  
  After logging in, users can access `/dashboard` and redeem keys to upgrade their account subscriptions. This is where your app content should go

- **Admin Panel:**  
  Visit `/admin` to log in as an admin. Once authenticated, you can generate a new key by selecting a subscription tier or delete an existing key by its value.

## Customization

Feel free to adjust templates, styles, and functionality as needed. This boilerplate is intended as a simple starting point for your Flask applications.

## Contributions

Contributions and suggestions are welcome!

## License

This project is provided as-is without any warranty. See the [LICENSE](LICENSE) file for details.
