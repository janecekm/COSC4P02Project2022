with open('./schedule.txt', 'rb') as source_file:
  with open('../cleandata/schedule.txt', 'w+b') as dest_file:
    contents = source_file.read()
    dest_file.write(contents.decode('utf-16').encode('utf-8'))