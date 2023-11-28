from tracker_manager import TrackerManager
from tracker import Tracker

def main():
    tracker_manager = TrackerManager()
    while (True):
        tracker_manager.poll_trackers()
        tracker_list = tracker_manager.get_trackers()
        for tracker in tracker_list:
            print(tracker)

if __name__ == '__main__':
    main()