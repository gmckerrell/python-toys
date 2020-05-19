days=[
  ["first", "a partridge in a pear tree"],
  ["second", "two turtle doves"],
  ["third", "three french hens"],
  ["forth", "four calling birds"],
  ["fifth", "FIVE GOLD RINGS"],
  ["sixth", "six geese a laying"],
  ["seventh", "seven swans a swimming"],
  ["eighth", "eight maids a milking"],
  ["ninth", "nine ladies dancing"],
  ["tenth", "ten lords a leaping"],
  ["eleventh", "eleven pipers piping"],
  ["twelth", "twelve drummers drumming"]
]

def printDays(day):
  for d in range(day, -1, -1):
    if (day > 0 and d == 0):
      print("and", end=' ')
    print(days[d][1])

def printVerse(day):
  print("On the %s day of christmas"%days[day][0])
  print("My true love gave to me")
  printDays(day)
  
for d in range(0, 12):
  printVerse(d)
  print()
