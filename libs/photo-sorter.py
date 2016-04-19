#!/usr/bin/env python3
import sys, os
import textwrap
import argparse
import re
import datetime, time
import hashlib
import shutil
from PIL import Image
import calendar

def get_minimum_creation_time(exif_data):
	if exif_data is None:
		return None
	mtime = '?'
	if 306 in exif_data and exif_data[306] < mtime: # 306 = DateTime
		return exif_data[306]
	if 36867 in exif_data and exif_data[36867] < mtime: # 36867 = DateTimeOriginal
		return exif_data[36867]
	if 36868 in exif_data and exif_data[36868] < mtime: # 36868 = DateTimeDigitized
		return exif_data[36868]
	return None

def run_walk_pictures_sorter(source, desctination):
	for root, subfolders, files in os.walk(source):
		for picture in files:
			is_unknown_ctime = False
			m = re.search(r'^.*\.(jpeg|jpg|png|gif|psd)$', picture, flags=re.I)
			if m:
				srcfile_path = root + os.path.sep + picture
				print(srcfile_path)

				try:
					img = Image.open(srcfile_path)
				except:
					print ("Skipping '%s' due to exception:\n\r" % (srcfile_path))
					continue

				mtime = get_minimum_creation_time(img._getexif())

				if mtime is None:
					ctime = time.ctime(os.path.getctime(root + os.path.sep + picture))
					is_unknown_ctime = True
				else:
					ctime = mtime

				destfile_path = desctination + os.sep
				if is_unknown_ctime:
					destfile_path += 'unknown' + os.sep

				destfile_path += ctime + '.' + m.group(1)
			
				flag_save_destinatin = not os.path.isfile(destfile_path)
			
				if not flag_save_destinatin:
					while_cnt = 0
					t_flag = True
					while True:
						while_cnt += 1
						if(os.path.isfile(destfile_path)):
							if not hashlib.md5(open(srcfile_path,'rb').read()).hexdigest() == hashlib.md5(open(destfile_path,'rb').read()).hexdigest():
								t_flag &= True
							else:
								t_flag &= False

							destfile_path = desctination + os.sep
							if is_unknown_ctime:
								destfile_path += 'unknown' + os.sep

							destfile_path += ctime + '_' + str(while_cnt) + '.' + m.group(1)
						else:
							break
						# endwhile
					flag_save_destinatin = t_flag
					#endif
				print (destfile_path+"\n")
				if flag_save_destinatin:
					shutil.copyfile(srcfile_path, destfile_path)
				#endif
			#endfor
		#endfor
	return None

argv_parser = argparse.ArgumentParser(prog='photo-sorter', formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent("""\
							Sorting your pictures from source folder and save to destination folder."""),
							add_help=True)

argv_parser.add_argument("-s", "--source", action="store", metavar='FOLDER PATH', dest='source', type=str, help="Saves the info to the specified file")
argv_parser.add_argument("-d", "--destination", action="store", metavar='FOLDER PATH', dest='destination', type=str, help="Saves the info to the specified file")							
argv_parser.add_argument("-v", "--verbose", action="store_true", dest='verbose', default=False, help="Print the Python version number and exit")
							
args = argv_parser.parse_args()

if args.verbose:
	print ("Version 1.4. Built by Web Apr 19 2016 13:00 GMT")
	print ("Please, press any key for exit...")
	input()
	sys.exit(0)
			
if args.source is None or args.destination is None:
	argv_parser.print_help()
	print ("Please, press any key for exit...")
	input()
	sys.exit(1)
	
if not os.path.exists(args.source):
	print ("* Error: `source` directory does not exists")
	print ("Please, press any key for exit...")
	input()
	sys.exit(2)
	
if not os.path.exists(args.destination):
	print ("* Error: `destination` directory does not exists")
	print ("Please, press any key for exit...")
	input()
	sys.exit(3)
	
run_walk_pictures_sorter( re.sub(r'/$',r'',args.source,flags=re.I), re.sub(r'/$',r'',args.destination,flags=re.I))

print ("Done")
print ("Please, press any key for exit...")
input()
sys.exit(0)



