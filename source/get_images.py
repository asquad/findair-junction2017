from glob import glob
import os

def get_pictures(username, n_photos):
    print("Running generated_problems_test")
    command = "mkdir " + username
    os.system(command)

    command = "python -m instaLooter " + username + " " + username + "/ "+ " -n " + str(n_photos)
    os.system(command)

    return glob(username + "/*")
