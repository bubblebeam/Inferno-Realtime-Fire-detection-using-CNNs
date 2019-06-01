#program to randomly move files(images here) from one folder to another
#used to create the test and valid sets from main set
import random, os
import shutil
path = r"/home/ramya/Desktop/project/Dataset/train/fire"
src = "/home/ramya/Desktop/project/Dataset/train/fire/"
dest = "/home/ramya/Desktop/project/Dataset/valid/fire"

random_filename = random.choice([
    		x for x in os.listdir(path)
    		if os.path.isfile(os.path.join(path, x))
	])


for i in range(1,2532): 
	while os.path.exists(dest+'/'+str(random_filename)):
		random_filename = random.choice([
    			x for x in os.listdir(path)
    			if os.path.isfile(os.path.join(path, x))
		])

	print(random_filename)
	shutil.move(src+str(random_filename),dest)

