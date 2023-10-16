# HaveIBeenPwnedAnalyzer
Search if any passwords are contained within the HIBP passwords hash list file.
The script reads a file with a newline seperated list of clear text passwords.
The script passes the passwords through sha1 and compares against HIBP passwords hash list file.
Results are delivered via a CSV file. Everything runs local.
If you don't have the HIBP passwords file, you can generate one through https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader.

I used pinae's code for the core functionality and built around it. Thank you Pina Merkert.
https://github.com/pinae/HaveIBeenPwnedOffline
