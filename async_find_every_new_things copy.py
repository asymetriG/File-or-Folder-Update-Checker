import os
import datetime
import asyncio



def logThem(text):
    today = str(datetime.date.today())
    
    dirname = os.path.dirname(__file__)
    
    with open(f"{dirname}\\{today} logs.txt","a",encoding="utf-8") as f:
        f.write(text)

#Folder Create Dedector   

async def folder_created_check(path,current_folders):  
  
    while True:
  
        for root,directories,files in os.walk(path):
            if root in current_folders:
                continue
            else:
                x = datetime.datetime.now()
                print(root+f" folder created at {x}\n")
                logThem(root+f" folder created at {x}\n\n")
                current_folders.append(root)
                
        await asyncio.sleep(0.1)
                
#File Create Dedector
              
async def file_created_check(path,current_files):

    while True:     
     
        for root,directories,files in os.walk(path):
            for f in files:
                if (root+"\\"+f) in current_files:
                    continue
                else:
                    x = datetime.datetime.now()
                    print(root+"\\"+f+f" file created at {x}\n")
                    logThem(root+"\\"+f+f" file created at {x}\n\n")
                    current_files.append(root+"\\"+f)
        await asyncio.sleep(0.1)
        
        
#File Remove Dedector


async def file_moved_or_deleted_check(path,current_files):
    while True:
        new_current_files = []
        for root,directories,files in os.walk(path):
            for f in files:
                new_current_files.append(root+"\\"+f)
                
        for file in current_files:
            try:
                new_current_files.remove(file)
            except:
                x = datetime.datetime.now()
                print(f"{file} file deleted or moved at {x}\n")
                logThem(f"{file} file deleted or moved at {x}\n\n")
                current_files.remove(file)
                
        await asyncio.sleep(0.1)
        
async def main():
    current_files = []
    current_folders = []
    tasks = []
    
    path = input("Path: ")


    os.chdir(path)
    
    for root,directories,files in os.walk(path):
        current_folders.append(root)
        
    for root,directories,files in os.walk(path):
        for f in files:
            current_files.append(root+"\\"+f)
  
    
    t1 = asyncio.create_task(folder_created_check(path,current_folders))
    t2 = asyncio.create_task(file_created_check(path,current_files))
    t3 = asyncio.create_task(file_moved_or_deleted_check(path,current_files))
    
    tasks.append(t1)
    tasks.append(t2)
    tasks.append(t3)
    
    await asyncio.gather(*tasks)
    
    
if __name__=="__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
    
    
    
    
    
