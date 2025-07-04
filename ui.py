

################################  works 🤌🏼  voice ko output terminal mai dekhauncha simple cha ramro cha ########################################################
# import sys
# import os
# from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
# from PyQt5.QtCore import QThread
# import subprocess

# class ScriptThread(QThread):
#     def __init__(self, script_name):
#         super().__init__()
#         self.script_name = script_name
#         self.process = None  # Store the subprocess.Popen object

#     def run(self):
#         try:
#             script_path = os.path.abspath(self.script_name)
#             self.process = subprocess.Popen([sys.executable, script_path])  # Use Popen instead of run
#             self.process.wait()  # Wait for the process to complete
#         except subprocess.CalledProcessError as e:
#             print(f"Error running {self.script_name}: {e}")

#     def terminate_script(self):
#         if self.process:
#             self.process.terminate()  # Terminate the running process
#             self.process = None

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.threads = {}  # Store threads for each script
#         self.initUI()

#     def initUI(self):
#         layout = QVBoxLayout()

#         # Button for Voice Assistant
#         self.button1 = QPushButton("Voice Assistant", self)
#         self.button1.clicked.connect(lambda: self.run_script("for_nepali.py", "voice_assistant"))
#         layout.addWidget(self.button1)

#         # Terminate button for Voice Assistant
#         self.terminate_button1 = QPushButton("Terminate Voice Assistant", self)
#         self.terminate_button1.clicked.connect(lambda: self.terminate_script("voice_assistant"))
#         layout.addWidget(self.terminate_button1)

#         # Button for FileZ2
#         self.button2 = QPushButton("VirtualMouse", self)
#         self.button2.clicked.connect(lambda: self.run_script("AiVirtualMouseProject.py", "filez2"))
#         layout.addWidget(self.button2)

#         # Terminate button for FileZ2
#         self.terminate_button2 = QPushButton("Terminate V-mouse", self)
#         self.terminate_button2.clicked.connect(lambda: self.terminate_script("filez2"))
#         layout.addWidget(self.terminate_button2)

#         self.setLayout(layout)
#         self.setWindowTitle("Control Panel")
#         self.setGeometry(300, 300, 300, 200)  # Increased height to fit terminate buttons

#     def run_script(self, script_name, thread_key):
#         if thread_key in self.threads:
#             self.threads[thread_key].terminate_script()  # Terminate if already running
#         self.threads[thread_key] = ScriptThread(script_name)
#         self.threads[thread_key].start()

#     def terminate_script(self, thread_key):
#         if thread_key in self.threads:
#             self.threads[thread_key].terminate_script()  # Terminate the script

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWin = MainWindow()
#     mainWin.show()
#     sys.exit(app.exec_())





#yo ramrari kam garcha tara voice assistant ko output dekhaudaina terminal ma, esma status ni cha ki running or stopped


# import sys
# import os
# from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QTextEdit
# from PyQt5.QtCore import QThread
# import subprocess

# class ScriptThread(QThread):
#     def __init__(self, script_name, log_text):
#         super().__init__()
#         self.script_name = script_name
#         self.process = None  # Store the subprocess.Popen object
#         self.log_text = log_text  # QTextEdit for logging

#     def run(self):
#         try:
#             script_path = os.path.abspath(self.script_name)
#             self.process = subprocess.Popen(
#                 [sys.executable, script_path],
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True
#             )
#             stdout, stderr = self.process.communicate()
#             if stdout:
#                 self.log_text.append(stdout)
#             if stderr:
#                 self.log_text.append(stderr)
#         except subprocess.CalledProcessError as e:
#             self.log_text.append(f"Error running {self.script_name}: {e}")

#     def terminate_script(self):
#         if self.process:
#             self.process.terminate()  # Terminate the running process
#             self.process = None

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.threads = {}  # Store threads for each script
#         self.initUI()

#     def initUI(self):
#         layout = QVBoxLayout()

#         # Button for Voice Assistant
#         self.button1 = QPushButton("Voice Assistant", self)
#         self.button1.clicked.connect(lambda: self.run_script("for_nepali.py", "voice_assistant"))
#         layout.addWidget(self.button1)

#         # Terminate button for Voice Assistant
#         self.terminate_button1 = QPushButton("Terminate Voice Assistant", self)
#         self.terminate_button1.clicked.connect(lambda: self.terminate_script("voice_assistant"))
#         self.terminate_button1.setEnabled(False)
#         layout.addWidget(self.terminate_button1)

#         # Status label for Voice Assistant
#         self.status_label1 = QLabel("Status: Stopped", self)
#         layout.addWidget(self.status_label1)

#         # Button for VirtualMouse
#         self.button2 = QPushButton("VirtualMouse", self)
#         self.button2.clicked.connect(lambda: self.run_script("AiVirtualMouseProject.py", "filez2"))
#         layout.addWidget(self.button2)

#         # Terminate button for VirtualMouse
#         self.terminate_button2 = QPushButton("Terminate V-mouse", self)
#         self.terminate_button2.clicked.connect(lambda: self.terminate_script("filez2"))
#         self.terminate_button2.setEnabled(False)
#         layout.addWidget(self.terminate_button2)

#         # Status label for VirtualMouse
#         self.status_label2 = QLabel("Status: Stopped", self)
#         layout.addWidget(self.status_label2)

#         # Log text box
#         self.log_text = QTextEdit(self)
#         self.log_text.setReadOnly(True)
#         layout.addWidget(self.log_text)

