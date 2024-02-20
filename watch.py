import time
import os
import datetime
import config as cr
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

config_values = cr.read_config()
outputdir = config_values.get("output_dir")


class Watcher:
    DIRECTORY_TO_WATCH = config_values.get("watch_path")

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(3)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == "created":
            # Take any action here when a file is first created.
            time.sleep(6)
            print("Received created event - %s." % event.src_path)
            location = str(event.src_path).rfind("\\")
            print(location)
            watchdir = config_values.get("watch_path")
            allfiles = os.listdir(os.path.abspath(watchdir))
            print(allfiles)
            for eachfile in allfiles:
                f = open(os.path.abspath(watchdir) + "/" + eachfile, "rt")
                data = f.read()
                print(data)
                f.close()
                """
                printjobs = data.split("\n")
                date_time = datetime.datetime.now()
                formated_date_time = "{:%Y-%m-%d-%H-%M-%S}".format(date_time)
                i = 0

                for p in printjobs:
                    if len(p) > 3:
                        i = i + 1
                        formattedJob = Tester.readString(p)
                        print(formattedJob)
                        # print(i)
                        filename = (
                            "output " + str(i) + " " + formated_date_time + ".txt"
                        )
                        writefile = open(outputdir + "\\" + filename, "w")
                        writefile.write(formattedJob)
                        time.sleep(3)

                print("Files Written")

                os.remove(os.path.abspath(watchdir) + "/" + eachfile)
            """
            # data = Tester.readFile(filename)
            # process all the data inside the file, store in array or write files at intervals

            # delete file

        elif event.event_type == "modified":
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)


if __name__ == "__main__":
    print("\n ********** Copyright and Licensed by Instrumec Pty Ltd **********")
    w = Watcher()
    w.run()
