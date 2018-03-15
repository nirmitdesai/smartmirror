import tungsten


client = tungsten.Tungsten('LTQ79R-2QP6YAAJ9A')
params = {'format' :['plaintext', 'image'], 
		  'scanner' : 'data',
		  'units' : 'metric'}

result = client.query('How far is New York from Los Angeles', params)
for pod in result.pods:
	print "scanner-->",pod.scanner
	print "ans-->" , pod.format