#         self.setLayout(layout)
#         self.setWindowTitle("Control Panel")
#         self.setGeometry(300, 300, 400, 300)  # Adjusted size for additional widgets

#     def run_script(self, script_name, thread_key):
#         if thread_key in self.threads:
#             self.threads[thread_key].terminate_script()  # Terminate if already running
#         self.threads[thread_key] = ScriptThread(script_name, self.log_text)
#         self.threads[thread_key].start()
#         self.update_button_states(thread_key, running=True)
#         self.update_status_labels(thread_key, "Running")

#     def terminate_script(self, thread_key):
#         if thread_key in self.threads:
#             self.threads[thread_key].terminate_script()  # Terminate the script
#         self.update_button_states(thread_key, running=False)
#         self.update_status_labels(thread_key, "Stopped")

#     def update_button_states(self, thread_key, running):
#         if thread_key == "voice_assistant":
#             self.button1.setEnabled(not running)
#             self.terminate_button1.setEnabled(running)
#         elif thread_key == "filez2":
#             self.button2.setEnabled(not running)
#             self.terminate_button2.setEnabled(running)

#     def update_status_labels(self, thread_key, status):
#         if thread_key == "voice_assistant":
#             self.status_label1.setText(f"Status: {status}")
#         elif thread_key == "filez2":
#             self.status_label2.setText(f"Status: {status}")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWin = MainWindow()
#     mainWin.show()
#     sys.exit(app.exec_())







######################arko
import sys
import os
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess


class ScriptThread(QThread):
    # Signal to send output to the main thread
    output_signal = pyqtSignal(str)

    def __init__(self, script_name, log_text):
        super().__init__()
        self.script_name = script_name
        self.process = None  # Store the subprocess.Popen object
        self.log_text = log_text  # QTextEdit for logging

    def run(self):
        try:
            script_path = os.path.abspath(self.script_name)
            self.process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line-buffered
                universal_newlines=True
            )

            # Read stdout and stderr in real-time
            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    self.output_signal.emit(output.strip())  # Emit the output signal

            # Capture any remaining output after the process ends
            stdout, stderr = self.process.communicate()
            if stdout:
                self.output_signal.emit(stdout.strip())
            if stderr:
                self.output_signal.emit(stderr.strip())

        except Exception as e:
            self.output_signal.emit(f"Error running {self.script_name}: {e}")

    def terminate_script(self):
        if self.process:
            self.process.terminate()  # Terminate the running process
            self.process = None


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.threads = {}  # Store threads for each script
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Button for Voice Assistant
        self.button1 = QPushButton("Voice Assistant", self)
        self.button1.clicked.connect(lambda: self.run_script("for_nepali.py", "voice_assistant"))
        layout.addWidget(self.button1)

        # Terminate button for Voice Assistant
        self.terminate_button1 = QPushButton("Terminate Voice Assistant", self)
        self.terminate_button1.clicked.connect(lambda: self.terminate_script("voice_assistant"))
        self.terminate_button1.setEnabled(False)
        layout.addWidget(self.terminate_button1)

        # Status label for Voice Assistant
        self.status_label1 = QLabel("Status: Stopped", self)
        layout.addWidget(self.status_label1)

        # Button for VirtualMouse
        self.button2 = QPushButton("VirtualMouse", self)
        self.button2.clicked.connect(lambda: self.run_script("AiVirtualMouseProject.py", "filez2"))
        layout.addWidget(self.button2)

        # Terminate button for VirtualMouse
        self.terminate_button2 = QPushButton("Terminate V-mouse", self)
        self.terminate_button2.clicked.connect(lambda: self.terminate_script("filez2"))
        self.terminate_button2.setEnabled(False)
        layout.addWidget(self.terminate_button2)

        # Status label for VirtualMouse
        self.status_label2 = QLabel("Status: Stopped", self)
        layout.addWidget(self.status_label2)

        # Log text box
        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        self.setLayout(layout)
        self.setWindowTitle("Smart Virtual Interface")
        self.setGeometry(300, 300, 400, 300)  # Adjusted size for additional widgets

    def run_script(self, script_name, thread_key):
        if thread_key in self.threads:
            self.threads[thread_key].terminate_script()  # Terminate if already running
        self.threads[thread_key] = ScriptThread(script_name, self.log_text)
        self.threads[thread_key].output_signal.connect(self.update_log)  # Connect signal to update log
        self.threads[thread_key].start()
        self.update_button_states(thread_key, running=True)
        self.update_status_labels(thread_key, "Running")

    def terminate_script(self, thread_key):
        if thread_key in self.threads:
            self.threads[thread_key].terminate_script()  # Terminate the script
        self.update_button_states(thread_key, running=False)
        self.update_status_labels(thread_key, "Stopped")

    def update_button_states(self, thread_key, running):
        if thread_key == "voice_assistant":
            self.button1.setEnabled(not running)
            self.terminate_button1.setEnabled(running)
        elif thread_key == "filez2":
            self.button2.setEnabled(not running)
            self.terminate_button2.setEnabled(running)

    def update_status_labels(self, thread_key, status):
        if thread_key == "voice_assistant":
            self.status_label1.setText(f"Status: {status}")
        elif thread_key == "filez2":
            self.status_label2.setText(f"Status: {status}")

    def update_log(self, message):
        """Update the log text box with the given message."""
        self.log_text.append(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
