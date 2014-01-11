from urllib2 import urlopen

width = 100
height = 100

url = 'http://placekitten.com/%d/%d' % (width, height)
kitten = urlopen(url).read()

f = open('../images/kitten-%d-%d.jpeg' % (height, width), 'w')
f.write(kitten)
f.close()

print 'Kittens acquired'