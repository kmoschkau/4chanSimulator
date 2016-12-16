import requests, json, time, re, markovify, sys
refetch = str(sys.argv[1])
print(refetch)
reload(sys)
sys.setdefaultencoding('utf8')

def clean(words):
  cleanbr = re.compile('<b.*?>')
  cleantext = re.sub(cleanbr, '\n', words)
  cleanr = re.compile('<.*>')
  cleantext = re.sub(cleanr, '', words)  
  return cleantext


if(refetch == 'y'):
  target = open('threadscrape.txt', 'w')
  target.truncate()
  response = requests.get("https://a.4cdn.org/b/threads.json")
  #print response.content
  parsed_json = json.loads(response.content)
  #length is 10
  for i in range(1,10):
    print(str(i) + "0% done")
    num_threads = len(parsed_json[i]['threads'])
    for j in range(1,num_threads):
      time.sleep(1)
      thread_num = parsed_json[i]['threads'][j]['no']
      thread_response = requests.get("https://a.4cdn.org/b/thread/" + str(thread_num) + ".json")
      if thread_response.status_code == 200: 
        parsed_thread = json.loads(thread_response.content)
      else:
        break
      num_posts = len(parsed_thread['posts'])
      for k in range(0,num_posts):
        #print(parsed_thread['posts'][k].keys())
        post = parsed_thread['posts'][k]
        if 'com' in post:
          words = parsed_thread['posts'][k]['com']
          words = clean(words)
          #print(words)
          target.write(words + "\n")
  target.close


target = open('threadscrape.txt', 'r')
dataset = target.read()
#print(dataset)
text_model = markovify.Text(dataset)

print("****Starting Markovify****\n")

for i in range(5):
  print(text_model.make_sentence())

target.close();

#print(thread_response)
#print(parsed_thread)
#print(parsed_thread['posts'][1].keys())
#print(parsed_thread['posts'][1]['resto'])
#print(parsed_thread['posts'][1]['now'])

