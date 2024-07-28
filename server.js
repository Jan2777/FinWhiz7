const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.post('/run-script', (req, res) => {
    const salary = req.body.salary;
    const scriptPath = path.join(__dirname, 'script.py'); // Adjust path to your Python script

    const { exec } = require('child_process');
    exec(`python ${scriptPath} ${salary}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).json({ error: 'Internal server error' });
        }

        // Read the results from JSON file
        const jsonFilePath = path.join(__dirname, 'results.json');
        fs.readFile(jsonFilePath, 'utf8', (err, data) => {
            if (err) {
                console.error('Error reading JSON file:', err);
                return res.status(500).json({ error: 'Internal server error' });
            }

            // Clear the JSON file
        

            res.json(JSON.parse(data));
        });
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
