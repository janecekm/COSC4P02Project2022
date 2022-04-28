with open('./programLinks.txt', 'rb') as source_file:
  with open('../cleandata/program.txt', 'w+b') as dest_file:
    contents = source_file.read()
    dest_file.write(contents.decode('utf-16').encode('utf-8'))
    # dest_file.write(contents.decode('utf-8-sig').encode('utf-8')) # for program info