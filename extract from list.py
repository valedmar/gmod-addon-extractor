import os, fnmatch, subprocess

DEBUG=False

current_dir = os.path.dirname(os.path.realpath(__file__)) + "\\"
addon_folder = "D:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\4000\\"
out_folder = 'extracted'
temp_folder = 'temp'
gma_folder = 'gma'

# get this from https://getcollectionids.moonguy.me COMMA separated
addon_ids = [1812190208,110871780,167547072,212055526,864100230,2129490712,145316417,183797802,889034501,163322799,1678408548,1937891124,649273679,2969994508,2913484004,2919111381,1517464837]

# run cleanup
def clean_up(current_dir, folder):
    if os.path.exists(current_dir+folder):
        os.popen('del "'+current_dir+folder+"\\*\" /Q /S")
        os.popen('rmdir "'+current_dir+folder+"\" /Q /S")
    os.popen("mkdir "+current_dir+folder)

clean_up(current_dir, gma_folder)    
clean_up(current_dir, temp_folder)  
clean_up(current_dir, out_folder)  



def get_files(directory, filetype):
    files = []
    for file in os.listdir(directory):
        if fnmatch.fnmatch(file, filetype):
            files.append(directory+'\\'+file)
            return files

addonsg = []
addonsb = []

for x in addon_ids:
    filesg = get_files(addon_folder+str(x), '*.gma')
    filesb = get_files(addon_folder+str(x), '*.bin')
    
    if filesg != None:
        for file in filesg:
            if file != None:
                addonsg.append(file)
    
    if filesb != None:
        for file in filesb:
            if file != None:
                addonsb.append(file)


addonslen = len(addonsg)+len(addonsb)
if addonslen == len(addon_ids):
    print('All addons from workshop collection found! ('+str(addonslen)+')')
else:
    print('Only found', addonslen, 'out of', len(addon_ids), 'addons!')


for addon in addonsg:
    print('extracting', addon)
    if DEBUG == True:
        print(subprocess.Popen(current_dir+'gmad.exe extract -file "'+addon.replace("\\","/")+'" -out "'+current_dir+out_folder+'"', shell=True, stdout=subprocess.PIPE).stdout.read())
    else:
        subprocess.Popen(current_dir+'gmad.exe extract -file "'+addon.replace("\\","/")+'" -out "'+current_dir+out_folder+'"', shell=True, stdout=subprocess.PIPE).stdout.read()
        
    addon_filename = addon.rsplit('\\', 1)[-1]
    os.popen('copy "'+addon+'" "'+current_dir+gma_folder+"\\"+addon_filename)



for addon in addonsb:
    print('extracting', addon)
    addon_filename = addon.rsplit('\\', 1)[-1]
    if DEBUG == True:
        print(subprocess.Popen('7z e -y -o"'+current_dir+temp_folder+'" "'+addon.replace("\\","/")+'"', shell=True, stdout=subprocess.PIPE).stdout.read())
    else:
        subprocess.Popen('7z e -y -o"'+current_dir+temp_folder+'" "'+addon.replace("\\","/")+'"', shell=True, stdout=subprocess.PIPE).stdout.read()
        
    os.rename(current_dir+temp_folder+'\\'+addon_filename[:-4], current_dir+temp_folder+'\\'+addon_filename[:-4]+".gma")
    new_addon_file = current_dir+temp_folder+'\\'+addon_filename[:-4]+".gma"
    
    if DEBUG == True:
        print(subprocess.Popen(current_dir+'gmad.exe extract -file "'+new_addon_file+'" -out "'+current_dir+out_folder+'"', shell=True, stdout=subprocess.PIPE).stdout.read())
    else:
        subprocess.Popen(current_dir+'gmad.exe extract -file "'+new_addon_file+'" -out "'+current_dir+out_folder+'"', shell=True, stdout=subprocess.PIPE).stdout.read()

    os.rename(new_addon_file, current_dir+gma_folder+"\\"+addon_filename.replace(".bin", ".gma"))

