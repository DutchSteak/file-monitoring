from flask import Flask, jsonify, send_from_directory, request, url_for
import threading
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


app = Flask(__name__)


is_monitoring = False
new_folder_path = None
file_found_path = None  # To store the path of the found file


class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, observer, target_file):
        """Initialize the handler with the observer and target file."""
        self.observer = observer
        self.target_file = target_file


    def on_created(self, event):
        """Handle the event when a new folder is created."""
        global new_folder_path
        if event.is_directory:
            print(f"New folder created: {event.src_path}")
            new_folder_path = event.src_path
            self.monitor_new_folder_for_file(event.src_path)


    #def on_deleted(self, event):
    #    """Handle the event when a file or folder is deleted."""
    #    global file_found_path, new_folder_path
    #    if event.is_directory and event.src_path == new_folder_path:
    #        print(f"Monitored folder deleted: {event.src_path}")
    #        new_folder_path = None
    #    elif not event.is_directory and event.src_path == file_found_path:
    #        print(f"Target file deleted: {event.src_path}")
    #        file_found_path = None


    def monitor_new_folder_for_file(self, folder_path):
        """Monitor a newly created folder for the target file."""
        global file_found_path
        print(f"Monitoring folder {folder_path} for {self.target_file}...")


        while True:
            target_file_path = os.path.join(folder_path, self.target_file)


            if os.path.exists(target_file_path):
                print(f"Found the file: {target_file_path}")
                file_found_path = target_file_path  # Update the found file path
                self.open_file(target_file_path)
                break
            time.sleep(2)


    def open_file(self, file_path):
        """Attempt to open the file using the default system viewer."""
        try:
            time.sleep(2)
            os.startfile(file_path)  # Opens the file with the default viewer
            print(f"File opened successfully: {file_path}")
            self.observer.stop()
        except Exception as e:
            print(f"Error opening the file: {e}")


def start_observer(path, target_file):
    """Start the file observer in a separate thread."""
    observer = Observer()
    event_handler = FileMonitorHandler(observer, target_file)
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    return observer


@app.route('/run-code', methods=['GET'])
def run_code():
    """Start the file monitoring process."""
    global new_folder_path, file_found_path, is_monitoring

    new_folder_path = None
    file_found_path = None

    path = 'c:\\Users\\colin\\Documents\\PDF test'
    target_file = 'confidence_over_time_plot.pdf'


    def monitor_in_background():
        """Run the file monitor in a background thread."""
        print("Starting observer...")
        observer = start_observer(path, target_file)
        try:
            global is_monitoring
            is_monitoring = True
            while observer.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Stopping observer...")
        finally:
            is_monitoring = False
            observer.stop()
            print("Observer stopping...")
            observer.join()
            print("Observer stopped.")


    threading.Thread(target=monitor_in_background, daemon=True).start()
    return jsonify({'message': 'File monitoring started...'})


@app.route('/get_output')
def get_output():
    """Get the current monitoring status, folder creation, and file finding status."""
    global new_folder_path, file_found_path


    if file_found_path:
        output = f"File found at: {file_found_path}"
    elif new_folder_path:
        output = f"New folder created at: {new_folder_path}. Searching for file..."
    else:
        output = "Monitoring for new folders..."


    return jsonify({'output': output})


from flask import render_template


@app.route('/')
def serve_index_stage():
    return render_template('index_stage.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'dna_logo.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(debug=False)