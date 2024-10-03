html_template = """
<html>
<head>
    <meta charset="UTF-8">
    <title>Conversion Successful</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #333;
        }}
        p {{
            color: #555;
            line-height: 1.6;
        }}
        .download-link {{
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            color: #fff;
            background-color: #007bff;
            border-radius: 5px;
            text-decoration: none;
        }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Conversion Successful!</h1>
        <p>Your video has been successfully converted into MP3.</p>
        <p>Click the link below to download your MP3 file:</p>
        <a href="{download_link}" class="download-link">Download MP3</a>
        <p class="footer">Thank you for using our conversion service!</p>
    </div>
</body>
</html>
"""

__all__ = ["html_template"]

# <a href="{donwload_svc}/?file_name={mp3_filename}" class="download-link">Download MP3</a>
