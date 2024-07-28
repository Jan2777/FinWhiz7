
<h1>Overview</h1>
Finwhiz is a financial analysis web application designed to help users evaluate their financial health through various tools, including stock market analysis, mutual fund performance tracking, and personalized financial planning. The application provides users with insightful visualizations and actionable recommendations.

<h1>Features</h1>h1>
<2>Stock Market Analysis:</h2>
  Analyze stock performance using TensorFlow-based forecasting.
<h2>Mutual Fund Performance:</h2> 
  Evaluate mutual fund investments with detailed metrics.
<h2>Financial Planning Tools:</h2> 
  Create personalized financial plans based on user inputs.
<h2>Visualizations:
  Interactive charts using Chart.js to visualize financial data.
<h2>AI Chatbot:</h2> 
  Integrated chatbot to assist users with queries and navigation.
<h2>User-Friendly Interface: </h2>
Clean and intuitive design for a better user experience.

<h1>Prerequisites</h1>

Python 3.x
Django 3.x or higher
Node.js (for front-end dependencies)
Steps
<h1>Clone the Repository</h2>

bash
Copy code
git clone https://github.com/yourusername/finwhiz.git
cd finwhiz
Create a Virtual Environment

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Set Up Database

bash
Copy code
python manage.py migrate
Run the Development Server

bash
Copy code
python manage.py runserver
Open Your Browser
Visit http://127.0.0.1:8000 to see the application in action.

<h1>Usage</h1>
<b>Home Page</b>
The home page provides a brief overview of Finwhiz and navigation options to different features.
<b>Financial Planning</b>
Users can input financial goals (e.g., saving for a house, education) through an interactive form.
Upon submission, results and recommendations are displayed based on user input.
<b>Stock Market Analysis</b>
Users can analyze stock performance and forecast trends.
Visualizations provide insights into historical and predicted stock values.
<b>Mutual Fund Performance</b>
Evaluate mutual funds with various metrics, including ROI and risk assessment.
<b>AI Chatbot</b>
Access the chatbot for assistance navigating the application and answering common queries.

Screenshots

Home Page
<img width="938" alt="Screenshot 2024-07-28 145719" src="https://github.com/user-attachments/assets/6636861a-bdcf-49fa-bf5d-b39675ff5305">
<img width="887" alt="Screenshot 2024-07-28 145857" src="https://github.com/user-attachments/assets/62970ad5-5cb8-480c-b9f8-f11d150ba715">


Description: This screenshot shows the Finwhiz home page with navigation links.

Financial Checkup
<img width="938" alt="Screenshot 2024-07-28 150121" src="https://github.com/user-attachments/assets/cf09fbaa-37eb-4410-a720-35a1e4d0c135">
<img width="343" alt="Screenshot 2024-07-28 150228" src="https://github.com/user-attachments/assets/c4ed91a3-2e0f-421a-8873-d9d4f146b2fd">
<img width="950" alt="Screenshot 2024-07-28 150326" src="https://github.com/user-attachments/assets/40fbb7e7-4d66-4237-8081-5fa5b0033ea6">


Description: This screenshot illustrates the financial checkup page and results where you stand on a generic basis , it porvides interface where users input their financial status/standing.

Financial Planning
<img width="861" alt="Screenshot 2024-07-28 154700" src="https://github.com/user-attachments/assets/2a60a4a8-5bb5-432f-a532-251d6bc17476">
<img width="242" alt="Screenshot 2024-07-28 154548" src="https://github.com/user-attachments/assets/d4ad92c8-1cca-4032-8768-eee21cc73462">

Personalized planning portotype

Stock Market Analysis and Mutual Fund Recommendations with Forecasting(LSTM)

Description: Here, users can view stock performance graphs and forecasts.
<img width="937" alt="Screenshot 2024-07-28 150927" src="https://github.com/user-attachments/assets/4533ab59-39d2-4b90-bd84-5a<img width="947" alt="Screenshot 2024-07-28 150957" src="https://github.com/user-attachments/assets/2a049fa1-b636-4d3c-bcfb-bb171fcdf6a8">
19caff17bd">

<img width="418" alt="Screenshot 2024-07-28 150715" src="https://github.com/user-attachments/assets/5c42c9e4-45e2-4dcd-8ce2-c146c64126b6">

Description: This shows the metrics for evaluating mutual fund performance.

AI Chatbot

Description: The integrated AI chatbot helps users navigate the application.

Contributing
We welcome contributions from the community! To contribute:

Fork the repository.
Create a new branch.
Make your changes.
Submit a pull request with a detailed description of your changes.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For any inquiries or feedback, please contact:

jan.narayanan27@gmail.com
