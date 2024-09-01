# csv_transformer

csv_transformer is a useful little tool that can convert CSV tables into the format I need.

The background is that I downloaded a lot of customer data from the appllo platform, and then I need to import this data into the Zoho system in batches.

At this time, I encountered some troubles. The header of the appllo table did not completely match the information required by Zoho, which made the table unable to upload.

At first, I could only modify the appllo table one by one according to the information required by Zoho. Later, I thought that I might need to repeat the same work many times in the future, so why not leave this work to the code?

So I wrote a simple script in Python, which will read the CSV file I uploaded and convert it into the format I need.

The process is as follows:

1. I put the CSV file into the folder where the script is located (of course you can specify any folder);
2. The script listens to the event and reads the file;
3. The script completes the columns that need to be deleted, modified, and added one by one;
4. The script puts the newly generated CSV file into the folder I specified.

After the script is completed, the test is fine, which is great.

At this time, I thought of a question, what if I want to give this script to others to use? Of course, they can install pyCharm and Python, then install all the required dependencies, such as pandas, and then run the script.

But the cost of use is too high. For people who don’t know how to code, it’s better to operate the csv file manually.

So I thought I could build this script.

> PyInstaller bundles a Python application and all its dependencies into a single package. The user can run the packaged app without installing a Python interpreter or any modules.

So I installed PyInstaller, which generated a simple transform file for me. I can share it with everyone who needs it. They can just double-click the file and run it to transform the file.

Anyone who needs this little tool can clone the code in the repository and modify some parameters in the code to transform their own files.

Cheers!
